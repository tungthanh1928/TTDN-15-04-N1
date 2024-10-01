from odoo import models, fields, api


class CaHoc(models.Model):
    _name = 'ca_hoc'
    _description = 'Quản lý ca hoc'
    # _rec_name = 'display_name'
    # _order = 'number desc, class_name asc, full_name asc'

    # ca_hoc_id = fields.Char("Mã ca học")
    date = fields.Date(
        compute = "_compute_date",
        store = True
    )
    start_time = fields.Datetime(string="Thời gian bắt đầu")
    end_time = fields.Datetime(string="Thời gian Ket thuc")
    student_class_id = fields.Many2one(
        "student_class",   
        string = "Lớp"
    )
    student_list = fields.Many2many(
        "student", 
        string="Danh sách sinh viên"
    ) 
    alowwed_app_list = fields.Text("Danh sách app được phép sử dụng")
    status = fields.Boolean(string="Status", default=False)

    # log_sinh_vien_ca_hoc_ids = fields.One2many(model_name='log_sinh_vien_ca_hoc', invert_name='ca_hoc_id')
    log_sinh_vien_ca_hoc_ids = fields.One2many(
        comodel_name='log_sinh_vien_ca_hoc',
        inverse_name='ca_hoc_id',
        string='Log Sinh Viên Ca Học'
    )

    @api.depends(
        "start_time"
    )
    def _compute_date(self):
        for record in self:
            if record.start_time:
                record.date = record.start_time.date()
    
    