from odoo import models, fields, api


class StudentLogAction(models.Model):
    _name = 'student_log_action'
    _description = 'Quản lý hành động sinh viên'
    _rec_name = 'student_id'

    student_id = fields.Many2one("student", string = "Mã sinh viên", ondelete = 'cascade', required = True)
    student_code = fields.Char(related = 'student_id.student_code', string = "Mã sinh viên", store = True)
    full_name = fields.Char(related = 'student_id.full_name', string = "Họ tên", store = True)
    student_class_id = fields.Many2one(
                comodel_name='student_class',
                related = "student_id.student_class_id", 
                string = "Lớp",
                store = True,
            )
    student_cohort_id = fields.Many2one(
                comodel_name='student_cohort',
                related = "student_id.student_cohort_id", 
                string = "Khóa",
                store = True,
                )

