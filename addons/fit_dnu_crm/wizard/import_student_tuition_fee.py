import base64
from email.policy import default
import os
import tempfile
from datetime import datetime, timedelta
import json
import pandas as pd
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import math


class ImportStudentTuitionFee(models.TransientModel):
    _name = "student_tuition_fee.import_wizard"
    _description = "Import học phí"
    _header = ["Mã sinh viên"]

    semester_id = fields.Many2one("semester", string = "Học kỳ", ondelete = 'cascade', required = True)
    file_import = fields.Binary("File import")
    noti_html = fields.Text(default='')

    def import_student_tuition_fee(self):
        if self.file_import:
            fd, path = tempfile.mkstemp()
            with os.fdopen(fd, "wb") as tmp:
                tmp.write(base64.decodebytes(self.file_import))
            df = pd.read_excel(path, dtype=str)
            df.fillna(False, inplace=True)
            data = df.to_dict("records")
            report_string = self.process(data)
            so_dong = len(data)
            if report_string:
                raise ValidationError(report_string)
            else:
                vls = f"<H4><B>Hệ thống đã import thành công {so_dong} dòng thông tin.</br></B></H4>"
                id_thong_bao = self.env["custom_noti"].create({
                    "noti_html": vls,
                })

                return {
                    'name': 'Thông báo hệ thống',
                    'type': 'ir.actions.act_window',
                    'res_model': 'custom_noti',
                    'view_mode': 'form',
                    'res_id': id_thong_bao.id,
                    'view_type': 'form',
                    'target': 'new',
                }
        else:
            raise ValidationError("Chưa có file excel.")
        
    def process(self, data):
        report_string = ""
        noti = ""
        fees = self.env["student_tuition_fee"].search([
            ('semester_id','=', self.semester_id.id)
        ])
        map_stu_fee = {x.student_id.student_code: x.id for x in fees}

        stu = self.env["student"].search([
            ('status','=', 'Đang học')
        ])
        map_stu = {x.student_code: x.id for x in stu}

        list_error_stu_null = []
        list_error_stu_not_found = []
        list_error_stu_fee_not_found = []

        check = True

        for i, row in enumerate(data):
            student_code = row.get("Mã sinh viên")
            reason = row["Lý do vắng"]

            if student_code == False:
                list_error_stu_null.append(i+1)
            else:
                if map_stu.get(student_code) == None:
                    list_error_stu_not_found.append(i + 1)
                else:
                    if map_stu_fee.get(student_code) == None:
                        list_error_stu_fee_not_found.append(student_code)


        if len(list_error_stu_null) > 0  \
            or len(list_error_stu_not_found) > 0 \
            or len(list_error_stu_fee_not_found) > 0:
            check = False
        
        if check == True:
            list_id_update = []
            for i, row in enumerate(data):
                student_code = row.get("Mã sinh viên")
                student_id = map_stu.get(student_code)
                list_id_update.append(student_id)
            
            self.env['student_tuition_fee'].browse(list_id_update).write({
                'status': True
            })
                
        else:
            if len(list_error_stu_null) > 0:
                report_string += f'[!] Cột "Mã định danh" trống ở dòng {list_error_stu_null}!\n'
            
            if len(list_error_stu_not_found) > 0:
                report_string += f'[!] Cột "Mã định danh" không tồn tại trong hệ thống ở các dòng {list_error_stu_not_found}!\n'
            
            if len(list_error_stu_fee_not_found) > 0:
                report_string += f'[!] Cột "Mã định danh" không có trong danh sách đóng học phí trong kỳ ở các dòng {list_error_stu_fee_not_found}!\n'

            self.noti_html = noti
            return report_string
    
    def get_header(self):
        fd, path = tempfile.mkstemp(suffix='.xlsx')
        import_template = pd.DataFrame(columns=self._header)
        import_template.to_excel(path, index=False)
        result = base64.b64encode(os.fdopen(fd, "rb").read())
        attachment = self.env['ir.attachment'].create({
            'name': "Mẫu import học phí.xlsx",
            'store_fname': 'test.xlsx',
            'datas': result
        })
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % (attachment.id),
            'target': 'self',
        }