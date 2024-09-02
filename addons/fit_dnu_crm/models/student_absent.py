from odoo import models, fields, api


class StudentAbsent(models.Model):
    _name = 'student_absent'
    _description = 'Quản lý sinh viên vắng'
    _rec_name = 'student_id'
    _order = 'date_absent desc, student_class_id asc, student_code asc'

    # display_name = fields.Char(
    #                     compute = "_compute_display_name",
    #                     store = True
    #                 )
    student_id = fields.Many2one("student", string = "Sinh viên", ondelete = 'cascade', required = True)
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
    semester_id = fields.Many2one("semester", string = "Kỳ học", ondelete = 'cascade', required = True)
    subject_id = fields.Many2one("subject", string = "Môn học", ondelete = 'cascade', required = True)
    subject_code = fields.Char(related = 'subject_id.subject_code', string = "Mã môn học")
    number_lesson_absent = fields.Integer("Số tiết học vắng mặt", default = 4, required = True)
    date_absent = fields.Date("Ngày vắng", required = True)
    reason = fields.Char("Lý do")
    day = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
    ], string='Ngày', compute = "_compute_day_month_year", store = True)

    month = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
    ], string='Tháng', compute = "_compute_day_month_year", store = True)

    year = fields.Selection([
        ('2023', '2023'),
        ('2024', '2024'),
        ('2025', '2025'),
        ('2026', '2026'),
        ('2027', '2027'),
        ('2028', '2028'),
        ('2029', '2029'),
        ('2030', '2030'),
        ('2031', '2031'),
        ('2032', '2032'),
        ('2033', '2033'),
        ('2034', '2034'),
    ], string='Năm', compute = "_compute_day_month_year", store = True)

    student_class_absent_id = fields.Many2one("student_class_absent", 
                            string = "Lớp - SV vắng",
                            compute = "_compute_student_class_absent_id",
                            store = True,
                        )
    student_subject_absent_id = fields.Many2one("student_subject_absent", 
                            string = "Môn học - SV vắng",
                            compute = "_compute_student_subject_absent_id",
                            store = True,
                        )
    teaching_schedule_id = fields.Many2one("teaching_schedule", 
                            string = "Lịch giảng dạy",
                            compute = "_compute_teaching_schedule_id",
                            store = True,
                        )
    lecturer_ids = fields.Many2many(
                        "lecturer",
                        related = 'teaching_schedule_id.lecturer_ids',
                        relation= "student_absent_lecturer", 
                        string = "Danh sách giảng viên",
                        store = True
                    )


    _sql_constraints = [
        ('student_day_absent_semester_subject_uniq', 'unique(student_id, date_absent, semester_id, subject_id)', 'Đã tồn tại bản ghi sinh viên, môn học với ngày vắng này'),
    ]


    @api.depends(
        "date_absent",
    )
    def _compute_day_month_year(self):
        for record in self:
            if record.date_absent:
                record.day = str(record.date_absent.day)
                record.month = str(record.date_absent.month)
                record.year = str(record.date_absent.year)

    @api.depends(
        "semester_id",
        "student_id",
        "subject_id"
    )
    def _compute_student_subject_absent_id(self):
        for record in self:
            if record.semester_id and record.student_id and record.subject_id:
                stu_subject_abs = self.env["student_subject_absent"].search([
                    ('student_id','=', record.student_id.id),
                    ('semester_id', '=', record.semester_id.id),
                    ('subject_id', '=', record.subject_id.id)
                ])
                if len(stu_subject_abs) > 0:
                    record.student_subject_absent_id = stu_subject_abs.id
                else:
                    data_cre = self.env["student_subject_absent"].create({
                        'student_id': record.student_id.id,
                        'subject_id': record.subject_id.id,
                        'semester_id': record.semester_id.id
                    })
                    record.student_subject_absent_id = data_cre.id
    
    @api.depends(
        "date_absent",
        "student_id",
        "student_class_id",
        "semester_id",
    )
    def _compute_student_class_absent_id(self):
        for record in self:
            if record.date_absent and record.student_id and record.student_class_id:
                stu_class_abs = self.env["student_class_absent"].search([
                    ('date_absent','=', record.date_absent),
                    ('student_class_id', '=', record.student_class_id.id)
                ])
                if len(stu_class_abs) > 0:
                    record.student_class_absent_id = stu_class_abs.id
                else:
                    data_cre = self.env["student_class_absent"].create({
                        'date_absent': record.date_absent,
                        'student_class_id': record.student_class_id.id,
                        'semester_id': record.semester_id.id
                    })
                    record.student_class_absent_id = data_cre.id

    @api.depends(
        "semester_id",
        "subject_id",
        'student_class_id',
    )
    def _compute_teaching_schedule_id(self):
        for record in self:
            if record.semester_id and record.subject_id and record.student_class_id:
                teaching_schedule = self.env["teaching_schedule"].search([
                    ('subject_id','=', record.subject_id.id),
                    ('student_class_id', '=', record.student_class_id.id),
                    ('subject_id', '=', record.subject_id.id)
                ])
                if len(teaching_schedule) > 0:
                    record.teaching_schedule_id = teaching_schedule.id
                else:
                    record.teaching_schedule_id = False