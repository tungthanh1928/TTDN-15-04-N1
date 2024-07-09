from odoo import models, fields, api


class StudentClass(models.Model):
    _name = 'student_class'
    _description = 'Quản lý lớp'
    _rec_name = 'class_name'

    class_name = fields.Char("Tên lớp", required = True)
    student_cohort_id = fields.Many2one("student_cohort", string = "Khóa", required = True)

    _sql_constraints = [
        ('class_name_uniq', 'unique (class_name)', """Tên lớp đã tồn tại"""),
    ]