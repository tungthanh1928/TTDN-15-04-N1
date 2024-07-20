from odoo import models, fields, api


class StudentCohort(models.Model):
    _name = 'student_cohort'
    _description = 'Quản lý khóa sinh viên'
    _rec_name = 'number'

    number = fields.Integer("Khóa", required = True)
    color_code = fields.Char("Màu hiển thị", default = '#f37423')
    student_classes = fields.One2many("student_class", inverse_name="student_cohort_id", string = "Danh sách lớp")

    _sql_constraints = [
        ('number_uniq', 'unique (number)', """Khóa đã tồn tại"""),
    ]