from odoo import models, fields, api


class StudentClass(models.Model):
    _name = 'student_class'
    _description = 'Quản lý lớp'
    _rec_name = 'class_name'
    _order = 'number desc, class_name asc'

    class_name = fields.Char("Tên lớp", required = True)
    student_cohort_id = fields.Many2one("student_cohort", string = "Khóa", required = True)
    number = fields.Integer("Khóa", related='student_cohort_id.number', store = True)
    student_ids = fields.One2many("student", inverse_name="student_class_id", string = "Danh sách sinh viên")
    number_students = fields.Integer("Số lượng SV", 
                        compute='compute_number_students', 
                        store = True
                    )

    _sql_constraints = [
        ('class_name_uniq', 'unique (class_name)', """Tên lớp đã tồn tại"""),
    ]

    @api.depends("student_ids")
    def compute_number_students(self):
        for record in self:
            record.number_students = len(record.student_ids)