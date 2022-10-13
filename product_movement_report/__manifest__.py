# -*- coding: utf-8 -*-
{
    'name': "Product Moves Report",

    'summary': """
Product Moves Report
        """,

    'description': """
    
    """,

    'author': "Code Flex",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
'license':'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/product_move_report_wizard.xml',
        'reports/product_move_report.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            "product_movement_report/static/src/css/*"
        ],
    },

}
