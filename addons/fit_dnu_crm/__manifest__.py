# -*- coding: utf-8 -*-
{
    'name': "FIT-DNU-CSSV",

    'summary': """
        Quản lý thông tin chung
    """,

    'description': """
        Module quản lý thông tin chung
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
    'depends': ['base', 'board'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/school_year.xml',
        'views/semester.xml',
        'views/student_cohort.xml',
        'views/student_class.xml',
        'views/student.xml',
        'views/lecturer.xml',
        # 'views/date_manager.xml',
        'views/teaching_schedule.xml',
        'views/student_absent.xml',
        'views/student_tuition_fee.xml',
        'views/dashboard.xml',
        'views/student_class_absent.xml',
        'views/student_subject_absent.xml',
        'views/student_class_tuition_fee.xml',
        'views/custom_noti.xml',
        'views/subject.xml',
        'views/import/import_student_absent.xml',
        'views/import/import_student_tuition_fee.xml',
        'views/user_account.xml',
        'views/core_menu_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        # 'mail.assets_discuss_public': [
        #     'hr/static/src/models/*/*.js',
        # ],
        'web.assets_backend': [
            'fit_dnu_crm/static/src/js/import_button.js',
        ],
        'web.assets_qweb': [
            'fit_dnu_crm/static/src/xml/import_excel_button.xml',
        ],
    },
    'installable': True,
    'application': True
}
