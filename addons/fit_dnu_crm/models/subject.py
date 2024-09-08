from odoo import models, fields, api


class Subject(models.Model):
    _name = 'subject'
    _description = 'Quản lý môn học'
    _rec_name = 'display_name'
    _order = 'subject_name asc'

    subject_code = fields.Char("Mã môn học", required = True)
    subject_name = fields.Char("Tên môn học", required = True)
    number_study_credits = fields.Integer("Số tín chỉ", required = True)
    total_lessons = fields.Integer("Tổng số tiết học",
                        compute = "_compute_total_lessons",
                        store = True
                        )
    number_lesson_allow_absent = fields.Integer("Số tiết học được phép vắng",
                                        compute = "_compute_lesson_allow_absent",
                                        store = True
                                        )
    display_name = fields.Char("Tên hiển thị", 
                               compute = "compute_display_name",
                               store = True
                               )

    _sql_constraints = [
        ('subject_code_uniq', 'unique (subject_code)', """Mã môn học đã tồn tại"""),
    ]
    
    @api.depends(
        "subject_code",
        "subject_name",
    )
    def compute_display_name(self):
        
        for record in self:
            if record.subject_code and record.subject_name:
                record.display_name = f'{record.subject_name} ({record.subject_code})'
    
    def compute_display_name_all(self):
        print("Vào đây zzzz")
        subject = self.env["subject"].search([
        ])
        subject.compute_display_name()
    @api.depends(
        "number_study_credits",
    )
    def _compute_total_lessons(self):
        for record in self:
            if record.number_study_credits:
                record.total_lessons = record.number_study_credits * 15
    
    @api.depends(
        "total_lessons",
    )
    def _compute_lesson_allow_absent(self):
        for record in self:
            if record.total_lessons:
                record.number_lesson_allow_absent = record.total_lessons * 20/100
    