from odoo import models, fields, api

class ChiPhi(models.Model):
    _name = 'chi.phi'
    _description = 'Chi phí'

    name = fields.Char('Tên chi phí', required=True)
    so_tien = fields.Float('Số tiền', required=True, default=0)
    ngay_chi = fields.Date('Ngày chi', default=fields.Date.today())
    du_an_id = fields.Many2one('du.an', string='Dự án')
    mo_ta = fields.Text('Mô tả chi phí')