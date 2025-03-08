from odoo import models, fields, api

class CongViec(models.Model):
    _name = 'cong.viec'
    _description = 'Công việc'

    name = fields.Char('Tên công việc', required=True)
    mo_ta = fields.Text('Mô tả công việc')
    du_an_id = fields.Many2many('du.an', string='Dự án')
    tong_so_nguoi_tham_gia = fields.Integer('Tổng số người tham gia', compute='_compute_tong_so_nguoi_tham_gia')
    tong_so_du_an = fields.Integer('Tổng số dự án ', compute='_compute_tong_so_du_an')
    trang_thai = fields.Selection([
        ('new', 'Mới'),
        ('progress', 'Đang thực hiện'),
        ('done', 'Hoàn thành')
    ], default='new', string='Trạng thái')

    @api.depends('du_an_id')
    def _compute_tong_so_nguoi_tham_gia(self):
        for record in self:
            record.tong_so_nguoi_tham_gia = len(record.du_an_id.thanh_vien_ids)

    @api.depends('du_an_id')
    def _compute_tong_so_du_an(self):
        for record in self:
            record.tong_so_du_an = len(record.du_an_id)
    thanh_vien_ids = fields.Many2many('nhan_vien', string='Thành viên')