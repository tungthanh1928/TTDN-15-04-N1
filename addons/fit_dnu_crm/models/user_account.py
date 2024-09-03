from odoo import models, fields, api
from odoo.exceptions import ValidationError

class UserAccount(models.Model):
    _name = 'user_account'
    _description = 'Quản lý người dùng'
    _rec_name = 'username'
    # _order = 'uu_tien asc'
    
    username = fields.Char("Tên đăng nhập", required = True)
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
                if not record.username:
                    raise ValidationError(_("Người dùng chưa có username"))
                password = "fitdnu@123"
                login = str(record.username)
                # if match is None:
                #     login = login.upper()
                user_id = users_res.create({
                    'name': record.full_name,
                    # 'partner_id': record.partner_id.id,
                    'login': login,
                    'password': password,
                    'groups_id': user_group,
                    # 'tz':
                    # self._context.get('tz'),
                })
                if user_id:
                    record.user_id = user_id
                    record.active_user = True
    
    def unlink(self):
        for record in self:
            if record.user_id:
                user = self.env['res.users'].search([('id', '=', record.user_id.id)]).unlink()
        result = super(UserAccount, self).unlink()
        return result
    
    # @api.model
    # def write(self, vals):
    #     check = False
    #     if 'username' in vals:
    #         check = True        
    #     result = super(UserAccount, self).write(vals)
    #     if check == True:
    #         for record in self:
    #             record.user_id.login = record.username
    #     return result