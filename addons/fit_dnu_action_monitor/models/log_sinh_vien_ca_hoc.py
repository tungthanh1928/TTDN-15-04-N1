from odoo import models, fields, api


class LogSinhVienCaHoc(models.Model):
    _name = 'log_sinh_vien_ca_hoc'
    _description = 'Quản lý log sinh viên ca học'
    # _rec_name = 'display_name'
    # _order = 'number desc, class_name asc, full_name asc'

    thong_tin = fields.Char(string="Thông tin")
    student_id = fields.Char(string="Mã sinh viên")
    dia_chi_ip = fields.Char(string="Địa chỉ IP")
    thoi_gian_login = fields.Datetime(string="Thời gian Login")
    ca_hoc_id = fields.Many2one(
        comodel_name='ca_hoc',
        string='Ca Học',
        ondelete='cascade'
    )