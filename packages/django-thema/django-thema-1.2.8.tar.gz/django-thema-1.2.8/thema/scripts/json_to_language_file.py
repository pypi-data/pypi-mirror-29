#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script to generate translation po&mo files given thema data in JSON format.

SYNOPSIS

    json_to_language_file.py [-l,--language]

DESCRIPTION
    The script takes a single argument, language. When the script
    is run, it will open the English JSON data file and the matched
    language file, create a proper django.po file based on the data in the
    files, and place it in the correct locale/<language>/LC_MESSAGES directory.

    Finally, it creates a django.mo file.

    Find all supported languages at http://www.editeur.org/151/Thema/.
"""
from __future__ import print_function
import argparse
import json
import os
import polib
from os import path
from os.path import join
from datetime import datetime as dt

SUPPORTED_LANGUAGES = [
    'ar',
    'da',
    'en',
    'es',
    'fr',
    'de',
    'hu',
    'it',
    'ja',
    'lt',
    'nb',
    'pl',
    'pt',
    'sv',
    'tr',
]

BASE_DIR = path.dirname(path.realpath(__file__))
THEMA_APP_DIR = join(BASE_DIR, '../')
DATA_DIR = join(THEMA_APP_DIR, 'data')
THEMA_JSON_EN = join(DATA_DIR, 'thema_en.json')
LOCALE_BASE_DIR = join(THEMA_APP_DIR, 'locale')


CODE_KEY_NAME = 'code'
HEADING_KEY_NAME = 'heading'
NOTES_KEY_NAME = 'notes'
TRANSLATION_PO_FILENAME = 'django.po'
TRANSLATION_MO_FILENAME = 'django.mo'


class LanguageFileGenerator(object):
    """Class to generate language files given thema JSON generated files."""

    def __init__(self, thema_en_filepath, thema_language_filepath):
        """Initialize the language file generator."""
        self.thema_en = thema_en_filepath
        self.thema_language = thema_language_filepath

    def _get_term(self, code, list_terms):
        """Return the first match of searching code in the list of items.

        :param code: code to search
        :param list_terms: list of sheet-as-dict items
        :return: first match
        """
        return next(
            (item for item in list_terms if item[CODE_KEY_NAME] == code),
            None
        )

    def gettext_timestamp(self, timestamp='%Y-%m-%d %H:%M%z'):
        """Give the time in the standard timestamp format in for PO files."""
        return dt.now().strftime(timestamp)

    def create_language_folders(self, language):
        """Create the language folders if they don't exist.
        :param language: language to create folders.
        """
        # Check and create the `locale` folder.
        if not path.exists(LOCALE_BASE_DIR):
            os.makedirs(LOCALE_BASE_DIR)

        # Check and create language folder
        LANGUAGE_DIR = join(LOCALE_BASE_DIR, '{}'.format(language))
        if not path.exists(LANGUAGE_DIR):
            os.makedirs(LANGUAGE_DIR)

        # Check and create LC_MESSAGES folder
        LANGUAGE_FULL_DIR = join(LANGUAGE_DIR, 'LC_MESSAGES')
        if not path.exists(LANGUAGE_FULL_DIR):
            os.makedirs(LANGUAGE_FULL_DIR)

        return LANGUAGE_FULL_DIR

    def generate_translation_files(self, language):
        """Generate both translation .po and .mo files for the given language.
        """
        po = polib.POFile()
        now = self.gettext_timestamp()
        # Add the meta data.
        po.metadata = {
            'Project-Id-Version': '1.2',
            'Report-Msgid-Bugs-To': 'publish@saxo.com',
            'POT-Creation-Date': now,
            'PO-Revision-Date': now,
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
        }
        en_terms = json.loads(
            open(self.thema_en).read(), encoding='utf-8'
        )["categories"]
        translated_terms = json.loads(
            open(self.thema_language).read(), encoding='utf-8'
        )["categories"]
        for en_term in en_terms:
            translated_item = self._get_term(
                en_term[CODE_KEY_NAME],
                translated_terms
            )
            if translated_item:
                po.append(
                    polib.POEntry(
                        msgid=en_term[HEADING_KEY_NAME],
                        msgstr=translated_item[HEADING_KEY_NAME],
                    )
                )
                if en_term[NOTES_KEY_NAME] and translated_item[NOTES_KEY_NAME]:
                    po.append(
                        polib.POEntry(
                            msgid=en_term[NOTES_KEY_NAME],
                            msgstr=translated_item[NOTES_KEY_NAME],
                        )
                    )
        # Create the folders and get path.
        destination_path = self.create_language_folders(language)
        po_path = join(destination_path, TRANSLATION_PO_FILENAME)
        mo_path = join(destination_path, TRANSLATION_MO_FILENAME)
        # Save the POFile as .po and .mo
        po.save(po_path)
        po.save_as_mofile(mo_path)

        return po.percent_translated(), po_path, mo_path


def main(language):
    """Main method to generate .po and .mo language files.

    :param language: language to process.
    """
    thema_language_name = 'thema_{}.json'.format(language)
    THEMA_JSON_LANGUAGE = join(DATA_DIR, thema_language_name)
    # Check each needed file is available
    if not path.exists(THEMA_JSON_LANGUAGE):
        print(
            "The {} file doesn't exist in the data directory. Make sure to "
            "generate it, see excel_to_json.py script.".format(
                thema_language_name
            )
        )
        exit(1)
    if not path.exists(THEMA_JSON_EN):
        print(
            "The English JSON file doesn't exist in the data directory. "
            "Make sure to generate it, see excel_to_json.py script."
        )
        exit(1)
    # Create an instance for the Language Generator
    # and generate translation files.
    print("Generating translation files...")
    percent, po_path, mo_path = LanguageFileGenerator(
        THEMA_JSON_EN, THEMA_JSON_LANGUAGE
    ).generate_translation_files(language)
    # Print some useful data.
    print("Percent of entries translated: {}%".format(percent))
    print('Saved translation .po file to {}'.format(po_path))
    print('Saved compiled .mo file to {}'.format(mo_path))


if __name__ == '__main__':
    # Process the args passed to the script.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l',
        '--language',
        type=str,
        choices=SUPPORTED_LANGUAGES,
        help='Language to process, e.g. `en` for English, '
             '`da` for Danish. Find all supported languages '
             'at http://www.editeur.org/151/Thema/',
        required=True,
    )
    # Parse the json file, generate the .po and .mo language files.
    main(parser.parse_args().language)
    exit(0)
