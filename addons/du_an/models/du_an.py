from odoo import models, fields, api

class DuAn(models.Model):
    _name = 'du.an'
    _description = 'Dự Án'

    name = fields.Char(string="Tên dự án", required=True)
    ngay_bat_dau = fields.Date(string="Ngày bắt đầu")
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc")
    mo_ta = fields.Text(string="Mô tả")
    cong_viec_ids = fields.One2many('cong.viec', 'du_an_id', string='Công việc')
    tong_chi_phi = fields.Float(string="Tổng chi phí")
    thanh_vien_ids = fields.Many2many('nhan_vien', string='Thành viên')
    chi_phi_ids = fields.One2many('chi.phi', 'du_an_id', string='Chi phí')
    trang_thai = fields.Selection([
        ('new', 'Mới'),
        ('progress', 'Đang thực hiện'),
        ('done', 'Hoàn thành')
    ], default='new', string='Trạng thái')
    phan_tram_hoan_thanh = fields.Float(string="Phần trăm hoàn thành", compute='_compute_phan_tram_hoan_thanh')
    @api.depends('cong_viec_ids')
    def _compute_phan_tram_hoan_thanh(self):
        for record in self:
            if record.cong_viec_ids:
                tong_cong_viec = len(record.cong_viec_ids)
                so_cong_viec_hoan_thanh = len(record.cong_viec_ids.filtered(lambda x: x.trang_thai == 'done'))
                record.phan_tram_hoan_thanh = so_cong_viec_hoan_thanh / tong_cong_viec * 100
            else:
                record.phan_tram_hoan_thanh = 0