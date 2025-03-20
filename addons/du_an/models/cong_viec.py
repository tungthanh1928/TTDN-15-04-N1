from odoo import models, fields, api

class CongViec(models.Model):
    _name = 'cong.viec'
    _description = 'Công việc'

    name = fields.Char('Tên công việc', required=True)
    mo_ta = fields.Text('Mô tả công việc')
    du_an_id = fields.Many2many('du.an', string='Dự án' )
    thanh_vien_ids = fields.Many2many('nhan_vien', string='Thành viên')
    phan_tram_hoan_thanh = fields.Float('Phần trăm hoàn thành', compute='_compute_phan_tram_hoan_thanh', store=True, readonly=False)
    trang_thai = fields.Selection([
        ('not_started', 'Chưa bắt đầu'),
        ('in_progress', 'Đang thực hiện'),
        ('done', 'Hoàn thành')
    ], default='not_started', string='Trạng thái')
    uu_tien = fields.Selection([
        ('high', 'Cao'),
        ('medium', 'Trung bình'),
        ('low', 'Thấp')
    ], default='medium', string='Ưu tiên')
    thoi_gian_du_kien = fields.Float('Thời gian dự kiến (giờ)')
    thoi_gian_thuc_te = fields.Float('Thời gian thực tế (giờ)', compute='_compute_thoi_gian_thuc_te', store=True)
    deadline = fields.Date('Hạn hoàn thành')

    @api.depends('trang_thai')
    def _compute_phan_tram_hoan_thanh(self):
        for record in self:
            if record.trang_thai == 'not_started':
                record.phan_tram_hoan_thanh = 0  # Chưa bắt đầu: 0%
            elif record.trang_thai == 'done':
                record.phan_tram_hoan_thanh = 100  # Hoàn thành: 100%
            # Khi trạng thái là "Đang thực hiện", phần trăm hoàn thành do người dùng tự nhập (không thay đổi)

    @api.depends('thoi_gian_du_kien', 'thoi_gian_thuc_te')
    def _compute_thoi_gian_thuc_te(self):
        for record in self:
            # Tính toán thời gian thực tế (giả định rằng nó được cập nhật khi công việc hoàn thành)
            record.thoi_gian_thuc_te = record.thoi_gian_du_kien if record.trang_thai == 'done' else 0
    