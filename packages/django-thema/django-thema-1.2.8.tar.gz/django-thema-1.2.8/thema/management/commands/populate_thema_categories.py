"""Command to create/update ThemaCategory table.

When the command is run, the data/thema_en.json file is opened. Then iterate
over the categories in the file and check whether there's an existing instance
of ThemaCategory with the code of the category. If so, update the header of the
instance with the value from the file. If not, create an instance with the code
and header from the file. Keep track of how many were updated and how many were
created.

Afterwards, do a reverse check and see if there are any obsolete categories in
the database that are not in the data file. If so, keep track of which.

Finally, print out a report saying how many were updated and how many were
created. If any obsolete categories were found, print out how many, list them
with code and header and finally print an encouragement to manually remove
these after dealing with any possible references them.
"""
import sys
import json
from os import path
from os.path import join
from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from thema.models import ThemaCategory

BASE_DIR = path.dirname(path.realpath(__file__))
THEMA_JSON_EN = join(BASE_DIR, '../../data/thema_en.json')

CODE_KEY_NAME = 'code'
HEADING_KEY_NAME = 'heading'
PARENT_KEY_NAME = 'parent'
NOTES_KEY_NAME = 'notes'


class Command(BaseCommand):
    help = 'Create or update Thema Categories.'

    def _get_parent(self, parent_code):
        parent = None
        if not parent_code:
            return parent
        else:
            return ThemaCategory.objects.get(code=parent_code)

    def _get_obsolete_categories(self, categories_in_file):
        db_categories = ThemaCategory.objects.values(
            'code', 'header'
        )
        obsolete_categories = []
        for db_category in db_categories:
            exists = next(
                (
                    item for item in categories_in_file
                    if item['code'] == db_category['code']
                ),
                None
            )
            if not exists:
                obsolete_categories.append(
                    {
                        'code': db_category['code'],
                        'header': db_category['header']
                    }
                )
        return obsolete_categories

    def handle(self, *args, **options):
        en_thema_categories = json.loads(
            open(THEMA_JSON_EN).read(), encoding='utf-8'
        )["categories"]
        total = len(en_thema_categories)
        created = updated = 0
        self.stdout.write(
            self.style.MIGRATE_LABEL(
                'Importing Thema categories. This could take a while. '
                'Please be patient.'
            )
        )
        for thema_category in en_thema_categories:
            current_categories = ThemaCategory.objects.filter(
                code=thema_category[CODE_KEY_NAME]
            )
            try:
                parent = self._get_parent(thema_category[PARENT_KEY_NAME])
            except ThemaCategory.DoesNotExist:
                raise CommandError(
                    'ThemaCategory "{}" does not exist'.format(
                        thema_category[PARENT_KEY_NAME]
                    )
                )
            if current_categories.exists():
                current_categories.update(
                    header=thema_category[HEADING_KEY_NAME],
                    notes=thema_category[NOTES_KEY_NAME],
                    parent=parent
                )
                updated += 1
            else:
                ThemaCategory.objects.create(
                    code=thema_category[CODE_KEY_NAME],
                    header=thema_category[HEADING_KEY_NAME],
                    notes=thema_category[NOTES_KEY_NAME],
                    parent=parent
                )
                created += 1

            sys.stdout.write(
                "Progress: {}%   \r".format(
                    round(float(created+updated) / total * 100, 2)
                )
            )
            sys.stdout.flush()

        self.stdout.write(
            self.style.SUCCESS(
                '\nThe Thema Categories were imported successfully.'
            )
        )
        self.stdout.write(
            self.style.NOTICE(
                'Amount of categories created: {}'.format(created)
            )
        )
        self.stdout.write(
            self.style.NOTICE(
                'Amount of categories updated: {}'.format(updated)
            )
        )
        self.stdout.write(
            self.style.MIGRATE_LABEL(
                'Doing a reverse check to find obsolete categories...'
            )
        )
        obsolete_categories = self._get_obsolete_categories(
            en_thema_categories
        )
        if obsolete_categories:
            self.stdout.write(
                self.style.WARNING(
                    'There are some obsolete categories in the database, we '
                    'encourage you to remove these manually after dealing '
                    'with any possible references them.'
                )
            )
            for obsolete_category in obsolete_categories:
                self.stdout.write(self.style.NOTICE(str(obsolete_category)))
        else:
            self.stdout.write(
                self.style.NOTICE(
                    "The ThemaCategory table is clean and updated, "
                    "you don't have obsolete categories."
                )
            )
