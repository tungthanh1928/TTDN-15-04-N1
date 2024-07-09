from odoo import models, fields, api


class DonXinLamNgoaiGioWizard(models.TransientModel):
    _name = "don_xin_lam_ngoai_gio_wizard"
    _description = "Đơn xin làm ngoài giờ Wizard"

    @api.model
    def _compute_num_of_rec(self):
        active_ids = self.env.context.get('active_ids', []) or []
        return len(active_ids)
    
    number_of_records = fields.Integer(
        "Số lượng profile", default=_compute_num_of_rec, readonly=True)
    
    def phe_duyet(self):
        active_ids = self.env.context.get('active_ids', []) or []
        model = self.env.context.get('active_model')
        records = self.env[model].browse(active_ids)
        records.duyet_don()
    
    def khong_phe_duyet(self):
        active_ids = self.env.context.get('active_ids', []) or []
        model = self.env.context.get('active_model')
        records = self.env[model].browse(active_ids)
        records.khong_duyet_don()


class DonXinDenMuonWizard(models.TransientModel):
    _name = "don_xin_den_muon_wizard"
    _description = "Đơn xin đến muộn Wizard"

    @api.model
    def _compute_num_of_rec(self):
        active_ids = self.env.context.get('active_ids', []) or []
        return len(active_ids)
    
    number_of_records = fields.Integer(
        "Số lượng profile", default=_compute_num_of_rec, readonly=True)
    
    def duyet_khong_phat(self):
        active_ids = self.env.context.get('active_ids', []) or []
        model = self.env.context.get('active_model')
        records = self.env[model].browse(active_ids)
        records.duyet_khong_phat()
    
    def duyet_phat(self):
        active_ids = self.env.context.get('active_ids', []) or []
        model = self.env.context.get('active_model')
        records = self.env[model].browse(active_ids)
        records.duyet_phat()
    
    def khong_duyet(self):
        active_ids = self.env.context.get('active_ids', []) or []
        model = self.env.context.get('active_model')
        records = self.env[model].browse(active_ids)
        records.khong_duyet()

class DonXinVeSomWizard(models.TransientModel):
    _name = "don_xin_ve_som_wizard"
    _description = "Đơn xin về sớm Wizard"

    @api.model
    def _compute_num_of_rec(self):
        active_ids = self.env.context.get('active_ids', []) or []
        return len(active_ids)
    
    number_of_records = fields.Integer(
        "Số lượng profile", default=_compute_num_of_rec, readonly=True)
    
    def duyet_khong_phat(self):
        active_ids = self.env.context.get('active_ids', []) or []
        model = self.env.context.get('active_model')
        records = self.env[model].browse(active_ids)
        records.duyet_khong_phat()
    
    def duyet_phat(self):
        active_ids = self.env.context.get('active_ids', []) or []
        model = self.env.context.get('active_model')
        records = self.env[model].browse(active_ids)
        records.duyet_phat()
    
    def khong_duyet(self):
        active_ids = self.env.context.get('active_ids', []) or []
        model = self.env.context.get('active_model')
        records = self.env[model].browse(active_ids)
        records.khong_duyet()


class DonXinNghiWizard(models.TransientModel):
    _name = "don_xin_nghi_wizard"
    _description = "Đơn xin nghỉ Wizard"

    @api.model
    def _compute_num_of_rec(self):
        active_ids = self.env.context.get('active_ids', []) or []
        return len(active_ids)
    
    number_of_records = fields.Integer(
        "Số lượng profile", default=_compute_num_of_rec, readonly=True)
    
    def duyet_khong_phat(self):
        active_ids = self.env.context.get('active_ids', []) or []
        model = self.env.context.get('active_model')
        records = self.env[model].browse(active_ids)
        records.duyet_khong_phat()
    
    def duyet_phat(self):
        active_ids = self.env.context.get('active_ids', []) or []
        model = self.env.context.get('active_model')
        records = self.env[model].browse(active_ids)
        records.duyet_phat()
    
    def khong_duyet(self):
        active_ids = self.env.context.get('active_ids', []) or []
        model = self.env.context.get('active_model')
        records = self.env[model].browse(active_ids)
        records.khong_duyet()

class NhanVienBuoiWizard(models.TransientModel):
    _name = "nhan_vien_buoi_wizard"
    _description = "Nhân viên buổi Wizard"

    @api.model
    def _compute_num_of_rec(self):
        active_ids = self.env.context.get('active_ids', []) or []
        return len(active_ids)
    
    number_of_records = fields.Integer(
        "Số lượng profile", default=_compute_num_of_rec, readonly=True)
    
    def tu_dong_check_in(self):
        active_ids = self.env.context.get('active_ids', []) or []
        model = self.env.context.get('active_model')
        records = self.env[model].browse(active_ids)
        records.tu_dong_check_in()
    
    def tu_dong_check_out(self):
        active_ids = self.env.context.get('active_ids', []) or []
        model = self.env.context.get('active_model')
        records = self.env[model].browse(active_ids)
        records.tu_dong_check_out()

class DonRemoteWizard(models.TransientModel):
    _name = "don_remote_wizard"
    _description = "Đơn remote Wizard"

    @api.model
    def _compute_num_of_rec(self):
        active_ids = self.env.context.get('active_ids', []) or []
        return len(active_ids)
    
    number_of_records = fields.Integer(
        "Số lượng profile", default=_compute_num_of_rec, readonly=True)
    
    def phe_duyet(self):
        active_ids = self.env.context.get('active_ids', []) or []
        model = self.env.context.get('active_model')
        records = self.env[model].browse(active_ids)
        records.duyet_don()
    
    def khong_phe_duyet(self):
        active_ids = self.env.context.get('active_ids', []) or []
        model = self.env.context.get('active_model')
        records = self.env[model].browse(active_ids)
        records.khong_duyet_don()
    