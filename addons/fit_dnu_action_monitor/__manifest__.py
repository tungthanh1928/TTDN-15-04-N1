# -*- coding: utf-8 -*-
{
    'name': "FIT-DNU-ACTION-MONITOR",

    'summary': """
        Giám sát hành động
    """,

    'description': """
        Module Giám sát hành động
    """,

    'author': "FIT-DNU",
    'website': "https://fitdnu.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    # 'category': 'Website',
    'version': '1.0',
    'images': [
        'static/src/img/core.png',
    ],

    # any module necessary for this one to work correctly
    'depends': ['base', 'fit_dnu_crm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/student_log_action.xml',
        'views/core_menu_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True
}
