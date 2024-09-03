from odoo import models, fields, api


class StudentClassAbsent(models.Model):
    _name = 'student_class_absent'
    _description = 'Quản lý sinh viên vắng theo lớp'
    _rec_name = 'display_name'
    _order = 'date_absent desc, class_name asc'

    display_name = fields.Char(
                        compute = "_compute_display_name",
                        store = True
                    )
    student_class_id = fields.Many2one("student_class", string = "Lớp", ondelete = 'cascade', required = True)
    student_cohort_id = fields.Many2one(
                comodel_name='student_cohort',
                related = "student_class_id.student_cohort_id", 
                string = "Khóa",
                store = True,
            )
    class_name = fields.Char("Tên lớp", related = 'student_class_id.class_name', store = True)
    number = fields.Integer("Khoá", related = 'student_cohort_id.number', store = True)
    number_absent = fields.Integer("Số lượng vắng",
                                    compute = "_compute_number_absent",
                                    store = True
                                )
    # date_id = fields.Many2one("date_manager", string = "Ngày", required = True)
    date_absent = fields.Date("Ngày",
                            # compute = "_compute_date_absent",
                            # store = True
                        )
    student_absent_ids = fields.One2many("student_absent", 
                                            inverse_name="student_class_absent_id", 
                                            string = "Danh sách vắng")
    semester_id = fields.Many2one("semester", string = "Kỳ học", ondelete = 'cascade', required = True)
    
    
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

    _sql_constraints = [
        ('student_date_absent_uniq', 'unique(student_class_id, date_absent)', 'Đã tồn tại bản ghi lớp với ngày vắng này'),
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
        "student_class_id",
        "student_class_id.class_name",
        "date_absent"
    )
    def _compute_display_name(self):
        for record in self:
            if record.student_class_id and record.date_absent:
                record.display_name = f'{record.student_class_id.class_name} ({record.date_absent.strftime("%d-%m-%Y")})'

    
    @api.depends(
        "student_absent_ids",
        "student_absent_ids.student_class_id",
    )
    def _compute_number_absent(self):
        print("Vào đây 1")
        for record in self:
            print("Vào đây 2")
            list_student_ids = []
            if record.student_absent_ids:
                for stu_absent in record.student_absent_ids:
                    stu_id = stu_absent.student_id.id
                    if stu_id not in list_student_ids:
                        list_student_ids.append(stu_id) 
            record.number_absent = len(list_student_ids)
            