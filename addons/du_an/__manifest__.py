{
    'name': 'Quản lý dự án',
    'version': '1.0',
    'summary': 'Module quản lý dự án, công việc và chi phí',
    'description': 'Quản lý các dự án, giai đoạn, công việc và chi phí liên quan',
    'category': 'Project Management',
    'author': 'Your Name',
    'website': 'https://www.example.com',
    'depends': ['base'],
    'data': [
        
        'security/ir.model.access.csv',
        'views/du_an_views.xml',
        'views/giai_doan_views.xml',
        'views/cong_viec_views.xml',
        'views/chi_phi_views.xml',
        'views/thanh_vien_views.xml',
        'views/menu.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}