# -*- coding: utf-8 -*-
{
    'name': "om_odoo_inheritance",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','sale'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}

