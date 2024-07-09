import base64
import os
import tempfile
import pandas as pd
from odoo import fields, models, api
from datetime import datetime
import pytz

class ThongKeThang(models.TransientModel):
    _name = "thong_ke_thang.custom_export"
    _description = "Export thống kê tháng"

    thang_select = fields.Selection([
        ('1', 'Tháng 1'),
        ('2', 'Tháng 2'),
        ('3', 'Tháng 3'),
        ('4', 'Tháng 4'),
        ('5', 'Tháng 5'),
        ('6', 'Tháng 6'),
        ('7', 'Tháng 7'),
        ('8', 'Tháng 8'),
        ('9', 'Tháng 9'),
        ('10', 'Tháng 10'),
        ('11', 'Tháng 11'),
        ('12', 'Tháng 12'),
    ], string='Tháng', default = str(datetime.now(tz=pytz.UTC).month))
    nam_int = fields.Integer(string="Năm", default = datetime.now().year)

    def export_thong_ke_thang(self):
        '''
            Hàm này có chức năng Export thống kê tháng của tất cả nhân viên theo tháng
        '''
        fd, path = tempfile.mkstemp(suffix='.xlsx')             
        df = pd.DataFrame(columns=[
            "Mã NV", "Họ và tên", "Số buổi đi làm", "Số buổi xin nghỉ được duyệt","Số buổi xin đến muộn được duyệt","Số buổi xin về sớm được duyệt","Số giờ OT", "Số buổi chưa Check-out",
        ])
        list_nhan_vien = self.env['hr.employee'].search([
                        ('trang_thai', '=', 'dang_lam'),
                ])
        for vl in list_nhan_vien:
            nhan_vien_buoi = self.env['nhan_vien_buoi'].search([
                ('thang_select', '=', self.thang_select),
                ('nam_int', '=', self.nam_int),
                ('trang_thai_lam_viec', '=', 'Đi làm'),
                ('trang_thai_check_in', '!=', 'Chưa Check-in'),
                ('nhan_vien_id', '=', vl.id),
            ])
            nhan_vien_thang = self.env['nhan_vien_thang'].search([
                ('thang_select', '=', self.thang_select),
                ('nam_int', '=', self.nam_int),
                ('nhan_vien_id', '=', vl.id),
            ])
            if len(nhan_vien_thang) > 0:
                so_buoi_xin_nghi_duoc_duyet = nhan_vien_thang[0].so_buoi_xin_nghi_duoc_duyet
                so_gio_ot = nhan_vien_thang[0].so_gio_ot_duoc_duyet
                so_buoi_xin_den_muon_duoc_duyet = nhan_vien_thang[0].so_don_xin_den_muon_duoc_duyet
                so_buoi_xin_ve_som_duoc_duyet = nhan_vien_thang[0].so_don_xin_ve_som_duoc_duyet
            else:
                so_buoi_xin_nghi_duoc_duyet = 0
                so_gio_ot = 0
                so_buoi_xin_den_muon_duoc_duyet = 0
                so_buoi_xin_ve_som_duoc_duyet = 0
            
            so_buoi_chua_check_out = 0
            if len(nhan_vien_buoi) > 0:
                for nvb in nhan_vien_buoi:
                    if nvb.trang_thai_check_out == 'Chưa Check-out':
                        so_buoi_chua_check_out += 1
            df = df.append(
                {
                    "Mã NV" : vl.ma_dinh_danh,
                    "Họ và tên" : vl.name, 
                    "Số buổi đi làm": len(nhan_vien_buoi),
                    "Số buổi xin nghỉ được duyệt": so_buoi_xin_nghi_duoc_duyet,
                    "Số buổi xin đến muộn được duyệt":so_buoi_xin_den_muon_duoc_duyet, 
                    "Số buổi xin về sớm được duyệt": so_buoi_xin_ve_som_duoc_duyet,
                    "Số giờ OT": so_gio_ot,
                    "Số buổi chưa Check-out":so_buoi_chua_check_out,
                },
                ignore_index=True
            )
        df.to_excel(path, index=False, encoding="utf-8-sig")
        result = base64.b64encode(os.fdopen(fd, "rb").read())
        attachment = self.env['ir.attachment'].create({
            'name': f"thong_ke_thang_{self.thang_select}_{self.nam_int}.xlsx",
            'store_fname': 'dssv.xlsx',
            'datas': result
        })
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % (attachment.id),
            'target': 'self',
        }
        
class ThongKeNgay(models.TransientModel):
    _name = "thong_ke_ngay"
    _description = "Xem thống kê ngày"

    ngay_date = fields.Date(string="Chọn ngày xem thống kê", default = datetime.now())
    so_don_xin_nghi_chua_duyet = fields.Integer(string="Đơn xin nghỉ", compute="_compute_so_don_xin_nghi_chua_duyet")
    so_don_xin_den_muon_chua_duyet = fields.Integer(string="Đơn xin đến muộn", compute="_compute_so_don_xin_den_muon_chua_duyet")
    so_don_xin_ve_som_chua_duyet = fields.Integer(string="Đơn xin về sớm", compute="_compute_so_don_xin_ve_som_chua_duyet")
    so_don_di_cong_tac_chua_duyet = fields.Integer(string="Đơn xin đi công tác", compute="_compute_so_don_di_cong_tac_chua_duyet")
    so_nguoi_dang_ky_lam_buoi_sang = fields.Integer(string="Số NV đăng ký đi làm", compute="_compute_thong_tin_lam_viec")
    so_nguoi_dang_ky_lam_buoi_chieu = fields.Integer(string="Số NV đăng ký đi làm", compute="_compute_thong_tin_lam_viec")
    so_nv_chua_check_in_buoi_sang = fields.Integer(string="Số NV chưa Check-in", compute="_compute_thong_tin_lam_viec")
    so_nv_chua_check_in_buoi_chieu = fields.Integer(string="Số NV chưa Check-in")
    so_nv_chua_check_out_buoi_sang = fields.Integer(string="Số NV chưa Check-out")
    so_nv_chua_check_out_buoi_chieu = fields.Integer(string="Số NV chưa Check-out")
    
    @api.depends("ngay_date")
    def _compute_so_don_xin_nghi_chua_duyet(self):
        for record in self:
            list_so_don_xin_nghi_chua_duyet = self.env['don_xin_nghi'].search([
                            ('ngay', '=', record.ngay_date),
                            ('trang_thai', '=', 'Chờ duyệt'),
                        ])
            record.so_don_xin_nghi_chua_duyet = len(list_so_don_xin_nghi_chua_duyet)
    

    @api.depends("ngay_date")
    def _compute_so_don_xin_den_muon_chua_duyet(self):
        for record in self:
            list_so_don_xin_den_muon_chua_duyet = self.env['don_xin_den_muon'].search([
                            ('ngay', '=', record.ngay_date),
                            ('trang_thai', '=', 'Chờ duyệt'),
                        ])
            record.so_don_xin_den_muon_chua_duyet = len(list_so_don_xin_den_muon_chua_duyet)

    @api.depends("ngay_date")
    def _compute_so_don_xin_ve_som_chua_duyet(self):
        for record in self:
            list_so_don_xin_ve_som_chua_duyet = self.env['don_xin_ve_som'].search([
                            ('ngay', '=', record.ngay_date),
                            ('trang_thai', '=', 'Chờ duyệt'),
                        ])
            record.so_don_xin_ve_som_chua_duyet = len(list_so_don_xin_ve_som_chua_duyet)
    
    @api.depends("ngay_date")
    def _compute_so_don_di_cong_tac_chua_duyet(self):
        for record in self:
            list_so_don_di_cong_tac_chua_duyet = self.env['don_xin_di_cong_tac'].search([
                            ('ngay_di_cong_tac', '=', record.ngay_date),
                            ('trang_thai', '=', 'Chờ duyệt'),
                        ])
            record.so_don_di_cong_tac_chua_duyet = len(list_so_don_di_cong_tac_chua_duyet)

    @api.depends("ngay_date")
    def _compute_thong_tin_lam_viec(self):
        for record in self:
            list_ban_ghi_buoi = self.env['nhan_vien_buoi'].search([
                        ('ngay_lam_viec', '=', record.ngay_date),
                        ('trang_thai_lam_viec', '=', 'Đi làm'),
                        # ('buoi_lam_viec', '=', 'sang'),
                        # ('trang_thai_check_in', '=', 'Chưa Check-in'),
                    ])
            so_nguoi_dang_ky_lam_buoi_sang = 0
            so_nguoi_dang_ky_lam_buoi_chieu = 0
            so_nv_chua_check_in_buoi_sang = 0
            so_nv_chua_check_in_buoi_chieu = 0
            so_nv_chua_check_out_buoi_sang = 0
            so_nv_chua_check_out_buoi_chieu = 0
            if len(list_ban_ghi_buoi) > 0:
                for vl in list_ban_ghi_buoi:
                    if vl.buoi_lam_viec == 'sang':
                        so_nguoi_dang_ky_lam_buoi_sang += 1
                        if vl.trang_thai_check_in == 'Chưa Check-in':
                            so_nv_chua_check_in_buoi_sang += 1
                        if vl.trang_thai_check_out == 'Chưa Check-out':
                            so_nv_chua_check_out_buoi_sang += 1
                    elif vl.buoi_lam_viec == 'chieu':
                        so_nguoi_dang_ky_lam_buoi_chieu += 1
                        if vl.trang_thai_check_in == 'Chưa Check-in':
                            so_nv_chua_check_in_buoi_chieu += 1
                        if vl.trang_thai_check_out == 'Chưa Check-out':
                            so_nv_chua_check_out_buoi_chieu += 1
                        
            record.so_nguoi_dang_ky_lam_buoi_sang = so_nguoi_dang_ky_lam_buoi_sang
            record.so_nguoi_dang_ky_lam_buoi_chieu = so_nguoi_dang_ky_lam_buoi_chieu
            record.so_nv_chua_check_in_buoi_sang = so_nv_chua_check_in_buoi_sang
            record.so_nv_chua_check_in_buoi_chieu = so_nv_chua_check_in_buoi_chieu
            record.so_nv_chua_check_out_buoi_sang = so_nv_chua_check_out_buoi_sang
            record.so_nv_chua_check_out_buoi_chieu = so_nv_chua_check_out_buoi_chieu

    