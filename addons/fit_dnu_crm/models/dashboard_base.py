from odoo import models, fields, api
from datetime import datetime, timedelta
import pytz
import requests

class DashboardBase(models.Model):
    """
        Class này định nghĩa Dashboard
    """
    
    _name = "dashboard_base"

    dashboard = fields.Char(string="dashboard",default="dashboard")
    dashboard_tree_field = fields.Char(string="dashboard_tree",store=True, default="dashboard_tree",readonly=True)

    # Vắng
    so_sv_vang = fields.Integer(string='Số lượng SV vắng', compute="_compute", store=True)
    so_lop_co_sv_vang = fields.Integer(string='Số  lớp có SV vắng:', compute="_compute", store=True)

    # Học phí
    so_sv_phai_dong_hp = fields.Integer(string='Số lượng phải đóng HP', compute="_compute", store=True)
    so_sv_chua_dong_hp = fields.Integer(string='Số lượng SV chưa đóng HP', compute="_compute", store=True)
    # so_lop_chua_hoan_thanh_hp = fields.Integer(string='Số  lớp có SV vắng:', compute="_compute", store=True)

    @api.depends('dashboard')
    def _compute(self):
        for record in self:
            record.tinh_thong_tin_vang()
            record.tinh_thong_tin_hoc_phi()


    def tinh_thong_tin_vang(self):
        for record in self:
            ngay_hien_tai = (datetime.now(tz=pytz.UTC)+timedelta(hours=7)).date()
            so_sv_vang = self.env["student_absent"].search_count([
                ('date_absent', '=', ngay_hien_tai)
            ])
            record.so_sv_vang = so_sv_vang
            so_lop_co_sv_vang = self.env["student_class_absent"].search_count([
                ('date_absent', '=', ngay_hien_tai)
            ])
            record.so_lop_co_sv_vang = so_lop_co_sv_vang

    def tinh_thong_tin_hoc_phi(self):
        for record in self:
            so_sv_phai_dong_hp = self.env["student_tuition_fee"].search_count([
                ('current_semester', '=', True),
            ])
            so_sv_chua_dong_hp = self.env["student_tuition_fee"].search_count([
                ('current_semester', '=', True),
                ('status', '=', False)
            ])
            record.so_sv_phai_dong_hp = so_sv_phai_dong_hp
            record.so_sv_chua_dong_hp = so_sv_chua_dong_hp

    def hien_thi_sinh_vien_vang(self):
        text = 'Danh sách sinh viên vắng'
        ngay_hien_tai = (datetime.now(tz=pytz.UTC)+timedelta(hours=7)).date()
        result = self.env["student_absent"].search([
            ('date_absent', '=', ngay_hien_tai)
        ])
        list_id = False
        if len(result) > 0:
            list_id = result.ids
        res =  {
            'name': text,
            'res_model': 'student_absent',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'views': [[False, 'tree'],[False, 'form'],],
            'view_id' : self.env.ref('fit_dnu_crm.view_student_absent_tree').id,
            'domain':[('id','in',list_id)],
            'target': 'current',
        }
        return res

    def hien_thi_lop_sinh_vien_vang(self):
        text = 'Danh sách lớp có sinh viên vắng'
        ngay_hien_tai = (datetime.now(tz=pytz.UTC)+timedelta(hours=7)).date()
        result = self.env["student_class_absent"].search([
            ('date_absent', '=', ngay_hien_tai)
        ])
        list_id = False
        if len(result) > 0:
            list_id = result.ids
        res =  {
            'name': text,
            'res_model': 'student_class_absent',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'views': [[False, 'tree'],[False, 'form'],],
            'view_id' : self.env.ref('fit_dnu_crm.view_student_class_absent_tree').id,
            'domain':[('id','in',list_id)],
            'target': 'current',
        }
        return res

    
    def hien_thi_hoc_phi_phai_dong_hp(self):
        text = 'Danh sách sinh viên đóng học phí'
        result = self.env["student_tuition_fee"].search([
            ('current_semester', '=', True),
        ])
        list_id = False
        if len(result) > 0:
            list_id = result.ids
        res =  {
            'name': text,
            'res_model': 'student_tuition_fee',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'views': [[False, 'tree'],[False, 'form'],],
            'view_id' : self.env.ref('fit_dnu_crm.view_student_tuition_fee_tree').id,
            'domain':[('id','in',list_id)],
            'target': 'current',
        }
        return res

    def hien_thi_hoc_phi_chua_dong_hp(self):
        text = 'Danh sách sinh viên đóng học phí'
        result = self.env["student_tuition_fee"].search([
            ('current_semester', '=', True),
            ('status', '=', False)
        ])
        list_id = False
        if len(result) > 0:
            list_id = result.ids
        res =  {
            'name': text,
            'res_model': 'student_tuition_fee',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'views': [[False, 'tree'],[False, 'form'],],
            'view_id' : self.env.ref('fit_dnu_crm.view_student_tuition_fee_tree').id,
            'domain':[('id','in',list_id)],
            'target': 'current',
        }
        return res
        
            
