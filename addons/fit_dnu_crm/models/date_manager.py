from odoo import models, fields, api


class DateManager(models.Model):
    _name = 'date_manager'
    _description = 'Quản lý ngày'
    
    date = fields.Date("Ngày", required = True)

    _sql_constraints = [
        ('date_uniq', 'unique(date)', 'Đã tồn tại bản ghi ngày'),
    ]