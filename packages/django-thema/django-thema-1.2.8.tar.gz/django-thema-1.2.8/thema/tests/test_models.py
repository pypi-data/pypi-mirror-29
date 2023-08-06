from django.core.exceptions import FieldDoesNotExist
from django.test import (
    TestCase,
    override_settings,
)

from thema.models import ThemaCategory


class TestThemaCategory(TestCase):

    fields_to_check = [
        'code', 'parent', 'header',
    ]

    def test_all_field_exist(self):
        for field in self.fields_to_check:
            try:
                ThemaCategory._meta.get_field(field)
            except FieldDoesNotExist:
                self.fail("The field '{}' doesn't exist")

    def test_create_instance(self):
        code = 'AVL'
        header = 'Music: styles & genres'
        # Thema without parent.
        thema = ThemaCategory.objects.create(code=code, header=header)
        self.assertIsNone(thema.parent)
        self.assertEqual(thema.code, code)
        self.assertEqual(thema.header, header)
        self.assertEqual(str(thema), 'AVL')
        # Thema with parent
        thema_child_code = 'AVLP'
        thema_child_header = 'Popular music'
        thema_child_notes = 'Use with music'
        thema_child = ThemaCategory.objects.create(
            code=thema_child_code,
            header=thema_child_header,
            parent=thema,
            notes=thema_child_notes,
        )
        self.assertEqual(thema_child.parent, thema)
        self.assertEqual(thema_child.code, thema_child_code)
        self.assertEqual(thema_child.header, thema_child_header)
        self.assertEqual(thema_child.notes, thema_child_notes)
        self.assertEqual(str(thema_child), 'AVLP')

    @override_settings(LANGUAGE_CODE='da', LANGUAGES=(('da', 'Danish'),))
    def test_local_header(self):
        thema = ThemaCategory.objects.create(
            code='AVL', header='Music: styles & genres'
        )
        self.assertIsNone(thema.parent)
        self.assertEqual(thema.local_header, 'Musikgenrer')

    @override_settings(LANGUAGE_CODE='da', LANGUAGES=(('da', 'Danish'),))
    def test_local_notes(self):
        thema = ThemaCategory.objects.create(
            code='code',
            header='Music: styles & genres',
            notes='With AVL* codes, ALWAYS assign STYLE Qualifier(s)'
                  ' as appropriate'
        )
        self.assertEqual(
            thema.local_notes,
            'Ved brug af AVL*-koder tildeles ALTID kvalifikator(er)'
            ' for stilarter'
        )
