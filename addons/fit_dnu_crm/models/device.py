from odoo import models, fields, api


class Device(models.Model):
    _name = 'device'
    _description = 'Quản lý thiết bị'
    _rec_name = 'device_code'
    _order = 'device_code asc'
    
    device_code = fields.Char("Mã thiết bị", require = True)
    device_name = fields.Char("Tên thiết bị", require = True)
    quantity = fields.Integer("Số lượng")
    status = fields.Selection([
        ('Mới', 'Mới'),
        ('Còn tốt', 'Còn tốt'),
        ('Hỏng', 'Hỏng')
    ], string='Trạng thái')
    
