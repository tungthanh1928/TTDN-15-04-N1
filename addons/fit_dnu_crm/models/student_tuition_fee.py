from odoo import models, fields, api


class StudentTuitionFee(models.Model):
    _name = 'student_tuition_fee'
    _description = 'Quản lý sinh viên học phí'
    _rec_name = 'student_id'

    semester_id = fields.Many2one("semester", string = "Học kỳ", ondelete = 'cascade', required = True)
    school_year_id = fields.Many2one("school_year", 
                            string = "Năm học", 
                            ondelete = 'cascade',
                            related = "semester_id.school_year_id", 
                            store = True)
    student_id = fields.Many2one("student", string = "Mã sinh viên", ondelete = 'cascade', required = True)
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
    student_class_tuition_fee_id = fields.Many2one("student_class_tuition_fee", 
                            string = "Lớp - Học phi",
                            compute = "_compute_student_class_tuition_fee_id",
                            store = True,
                        )
    status = fields.Boolean("Đã nộp học phí?", default = False, required = True)
    current_semester = fields.Boolean("Kỳ hiện tại", 
                        related = "semester_id.current_semester",
                        store = True,
                    )

    _sql_constraints = [
        ('student_semester_id_uniq', 'unique(semester_id, student_id)', 'Đã tồn tại bản ghi học phí của sinh viên trong học kỳ này'),
    ]


    @api.depends(
        "semester_id",
        "student_id",
        "student_class_id"
    )
    def _compute_student_class_tuition_fee_id(self):
        for record in self:
            if record.semester_id and record.student_id and record.student_class_id:
                stu_class_fee = self.env["student_class_tuition_fee"].search([
                    ('semester_id','=', record.semester_id.id),
                    ('student_class_id', '=', record.student_class_id.id)
                ])
                if len(stu_class_fee) > 0:
                    record.student_class_tuition_fee_id = stu_class_fee.id
                else:
                    data_cre = self.env["student_class_tuition_fee"].create({
                        'semester_id': record.semester_id.id,
                        'student_class_id': record.student_class_id.id
                    })
                    record.student_class_tuition_fee_id = data_cre.id
