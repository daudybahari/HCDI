# -*- coding: utf-8 -*-
{
    'name': 'training',

    'summary': 'Modul latihan Odoo 18',

    'description': '''
Modul sederhana untuk belajar Odoo 18.
''',

    'author': 'Nama Anda',

    'category': 'Training',

    'version': '18.0.1.0.0',

    'depends': ['base', 'mail'],

    'data': [
    'security/ir.model.access.csv',
    'views/menu_training.xml',
    'views/training_course.xml',
    'views/training_session.xml',
    'views/instruktur.xml',
    'views/wilayah.xml',
    'views/peserta.xml',
],


    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,

    'license': 'LGPL-3',
}