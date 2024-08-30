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


class ImportStudentAbsent(models.TransientModel):
    _name = "student_absent.import_wizard"
    _description = "Import sinh viên vắng"
    _header = ["Mã sinh viên", "Lý do vắng", "Mã môn học"]

    date_absent = fields.Date("Ngày vắng", require = True)
    file_import = fields.Binary("File import")
    noti_html = fields.Text(default='')

    def import_student_absent(self):
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
        stu_absent = self.env["student_absent"].search([
            ('date_absent','=', self.date_absent)
        ])
        map_stu_absent = {x.student_code: x.id for x in stu_absent}

        stu = self.env["student"].search([])
        map_stu = {x.student_code: x.id for x in stu}

        list_error_stu_null = []
        list_error_stu_not_found = []
        list_stu_absent_exist = []
        list_result_create = []

        map_stu_absent_exist_id = {}

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
                    if map_stu_absent.get(student_code) != None:
                        list_stu_absent_exist.append(student_code)


        if len(list_error_stu_null) > 0  \
            or len(list_error_stu_not_found) > 0:
            check = False
        
        if check == True:
            for i, row in enumerate(data):
                student_code = row.get("Mã sinh viên")
                reason = row["Lý do vắng"]
                student_id = map_stu.get(student_code)
                if student_code not in list_stu_absent_exist:
                    list_result_create.append({
                        'student_id': student_id,
                        'date_absent': self.date_absent,
                        'reason': reason
                    })
                else:
                    stu_absent_exist_id = map_stu_absent_exist_id.get(student_code)
                    self.env['student_absent'].browse(stu_absent_exist_id).write({
                        'reason': reason
                    })
            self.env['student_absent'].create(list_result_create)
                
        else:
            if len(list_error_stu_null) > 0:
                report_string += f'[!] Cột "Mã định danh" trống ở dòng {list_error_stu_null}!\n'
            
            if len(list_error_stu_not_found) > 0:
                report_string += f'[!] Cột "Mã định danh" không tồn tại trong hệ thống ở các dòng {list_error_stu_not_found}!\n'
            
            self.noti_html = noti
            return report_string
    
    def get_header(self):
        fd, path = tempfile.mkstemp(suffix='.xlsx')
        import_template = pd.DataFrame(columns=self._header)
        import_template.to_excel(path, index=False)
        result = base64.b64encode(os.fdopen(fd, "rb").read())
        attachment = self.env['ir.attachment'].create({
            'name': "mau_import_student_absent.xlsx",
            'store_fname': 'test.xlsx',
            'datas': result
        })
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % (attachment.id),
            'target': 'self',
        }