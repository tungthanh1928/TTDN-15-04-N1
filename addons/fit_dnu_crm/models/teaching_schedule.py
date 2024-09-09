from odoo import models, fields, api


class TeachingSchedule(models.Model):
    _name = 'teaching_schedule'
    _description = 'Quản lý lịch giảng dạy'
    # _rec_name = 'display_name'
    _order = 'semester_id desc, student_cohort_id desc, student_class_id asc'

    # display_name = fields.Char(
    #                     compute = "_compute_display_name",
    #                     store = True
    #                 )
    
    student_class_id = fields.Many2one("student_class", string = "Lớp", ondelete = 'cascade', required = True)
    room = fields.Char("Phòng học")
    lecturer_ids = fields.Many2many("lecturer", relation= "teaching_schedule_lecturer", string = "Danh sách giảng viên")
    student_cohort_id = fields.Many2one(
                comodel_name='student_cohort',
                related = "student_class_id.student_cohort_id", 
                string = "Khóa",
                store = True,
                )
    semester_id = fields.Many2one("semester", string = "Kỳ học", ondelete = 'cascade', required = True)
    subject_id = fields.Many2one("subject", string = "Môn học", ondelete = 'cascade', required = True)
    subject_code = fields.Char("Mã môn học", related = 'subject_id.subject_code', store = True)
    subject_name = fields.Char("Tên môn học", related = 'subject_id.subject_name', store = True)
    # class_name = fields.Char("Tên lớp", related = 'student_class_id.class_name', store = True)
    number = fields.Integer("Khoá", related = 'student_cohort_id.number', store = True)

    
    teaching_session = fields.Selection([
        ('Sáng thứ 2', 'Sáng thứ 2'),
        ('Chiều thứ 2', 'Chiều thứ 2'),
        ('Sáng thứ 3', 'Sáng thứ 3'),
        ('Chiều thứ 3', 'Chiều thứ 3'),
        ('Sáng thứ 4', 'Sáng thứ 4'),
        ('Chiều thứ 4', 'Chiều thứ 4'),
        ('Sáng thứ 5', 'Sáng thứ 5'),
        ('Chiều thứ 5', 'Chiều thứ 5'),
        ('Sáng thứ 6', 'Sáng thứ 6'),
        ('Chiều thứ 6', 'Chiều thứ 6'),
        ('Sáng thứ 7', 'Sáng thứ 7'),
        ('Chiều thứ 7', 'Chiều thứ 7'),
    ], string='Buổi giảng dạy')


    _sql_constraints = [
        ('teaching_schedule_uniq', 'unique(student_class_id, semester_id, subject_id, teaching_session)', 'Đã tồn tại lịch giảng dạy'),
    ]