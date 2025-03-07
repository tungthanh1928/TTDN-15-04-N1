from odoo import models, fields, api  # Thêm api ở đây

class CongViec(models.Model):
    _name = 'cong.viec'
    _description = 'Công việc'
    du_an_id = fields.Many2one('du.an', string='Dự án')  # Liên kết với dự án
    name = fields.Char('Tên công việc', required=True)
    mo_ta = fields.Text('Mô tả công việc')
    nguoi_phu_trach = fields.Many2one('thanh.vien', string='Người phụ trách', ondelete='set null')
    trang_thai = fields.Selection([
        ('new', 'Mới'),
        ('progress', 'Đang thực hiện'),
        ('done', 'Hoàn thành')
    ], default='new', string='Trạng thái')

    @api.onchange( 'nguoi_phu_trach')
    def _onchange_fields(self):
        
        if not self.nguoi_phu_trach:
            return {'warning': {'title': 'Warning', 'message': 'Người phụ trách không hợp lệ.'}}
    so_tien = fields.Float('Chi phí', required=True)