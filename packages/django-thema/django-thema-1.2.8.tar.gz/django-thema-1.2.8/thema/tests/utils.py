# -*- coding: utf-8 -*-
import os
from os import path
from shutil import rmtree
from os.path import join

TEMPORARY_TEST_DATA_DIR = join(
    path.dirname(path.realpath(__file__)),
    'test_data'
)


class ThemaTemporaryFilesMixin(object):
    """
    Mixin containing test data.

    Contains test data for a couple of categories:
    en, da, es header & notes, parent, related_categories.
    """
    random_codes = {
        'AMVD': {
            'en': (
                'City & town planning: architectural aspects',
                'See also: RPC Urban & municipal planning',
            ),
            'da': (
                'Byplanlægning: arkitektoniske aspekter',
                'Se også: RPC Byplanlægning og kommuneplanlægning'
            ),
            'es': (
                'Urbanismo: aspectos arquitectónicos',
                'Ver también: RPC Planificación urbana y municipal',
            ),
            'parent': 'AMV',
            'related_categories': ['RPC'],
        },
        'MBNH4': {
            'en': (
                'Birth control, contraception, family planning',
                '',
            ),
            'da': (
                'Prævention, fødselskontrol og familieplanlægning',
                '',
            ),
            'es': (
                'Control de la natalidad, anticoncepción y '
                'planificación familiar',
                '',
            ),
            'parent': 'MBNH',
            'related_categories': [],
        },
        'PBB': {
            'en': ('Philosophy of mathematics', ''),
            'da': ('Matematikkens filosofi', ''),
            'es': ('Filosofía de las matemáticas', ''),
            'parent': 'PB',
            'related_categories': [],

        },
        'RGBR': {
            'en': ('Coral reefs', ''),
            'da': ('Koralrev', ''),
            'es': ('Arrecifes de coral', ''),
            'parent': 'RGB',
            'related_categories': [],
        },
        'VXQM': {
            'en': (
                'Monsters & legendary beings',
                'See also: JBGB Folklore, myths & legends'
            ),
            'da': (
                'Monstre og mytiske væsner',
                'Se også: JBGB Folklore, myter og legender'
            ),
            'es': (
                'Monstruos y seres legendarios',
                'Ver también: JBGB Folclore, mitos y leyendas'
            ),
            'parent': 'VXQ',
            'related_categories': ['JBGB'],
        },
        'MBX': {
            'en': (
                'History of medicine',
                'See also: NHTF History: plagues, diseases etc'),
            'da': (
                'Medicinsk historie',
                'Her: lægevidenskabens historie.'
                ' Se også: NHTF Historie: Pest og epidemiske sygdomme'),
            'es': (
                'Historia de la medicina',
                'Ver también: NHTF Historia: plagas, enfermedades, etc.'),
            'parent': 'MB',
            'related_categories': ['NHTF'],
        }
    }

    def setUp(self):
        """Create a temporary location for testing files."""
        if not path.exists(TEMPORARY_TEST_DATA_DIR):
            os.makedirs(TEMPORARY_TEST_DATA_DIR)

    def tearDown(self):
        """Remove the temporary test location and all its content."""
        rmtree(TEMPORARY_TEST_DATA_DIR)
