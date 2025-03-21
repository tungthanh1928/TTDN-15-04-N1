from datetime import date
from odoo import models, fields, api

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_va_ten'

    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    nam_sinh = fields.Date("Năm sinh")
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    ho_ten_dem = fields.Char("Họ tên đệm", required=True)
    ten = fields.Char("Tên", required=True)
    ho_va_ten = fields.Char("Họ và tên", compute='_compute_ho_va_ten', store=True)
    tuoi = fields.Integer("Tuổi", compute="_compute_tuoi", store=True)

    lich_su_cong_tac_ids = fields.One2many("lich_su_cong_tac", "nhan_vien_id", string="Danh sách lịch sử công tác")
    phong_ban_id = fields.Many2one("phong_ban", string="Phòng ban")
    cong_viec_ids = fields.Many2many('cong.viec', string='Công việc tham gia')  # Kết nối với công việc

    @api.depends("ho_ten_dem", "ten")
    def _compute_ho_va_ten(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                record.ho_va_ten = f"{record.ho_ten_dem} {record.ten}"
            else:
                record.ho_va_ten = ""

    @api.depends("nam_sinh")
    def _compute_tuoi(self):
        today = date.today()
        for record in self:
            if record.nam_sinh:
                age = today.year - record.nam_sinh.year
                if (today.month, today.day) < (record.nam_sinh.month, record.nam_sinh.day):
                    age -= 1
                record.tuoi = age
            else:
                record.tuoi = 0