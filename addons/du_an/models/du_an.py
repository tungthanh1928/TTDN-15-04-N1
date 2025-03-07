from odoo import models, fields, api

class DuAn(models.Model):
    _name = 'du.an'
    _description = 'Dự án'

    name = fields.Char('Tên dự án', required=True)
    mo_ta = fields.Text('Mô tả dự án')
    ngay_bat_dau = fields.Date('Ngày bắt đầu')
    ngay_ket_thuc = fields.Date('Ngày kết thúc')
    thanh_vien_ids = fields.Many2many('thanh.vien', string='Thành viên tham gia')
    cong_viec_ids = fields.One2many('cong.viec', 'du_an_id', string='Công việc')
    tong_chi_phi = fields.Float('Tổng chi phí', compute='_compute_tong_chi_phi', store=True)

    @api.depends('cong_viec_ids.so_tien')  # Đảm bảo rằng trường này tồn tại
    def _compute_tong_chi_phi(self):
        for record in self:
            total = sum(cong_viec.so_tien for cong_viec in record.cong_viec_ids)
            record.tong_chi_phi = total