#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script to convert EDItEUR Thema categories from excel to json.

SYNOPSIS

    excel_to_json.py [-l,--language] [-f,--input_file]

DESCRIPTION
    Converts standard EDItEUR Thema data, given in Excel format, to a JSON.
    It excepts two arguments: `language` and `input_file`.

    The script opens the Excel file specified by `input_file`, run through
    the rows of it and create a list of {"code": ..., "heading": ...
    "parent": ... } objects, based on the data in the file.

    A simple check is done in the script, to verify whether the specified
    language is English and, in that case, looks for the heading value
    in the English Heading column, otherwise in the New Language Heading
    column. Find all supported languages at http://www.editeur.org/151/Thema/.

    When all of the data from the input file is processed, the compiled list
    is saved as JSON to `thema_<language>.json` in the `data` directory.
"""
from __future__ import print_function
import os
import sys
import xlrd
import json
import argparse
from xlrd.biffh import XLRDError

# All supported languages, more details at http://www.editeur.org/151/Thema/
HEADING_COLNAME_BY_LANGUAGE = {
    'ar': 'Arabic Heading',
    'da': 'Danish Heading',
    'de': 'German Heading',
    'en': 'English Heading',
    'es': 'Materia español',
    'fr': 'Libellé français',
    'de': 'German Heading',
    'hu': 'Hungarian Language Heading',
    'it': 'etichette italiane',
    'ja': 'Japanese Heading',
    'lt': 'Lithuanian Heading',
    'nb': 'Norwegian Heading',
    'pl': 'Wersja polska',
    'pt': 'Título (Heading) Português',
    'sv': 'Swedish Heading',
    'tr': 'Başlık',
}

NOTES_COLNAME_BY_LANGUAGE = {
    'ar': 'Arabic Notes',
    'da': 'Danish Notes',
    'de': 'German Notes',
    'en': 'Notes',
    'es': 'Notas español',
    'fr': 'Commentaires français',
    'hu': 'Hungarian Language Notes',
    'it': 'note italiani',
    'ja': 'Japanese Notes',
    'lt': 'Lithuanian Notes',
    'nb': 'Norwegian Notes',
    'pl': 'Komentarze',
    'pt': 'Notas (Notes) Português',
    'sv': 'Swedish Notes',
    'tr': 'Notlar',
}

LANGUAGE_INFO_COLNAME_BY_LANGUAGE = {
    x: "Original language" if x == "en" else "New language"
    for x in NOTES_COLNAME_BY_LANGUAGE
}

CODE_COLNAME = 'Code'
PARENT_COLNAME = 'Parent'
RELATED_COLNAME = 'Related (see also)'
ADDITIONS_COLNAME = (
    'Additions SINCE VERSION 1.1\n'
    'Changes SINCE VERSION 1.1\n'
    'Added National Extensions'
)

HEADING_NEW_COLNAME = 'heading'
CODE_NEW_COLNAME = 'code'
PARENT_NEW_COLNAME = 'parent'
NOTES_NEW_COLNAME = 'notes'
RELATED_NEW_COLNAME = 'related_categories'
LANGUAGE_INFO_NEW_COLNAME = 'language_info'

LANGUAGE_CODE_ROW_INDEX = 1
SEE_ALSO_TRANSLATION_ROW_INDEX = 2
AND_SUBCATEGORIES_TRANSLATION_ROW_INDEX = 3

JSON_FILENAME_PATTERN = 'thema_{}.json'
HEADERS_TO_CHANGE = {
    CODE_COLNAME: CODE_NEW_COLNAME,
    PARENT_COLNAME: PARENT_NEW_COLNAME,
    RELATED_COLNAME: RELATED_NEW_COLNAME,
}
HEADERS_TO_CHANGE.update(
    {
        native_name: HEADING_NEW_COLNAME
        for native_name in HEADING_COLNAME_BY_LANGUAGE.values()
    }
)
HEADERS_TO_CHANGE.update(
    {
        native_name: NOTES_NEW_COLNAME
        for native_name in NOTES_COLNAME_BY_LANGUAGE.values()
    }
)
HEADERS_TO_CHANGE.update(
    {
        native_name: LANGUAGE_INFO_NEW_COLNAME
        for native_name in LANGUAGE_INFO_COLNAME_BY_LANGUAGE.values()
    }
)

_IS_PYTHON2 = sys.version_info[0] == 2


class ThemaFileParser(object):
    """Base class for EDItEUR Thema parsers."""

    def __init__(self, input_file):
        """Default constructor for parsers."""
        self.input_file = input_file

    def parse(self, filter_by=None, clean_headers_language=None):
        """Method to parse the input file.

        It must be overridden in the child classes.
        :param clean_headers_language: language to clean header.
        :param filter_by: list of column names to filter by.
        """
        raise NotImplementedError


class ExcelThemaFileParser(ThemaFileParser):
    """Parser to translate excel EDItEUR Thema files to json."""

    THEMA_SHEET_NAME_PATTERN = 'Vers {} Codes & Headings'

    def __init__(self, input_file, thema_version='1.2'):
        """Constructor for excel-to-json Thema parser."""
        super(ExcelThemaFileParser, self).__init__(input_file)
        # Open the book.
        self.xl_book = xlrd.open_workbook(self.input_file)
        # Get the thema sheet that contains the codes and headings.
        self.xl_sheet = self.xl_book.sheet_by_name(
            self.THEMA_SHEET_NAME_PATTERN.format(thema_version)
        )
        # Get the column names.
        self.headers = [
            cell.value.encode('utf-8')
            if _IS_PYTHON2 else str(cell.value)
            for cell in self.xl_sheet.row(0)
        ]

    def _add_language_info(self, row_values, language):
        """
        Add related category translation info to the row.

        add the translations for "See also:" and "and its subcategories"
        for the specified language.

        """
        # Get indexes of columns we want.
        language_info_colname = LANGUAGE_INFO_COLNAME_BY_LANGUAGE[language]
        language_info_index = self.headers.index(language_info_colname)
        # Get category-related translations and language.
        see_also_translation = self.xl_sheet.row(
            SEE_ALSO_TRANSLATION_ROW_INDEX
        )[language_info_index].value
        and_subcategories_translation = self.xl_sheet.row(
            AND_SUBCATEGORIES_TRANSLATION_ROW_INDEX
        )[language_info_index].value
        language_code = self.xl_sheet.row(
            LANGUAGE_CODE_ROW_INDEX
        )[language_info_index].value

        language_info = {
            "language": language_code,
            "see_also_translation": see_also_translation,
            "and_subcategories_translation": and_subcategories_translation
        }
        return (language_info, row_values)

    def parse(self, filter_by=None, clean_headers_language=None):
        """Parse the sheet with thema codes and return a list of sheet-as-dict.

        Each row is a dict where the keys are the headings and the values
        the content of each cell.

        Each row (dict) will contain all columns if `filter_by==None` (
        default behaviour), otherwise only the columns present in `filter_by`

        e.g. filter_by=None, clean_headers_language=None
        [
            {
                'New Language Heading': 'Musikgenrer',
                'English Heading': 'Music: styles & genres',
                ...
                'Code': 'AVL',
                'Parent': 'AV',
                ...
            },
            {
                'New Language Heading': 'Klassisk musik og orkestermusik',
                'English Heading': 'Art music, orchestral & formal music',
                ...
                'Code': 'AVLA',
                'Parent': 'AVL',
                ...
            },
            ...

        ]
        e.g. filter_by=['New Language Heading', 'Code', ],
             clean_headers_language=None
        [
            {
                'New Language Heading': 'Musikgenrer',
                'Code': 'AVL',
                'Parent': 'AV',
            },
            {
                'New Language Heading': 'Klassisk musik og orkestermusik',
                'Code': 'AVLA',
                'Parent': 'AVL',
            },
            ...

        ]
        e.g. filter_by=['New Language Heading', 'Code', ],
             clean_headers_language='en'
            {
                'heading': 'Music: styles & genres',
                ...
                'code': 'AVL',
                'parent': 'AV',
                ...
            },
            {
                'heading': 'Art music, orchestral & formal music',
                ...
                'code': 'AVLA',
                'parent': 'AVL',
                ...
            },
            ...

        ]

        :param filter_by: List of keys to keep.
        :param clean_headers_language: Language to use to change the headings
        keys from 'New Language Heading' or 'English Heading' to 'heading'.
        :return: List of dicts with all cells.
        """
        # Create the list of sheet-as-dict.
        sheet_as_dict = []
        language_info = {}
        for row_index in range(self.xl_sheet.nrows)[1:]:
            row_values = [cell.value for cell in self.xl_sheet.row(row_index)]
            related_index = self.headers.index(RELATED_COLNAME)
            additions_index = self.headers.index(ADDITIONS_COLNAME)
            # Get related categories until end column (additions column).
            related_categories = [
                category for category in row_values[
                    related_index:additions_index
                ]
                if category
            ]
            # Insert categories and category related translations into row.
            row_values[related_index] = related_categories
            if clean_headers_language:
                language_info, row_values = self._add_language_info(
                    row_values,
                    clean_headers_language
                )

            sheet_as_dict.append(dict(zip(self.headers, row_values)))

        # Prune keys if it needs.
        if filter_by:
            sheet_as_dict = [
                {
                    k: v for k, v in row.items() if k in filter_by
                }
                for row in sheet_as_dict
            ]
        # Clean headers if it needs.
        if clean_headers_language:
            clean_list = []
            for row in sheet_as_dict:
                item = {}
                for k, v in row.items():
                    item.update(
                        {k: v}
                        if k not in HEADERS_TO_CHANGE.keys()
                        else {HEADERS_TO_CHANGE[k]: v}
                    )
                clean_list.append(item)
            return {"language_info": language_info, "categories": clean_list}

        return {"language_info": language_info, "categories": sheet_as_dict}


def add_related_category_info_to_notes(data):
    """
    Add information about the related categories to the notes.

    e.g for category DNP (with related categories WTL*, AJF)
    we add the string "See also: WTL* Travel writing and its subcategories,
    AJF Photojournalism".
    """
    lang_info = data["language_info"]
    rows = data["categories"]
    see_also_translation = lang_info["see_also_translation"]
    and_subcategories_translation = lang_info["and_subcategories_translation"]

    for row in rows:
        if not row[RELATED_NEW_COLNAME]:
            continue

        def is_wildcard_category(code):
            return code[-1] == "*"

        def fetch_category(code):
            return [cat for cat in rows if cat["code"] == code][0]

        def generate_category_string(code):
            if is_wildcard_category(code):
                lookup = code[:-1]
                postfix = u" {}".format(and_subcategories_translation)
            else:
                lookup = code
                postfix = u""
            related_category = fetch_category(lookup)
            return u"{} {}{}".format(
                code,
                related_category["heading"],
                postfix
            )

        row[NOTES_NEW_COLNAME] += u"{}{} ".format(
            "" if not row[NOTES_NEW_COLNAME] else ". ",
            see_also_translation
        )

        row[NOTES_NEW_COLNAME] += u", ".join(
            generate_category_string(code) for code in row[RELATED_NEW_COLNAME]
        )
    return data


def main(language, thema_filepath):
    """Main method to parse the Excel EDItEUR Thema to json.

    :param language: original language.
    :param thema_filepath: full path for the excel file.
    :return:
    """
    dir_name = os.path.dirname(thema_filepath)
    print('Processing file {}'.format(thema_filepath))
    try:
        # create the parser instance.
        xl_parser = ExcelThemaFileParser(thema_filepath)
        # Parse the excel file and get the list of sheet-as-dict with codes.
        data = xl_parser.parse(
            [
                CODE_COLNAME,
                PARENT_COLNAME,
                HEADING_COLNAME_BY_LANGUAGE[language],
                NOTES_COLNAME_BY_LANGUAGE[language],
                RELATED_COLNAME,
            ],
            language
        )
        # Add related category info to category notes.
        data = add_related_category_info_to_notes(data)
    except XLRDError:
        print(
            'The given file is not valid, please ensure to '
            'provide a valid EDItEUR Thema Excel file.'
        )
        exit(1)
    json_file_path = os.path.join(
        dir_name, JSON_FILENAME_PATTERN.format(language)
    )
    print('Saving to JSON file {}'.format(json_file_path))
    # Save the result to a JSON file in the same folder of the input file.
    json_file = open(json_file_path, 'w+')
    json_file.write(json.dumps(data))
    json_file.close()
    print(
        'Processing completed, total amount of thema codes: {}'.format(
            len(data["categories"])
        )
    )


if __name__ == '__main__':
    # Process the args passed to the script.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l',
        '--language',
        type=str,
        choices=HEADING_COLNAME_BY_LANGUAGE.keys(),
        help='Language to process, e.g. `en` for English, '
             '`da` for Danish. Find all supported languages '
             'at http://www.editeur.org/151/Thema/',
        required=True,
    )
    parser.add_argument(
        '-i',
        '--input_file',
        type=str,
        help='File to process',
        required=True
    )
    args = parser.parse_args()
    # Parse the file and save result to the Json file.
    main(args.language, args.input_file)
    exit(0)
