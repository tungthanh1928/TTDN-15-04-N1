from odoo import models, fields, api


class StudentSubjectAbsent(models.Model):
    _name = 'student_subject_absent'
    _description = 'Quản lý sinh viên vắng theo môn học'
    _order = 'semester_id desc, class_name asc, percent_absent asc'

    student_id = fields.Many2one("student", string = "Sinh viên", ondelete = 'cascade', required = True)
    student_code = fields.Char(related = 'student_id.student_code', string = "Mã sinh viên")
    full_name = fields.Char(related = 'student_id.full_name', string = "Họ tên")
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
    semester_id = fields.Many2one("semester", string = "Kỳ học", ondelete = 'cascade', required = True)
    subject_id = fields.Many2one("subject", string = "Môn học", ondelete = 'cascade', required = True)
    class_name = fields.Char("Tên lớp", related = 'student_class_id.class_name', store = True)
    number = fields.Integer("Khoá", related = 'student_cohort_id.number', store = True)
    
    student_absent_ids = fields.One2many("student_absent", 
                                            inverse_name="student_subject_absent_id", 
                                            string = "Danh sách vắng")
    
    total_lesson_absent = fields.Integer("Tổng số tiết vắng",
                                    compute = "_compute_total_lesson_absent",
                                    store = True
                                )
    total_lessons = fields.Integer("Tổng số tiết học",
                                        related = "subject_id.total_lessons",
                                        store = True
                                        )
    percent_absent = fields.Float("Phần trăm vắng",
                                    compute = "_compute_percent_absent",
                                    store = True
                                )
    
    number_study_credits = fields.Integer(related = 'subject_id.number_study_credits', string = "Số tín chỉ")
    
    # range_absent = fields.Selection([
    #     ('5%', '5%'),
    #     ('10%', '10%'),
    #     ('15%', '15%'),
    #     ('20%', '20%'),
    # ], string='Mức độ vắng', 
    #     compute = "_compute_range_absent", 
    #     # store = True
    # )

    _sql_constraints = [
        ('student_subject_semester_uniq', 'unique(student_id, semester_id, subject_id)', 'Đã tồn tại bản ghi sinh viên + môn học + kỳ học'),
    ]

    
    @api.depends(
        "student_absent_ids",
        "student_absent_ids.number_lesson_absent",
    )
    def _compute_total_lesson_absent(self):
        for record in self:
            total = 0
            for stu_absent in record.student_absent_ids:
                total += stu_absent.number_lesson_absent 
            record.total_lesson_absent = total

    @api.depends(
        "total_lesson_absent",
        "total_lessons",
    )
    def _compute_percent_absent(self):
        for record in self:
            if record.total_lesson_absent and record.total_lessons and record.total_lessons != 0:
                record.percent_absent = round(record.total_lesson_absent/record.total_lessons, 2) * 100
    
    # @api.depends(
    #     "percent_absent",
    # )
    # def _compute_range_absent(self):
    #     for record in self:
    #         if record.percent_absent and record.percent_absent > 0:
    #             if record.percent_absent >= 20:
    #                 record.range_absent = '20%'
    #             elif record.percent_absent >= 15:
    #                 record.range_absent = '15%'
    #             elif record.percent_absent >= 10:
    #                 record.range_absent = '10%'
    #             else:
    #                 record.range_absent = '5%'
                
    def compute_percent_absent_all(self):
        for record in self:
            student_subject_absent = self.env["student_subject_absent"].search([])
            for vl in student_subject_absent:
                vl._compute_percent_absent()