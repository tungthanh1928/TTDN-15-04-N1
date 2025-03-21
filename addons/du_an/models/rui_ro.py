from odoo import models, fields, api

class RuiRo(models.Model):
    _name = 'rui_ro'
    _description = 'Quản lý Rủi ro'

    name = fields.Char(string='Tên Rủi ro', required=True)
    description = fields.Text(string='Mô tả')
    project_id = fields.Many2one('du.an', string='Dự án', required=True)  # Sửa lại để liên kết với dự án
    risk_level = fields.Selection([
        ('low', 'Thấp'),
        ('medium', 'Trung Bình'),
        ('high', 'Cao'),
    ], string='Mức độ Rủi ro', required=True)
    likelihood = fields.Selection([
        ('low', 'Thấp'),
        ('medium', 'Trung Bình'),
        ('high', 'Cao'),
    ], string='Khả năng xảy ra', required=True)
    impact = fields.Selection([
        ('low', 'Thấp'),
        ('medium', 'Trung Bình'),
        ('high', 'Cao'),
    ], string='Tác động', required=True)
    response_plan = fields.Text(string='Kế hoạch ứng phó')
    status = fields.Selection([
        ('identified', 'Đã xác định'),
        ('monitored', 'Đang theo dõi'),
        ('resolved', 'Đã giải quyết'),
    ], string='Trạng thái', default='identified')