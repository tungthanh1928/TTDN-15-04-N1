from odoo import models, fields, api

class ChiPhi(models.Model):
    _name = 'chi.phi'
    _description = 'Chi phí'

    name = fields.Char('Tên chi phí', required=True)
    so_tien = fields.Float('Số tiền', required=True)
    ngay_chi = fields.Date('Ngày chi', default=fields.Date.today())
    du_an_id = fields.Many2one('du.an', string='Dự án')
    mo_ta = fields.Text('Mô tả chi phí')

    @api.model
    def create(self, vals):
        # Gọi phương thức tạo chi phí
        record = super(ChiPhi, self).create(vals)
        # Cập nhật tổng chi phí cho dự án
        if record.du_an_id:
            total_cost = sum(record.du_an_id.chi_phi_ids.mapped('so_tien')) + record.so_tien
            record.du_an_id.tong_chi_phi = total_cost
        return record

    def write(self, vals):
        # Lưu giá trị cũ để tính toán
        old_record = self.read(['so_tien', 'du_an_id'])
        result = super(ChiPhi, self).write(vals)
        # Cập nhật tổng chi phí cho dự án
        for record in self:
            if record.du_an_id:
                total_cost = sum(record.du_an_id.chi_phi_ids.mapped('so_tien'))
                if 'so_tien' in vals:
                    total_cost += vals['so_tien'] - old_record[0]['so_tien']
                record.du_an_id.tong_chi_phi = total_cost
        return result