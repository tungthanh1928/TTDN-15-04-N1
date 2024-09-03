from odoo import models, fields, api
from odoo.exceptions import ValidationError

class UserAccount(models.Model):
    _name = 'user_account'
    _description = 'Quản lý người dùng'
    # _rec_name = 'display_name'
    # _order = 'uu_tien asc'
    
    user_name = fields.Char("Tên đăng nhập", required = True)
    full_name = fields.Char("Họ tên", required = True)
    role = fields.Selection([
        ('Admin', 'Admin'),
        ('User', 'User'),
    ], string='Vai trò', default = 'Admin')
    user_id = fields.Many2one('res.users', 'User')
    active_user = fields.Boolean('Kích hoạt')
    
    _sql_constraints = [
        ('user_name_uniq', 'unique(user_name)', 'Tên đăng nhập đã tồn tại'),
    ]
    
    def create_user(self):
        user_group = False
        users_res = self.env['res.users']
        for record in self:
            if not record.user_id:
                if not record.ma_dinh_danh:
                    raise ValidationError(_("Người dùng chưa có mã định danh"))
                password = "aisoftdigital"
                login = str(record.ma_dinh_danh)
                # if match is None:
                #     login = login.upper()
                user_id = users_res.create({
                    'name': record.name,
                    # 'partner_id': record.partner_id.id,
                    'login': login,
                    'password': password,
                    'groups_id': user_group,
                    # 'tz':
                    # self._context.get('tz'),
                })
                record.user_id = user_id
