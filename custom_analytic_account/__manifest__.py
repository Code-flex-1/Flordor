# -*- coding: utf-8 -*-
{
    'name': "Customer Analytic Account",

    'summary': """
  display customer related analytic account 
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
    'depends': ['base', 'sale','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_payment.xml',
        'wizards/account_payment_register_views.xml',
    ],

}
