from odoo import models, fields

class GiaiDoan(models.Model):
    _name = 'giai.doan'
    _description = 'Giai đoạn dự án'

    name = fields.Char('Tên giai đoạn', required=True)
    du_an_id = fields.Many2one('du.an', string='Dự án', required=True)
    cong_viec_ids = fields.One2many('cong.viec', 'giai_doan_id', string='Công việc')
    chi_phi_ids = fields.One2many('chi.phi', 'giai_doan_id', string='Chi phí')
    ngay_bat_dau = fields.Date('Ngày bắt đầu')
    ngay_ket_thuc = fields.Date('Ngày kết thúc')