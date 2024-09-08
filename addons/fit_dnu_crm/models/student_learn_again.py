from odoo import models, fields, api


class StudentLearnAgain(models.Model):
    _name = 'student_learn_again'
    _description = 'Quản lý học lại'
    # _rec_name = 'display_name'
    # _order = 'display_name desc'

    student_id = fields.Many2one("student", string = "Sinh viên", ondelete = 'cascade', required = True)
    student_code = fields.Char(related = 'student_id.student_code', string = "Mã sinh viên", store = True)
    full_name = fields.Char(related = 'student_id.full_name', string = "Họ tên", store = True)
    subject_id = fields.Many2one("subject", string = "Môn học", ondelete = 'cascade', required = True)
    subject_code = fields.Char(related = 'subject_id.subject_code', string = "Mã môn học", store = True)
    subject_name = fields.Char("Tên môn học", related = 'subject_id.subject_name', store = True)
    _sql_constraints = [
        ('subject_id_student_id_uniq', 'unique (student_id,subject_id)', """Môn học lại của sinh viên đã tồn tại"""),
    ]
