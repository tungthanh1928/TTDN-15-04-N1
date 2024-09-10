from odoo import models, fields, api


class StudentClassTuitionFee(models.Model):
    _name = 'student_class_tuition_fee'
    _description = 'Quản lý học phí theo lớp'
    _rec_name = 'display_name'
    _order = 'number asc, class_name asc'

    display_name = fields.Char(
                        compute = "_compute_display_name",
                        store = True
                    )
    student_class_id = fields.Many2one("student_class", string = "Lớp", ondelete = 'cascade', required = True)
    class_name = fields.Char("Tên lớp", related = 'student_class_id.class_name', store = True)
    number = fields.Integer("Khóa", related = 'student_cohort_id.number', store = True)
    student_cohort_id = fields.Many2one(
                comodel_name='student_cohort',
                related = "student_class_id.student_cohort_id", 
                string = "Khóa",
                store = True,
                )
    number = fields.Integer("Khoá", related = 'student_cohort_id.number', store = True)
    semester_id = fields.Many2one("semester", string = "Học kỳ", ondelete = 'cascade', required = True)
    current_semester = fields.Boolean("Kỳ hiện tại", 
                        related = "semester_id.current_semester",
                        store = True,
                    )
    school_year_id = fields.Many2one("school_year", 
                            string = "Năm học", 
                            ondelete = 'cascade',
                            related = "semester_id.school_year_id", 
                            store = True
                            )
    number_unpaid = fields.Integer("Số lượng chưa đóng",
                                    compute = "_compute_number_unpaid",
                                    store = True
                                )
    total = fields.Integer("Tổng số",
                                    compute = "_compute_number_unpaid",
                                    # store = True
                                )
    student_tuition_fee_ids = fields.One2many("student_tuition_fee", 
                                            inverse_name="student_class_tuition_fee_id", 
                                            string = "Danh sách đóng học phí")

    _sql_constraints = [
        ('class_semester_id_uniq', 'unique(student_class_id, semester_id)', 'Đã tồn tại bản ghi lớp với ngày vắng này'),
    ]
    
    @api.depends(
        "student_class_id",
        "student_class_id.class_name",
        "semester_id"
    )
    def _compute_display_name(self):
        for record in self:
            if record.student_class_id and record.semester_id:
                record.display_name = f'{record.student_class_id.class_name} ({record.semester_id.display_name})'

    
    @api.depends(
        "student_tuition_fee_ids",
        "student_tuition_fee_ids.student_class_id",
        "student_tuition_fee_ids.status",
    )
    def _compute_number_unpaid(self):
        for record in self:
            record.total = len(record.student_tuition_fee_ids)
            result = 0
            if record.student_tuition_fee_ids:
                for vl in record.student_tuition_fee_ids:
                    if vl.status == False:
                        result += 1
            record.number_unpaid = result