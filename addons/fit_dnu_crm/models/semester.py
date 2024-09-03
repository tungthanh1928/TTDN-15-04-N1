from odoo import models, fields, api


class Semester(models.Model):
    _name = 'semester'
    _description = 'Quản lý kỳ học'
    _rec_name = 'display_name'
    _order = 'display_name desc'

    school_year_id = fields.Many2one("school_year", string = "Năm học", required = True)
    display_name = fields.Char("Kỳ học", 
                               compute = "_compute_display_name",
                               store = True
                               )
    semester_number = fields.Integer(string='Số thự tự kỳ', required = True)
    student_tuition_fees = fields.One2many("student_tuition_fee", inverse_name="semester_id", string = "Học phí")
    number_student_not_paid_tuition = fields.Integer("Số SV chưa đóng HP",
                                compute = "_compute_number_student_not_paid_tuition",
                                store = True
                            )
    current_semester = fields.Boolean("Kỳ hiện tại", default = False, required = True)
    subject_ids = fields.Many2many("subject", relation= "semester_subject", string = "Danh sách môn học trong kỳ")
    
    _sql_constraints = [
        ('display_name_uniq', 'unique (display_name)', """Kỳ học đã tồn tại"""),
    ]

    @api.depends(
        "school_year_id",
        "school_year_id.start_year",
        "semester_number",
    )
    def _compute_display_name(self):
        for record in self:
            if record.school_year_id.start_year and record.semester_number:
                record.display_name = f'{record.school_year_id.start_year} - {record.semester_number}'
    

    @api.depends(
        "student_tuition_fees",
        "student_tuition_fees.status",
        "student_tuition_fees.semester_id",
    )
    def _compute_number_student_not_paid_tuition(self):
        for record in self:
            if record.student_tuition_fees:
                total = 0
                for vl in record.student_tuition_fees:
                    if vl.status == False:
                        total += 1
                record.number_student_not_paid_tuition = total

    def action_sync_stu_tuition_fees(self):
        for record in self:
            list_stu_exist = []
            if record.student_tuition_fees:
                for vl in record.student_tuition_fees:
                    list_stu_exist.append(vl.student_id.id)
            students = self.env["student"].search([
                ('status','=', 'Đang học'),
            ])
            if len(students) > 0:
                list_data_cre = []
                for stu in students:
                    if stu.id not in list_stu_exist:
                        list_data_cre.append({
                            'student_id': stu.id,
                            'semester_id': record.id
                        })
                print("???", list_data_cre)
                self.env["student_tuition_fee"].create(list_data_cre)