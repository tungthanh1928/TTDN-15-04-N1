from odoo import models, fields, api


class Student(models.Model):
    _name = 'student'
    _description = 'Quản lý sinh viên'
    _rec_name = 'display_name'

    display_name = fields.Char(
                        compute = "_compute_display_name",
                        store = True
                    )
    student_code = fields.Char("Mã sinh viên")
    student_class_id = fields.Many2one("student_class", string = "Lớp")
    student_cohort_id = fields.Many2one("student_cohort", 
                                            related = 'student_class_id.student_cohort_id', 
                                            store = True, 
                                            string = "Khóa"
                                        )
    full_name = fields.Char("Họ tên")
    phone_number = fields.Char("Số điện thoại")
    email = fields.Char("Email")
    sex = fields.Selection([
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ'),
    ], string='Giới tính')
    date_of_birth = fields.Date("Ngày sinh")
    status = fields.Selection([
        ('Đang học', 'Đang học'),
        ('Đã tốt nghiệp', 'Đã tốt nghiệp'),
    ], string='Trạng thái', default = 'Đang học')

    _sql_constraints = [
        ('student_code_uniq', 'unique (student_code)', """Mã sinh viên đã tồn tại"""),
    ]

    # display_name = fields.Char("Kỳ học", 
    #                            compute = "_compute_display_name",
    #                            store = True
    #                            )

    @api.depends(
        "student_code",
        "full_name",
    )
    def _compute_display_name(self):
        for record in self:
            if record.student_code and record.full_name:
                record.display_name = f'{record.full_name} ({record.student_code})'