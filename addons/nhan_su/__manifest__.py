{
    'name': 'Nhân Sự',
    'version': '1.0',
    'summary': 'Module quản lý dự án, công việc và chi phí',
    'description': 'Quản lý các dự án, giai đoạn, công việc và chi phí liên quan',
    'category': 'Project Management',
    'author': 'Your Name',
    'website': 'https://www.example.com',
    'depends': ['base'],
    'data': [
        
        'security/ir.model.access.csv',
        'views/nhan_vien.xml',
        'views/chuc_vu.xml',
        'views/lich_su_cong_tac.xml',
        'views/phong_ban.xml',
        'views/menu.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}