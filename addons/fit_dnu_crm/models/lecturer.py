from odoo import models, fields, api


class Lecturer(models.Model):
    _name = 'lecturer'
    _description = 'Quản lý giảng viên'
    _rec_name = 'display_name'
    
    display_name = fields.Char(
                        "Tên hiển thị",
                        compute = "_compute_display_name",
                        store = True
                    )
    lecturer_name = fields.Char("Tên giảng viên", require = True)
    hoc_ham_hoc_vi = fields.Selection([
        ('Cử nhân', 'Cử nhân'),
        ('Kỹ sư', 'Kỹ sư'),
        ('Thạc sĩ', 'Thạc sĩ'),
        ('Tiến sĩ', 'Tiến sĩ'),
        ('Phó Giáo sư', 'Phó Giáo sư'),
        ('Giáo sư', 'Giáo sư'),
    ], string='Học hàm/Học vị', default = 'Thạc sĩ')
    phone_number = fields.Char("Số điện thoại")
    email = fields.Char("Email")
    ch_tg = fields.Selection([
        ('CH', 'CH'),
        ('TG', 'TG'),
    ], string='CH/TG', default = 'CH')
    
    @api.depends(
        "lecturer_name",
        "hoc_ham_hoc_vi",
    )
    def _compute_display_name(self):
        for record in self:
            if record.lecturer_name and record.hoc_ham_hoc_vi:
                map_trinh_do = {
                    "Cử nhân": "CN",
                    "Kỹ sư": "KS",
                    "Thạc sĩ": "ThS",
                    "Tiến sĩ": "TS",
                    "Phó Giáo sư": "PGS.TS",
                    "Giáo sư": "GS.TS"
                }
                prefix = map_trinh_do.get(record.hoc_ham_hoc_vi)
                record.display_name = f'{prefix}. {record.lecturer_name}'