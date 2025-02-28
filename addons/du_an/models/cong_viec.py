from odoo import models, fields

class CongViec(models.Model):
    _name = 'cong.viec'
    _description = 'Công việc'

    name = fields.Char('Tên công việc', required=True)
    mo_ta = fields.Text('Mô tả công việc')
    giai_doan_id = fields.Many2one('giai.doan', string='Giai đoạn', required=True)
    nguoi_phu_trach = fields.Many2one('thanh.vien', string='Người phụ trách')
    trang_thai = fields.Selection([
        ('new', 'Mới'),
        ('progress', 'Đang thực hiện'),
        ('done', 'Hoàn thành')
    ], default='new', string='Trạng thái')