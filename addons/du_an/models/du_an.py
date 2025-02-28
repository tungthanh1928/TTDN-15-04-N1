from odoo import models, fields, api

class DuAn(models.Model):
    _name = 'du.an'
    _description = 'Dự án'

    name = fields.Char('Tên dự án', required=True)
    mo_ta = fields.Text('Mô tả dự án')
    ngay_bat_dau = fields.Date('Ngày bắt đầu')
    ngay_ket_thuc = fields.Date('Ngày kết thúc')
    giai_doan_ids = fields.One2many('giai.doan', 'du_an_id', string='Các giai đoạn')
    thanh_vien_ids = fields.Many2many('thanh.vien', string='Thành viên tham gia')
    tong_chi_phi = fields.Float('Tổng chi phí', compute='_compute_tong_chi_phi')

    @api.depends('giai_doan_ids.chi_phi_ids.so_tien')
    def _compute_tong_chi_phi(self):
        for record in self:
            total = 0
            for giai_doan in record.giai_doan_ids:
                total += sum(chi_phi.so_tien for chi_phi in giai_doan.chi_phi_ids)
            record.tong_chi_phi = total