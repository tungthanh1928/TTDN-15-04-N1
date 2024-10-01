from odoo import models, fields, api


class LichCongTac(models.Model):
    _name = 'lich_cong_tac'
    _description = 'Quản lý lịch công tác'
    # _rec_name = 'display_name'
    _order = 'ngay desc'
    
    ngay = fields.Date("Ngày", required = True)
    thoi_gian_bat_dau = fields.Datetime("Thời gian bắt đầu", required = True)
    thoi_gian_ket_thuc = fields.Datetime("Thời gian kết thúc")
    noi_dung = fields.Text("Nội dung", required = True)
    thanh_phan = fields.Text("Thành phần", required = True)
    chu_tri = fields.Text("Chủ trì")
    don_vi_thuc_hien = fields.Char("Đơn vị thực hiện")
    dia_diem = fields.Char("Địa điểm")
    phu_trach = fields.Char("Phụ trách")
    tuan_trong_nam = fields.Integer("Tuần trong năm", compute = '_compute_tuan_thu', store = True)
    thu_int = fields.Integer("Thứ", compute = '_compute_tuan_thu', store = True)
    
    @api.depends("ngay")
    def _compute_tuan_thu(self):
        for record in self:
            if record.ngay:
                record.tuan_trong_nam = record.ngay.isocalendar()[1]
                record.thu_int = record.ngay.isocalendar()[2]
    
    