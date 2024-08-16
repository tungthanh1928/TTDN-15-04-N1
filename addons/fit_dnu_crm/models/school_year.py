from odoo import models, fields, api


class SchoolYear(models.Model):
    _name = 'school_year'
    _description = 'Quản lý năm học'
    _rec_name = 'display_name'
    _order = 'start_year desc'

    display_name = fields.Char("Năm học", 
                               compute = "_compute_display_name",
                               store = True
                               )
    start_year = fields.Integer(string='Năm bắt đầu', required = True)

    _sql_constraints = [
        ('display_name_uniq', 'unique (display_name)', """Năm học đã tồn tại"""),
    ]

    @api.depends("start_year")
    def _compute_display_name(self):
        for record in self:
            if record.start_year:
                end_year = record.start_year +  1
                record.display_name = f'{record.start_year} - {end_year}'