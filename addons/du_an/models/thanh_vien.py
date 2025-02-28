from odoo import models, fields

class ThanhVien(models.Model):
    _name = 'thanh.vien'
    _description = 'Thành viên'

    name = fields.Char('Họ tên', required=True)
    chuc_vu = fields.Char('Chức vụ')
    email = fields.Char('Email')
    so_dien_thoai = fields.Char('Số điện thoại')
    du_an_ids = fields.Many2many('du.an', string='Dự án tham gia')