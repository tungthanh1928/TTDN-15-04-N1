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
        ('male', 'Nam'),
        ('female', 'Nữ'),
    ], string='Giới tính')
    date_of_birth = fields.Date("Ngày sinh")
    status = fields.Selection([
        ('Đang học', 'Đang học'),
        ('Đã tốt nghiệp', 'Đã tốt nghiệp'),
    ], string='Trạng thái', default = 'Đang học')
    dia_chi_tt = fields.Char("Địa chỉ TT")
    ho_va_ten_cha = fields.Char("Họ và tên cha")
    so_dien_thoai_cha = fields.Char("Số điện thoại cha")
    ho_va_ten_me = fields.Char("Họ và tên mẹ")
    so_dien_thoai_me = fields.Char("Số điện thoại mẹ")
    
    _sql_constraints = [
        ('student_code_uniq', 'unique (student_code)', """Mã sinh viên đã tồn tại"""),
    ]

    # display_name = fields.Char("Kỳ học", 
    #                            compute = "_compute_display_name",
    #                            store = True
    #                            )

    # @api.model    
    # def get_student_by_list_id(self, list_id):
    #     result = self.env['student'].browse(list_id)
    #     list_result = []
    #     if len(result) > 0:
    #         for stu in result:
    #             list_result.append({
    #                 "id": stu.id,
    #                 'student_code': stu.student_code,
    #                 'full_name': stu.full_name,
    #                 'student_class_id': stu.student_class_id,
    #                 'phone_number': stu.phone_number,
    #                 'email': stu.email,
    #                 'sex': stu.sex,
    #                 'date_of_birth': stu.date_of_birth,
    #                 'status': stu.status,
    #             })
    #     print("???", list_result)
    #     return list_result

    
    @api.depends(
        "student_code",
        "full_name",
    )
    def _compute_display_name(self):
        for record in self:
            if record.student_code and record.full_name:
                record.display_name = f'{record.full_name} ({record.student_code})'
    
    