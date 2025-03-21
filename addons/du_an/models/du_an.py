from odoo import models, fields, api

class DuAn(models.Model):
    _name = 'du.an'
    _description = 'Dự Án'

    name = fields.Char(string="Tên dự án", required=True)
    ngay_bat_dau = fields.Date(string="Ngày bắt đầu")
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc")
    mo_ta = fields.Text(string="Mô tả")
    cong_viec_ids = fields.One2many('cong.viec', 'du_an_id', string='Công việc')
    thanh_vien_ids = fields.Many2many('nhan_vien', string='Thành viên')
    chi_phi_ids = fields.One2many('chi.phi', 'du_an_id', string='Chi phí')
    trang_thai = fields.Selection([
        ('new', 'Mới'),
        ('progress', 'Đang thực hiện'),
        ('done', 'Hoàn thành')
    ], default='new', string='Trạng thái')
    phan_tram_hoan_thanh = fields.Float(string="Phần trăm hoàn thành", compute='_compute_phan_tram_hoan_thanh', store=True)
    tong_chi_phi = fields.Float(compute='_compute_tong_chi_phi', string='Tổng chi phí', store=True)
    
    @api.depends('chi_phi_ids')
    def _compute_tong_chi_phi(self):
        for record in self:
            record.tong_chi_phi = sum(record.chi_phi_ids.mapped('so_tien'))
        pass

    @api.depends('cong_viec_ids')
    def _compute_phan_tram_hoan_thanh(self):
        for record in self:
            if record.cong_viec_ids:
                tong_cong_viec = len(record.cong_viec_ids) * 100
                so_cong_viec_hoan_thanh = sum(record.cong_viec_ids.mapped('phan_tram_hoan_thanh'))
                record.phan_tram_hoan_thanh = round(so_cong_viec_hoan_thanh / tong_cong_viec * 100, 2)
            else:
                record.phan_tram_hoan_thanh = 0