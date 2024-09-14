from odoo import models, fields, api
from bs4 import BeautifulSoup
import requests
from .general_crawl import general_info_crawl, get_class_id 
import json

class StudentSubjectAbsentCrawl(models.Model):
    _name = 'student_subject_absent_crawl'
    _description = 'Quản lý sinh viên vắng theo môn học crawl'
    _order = 'semester_id desc, class_name asc'

    student_id = fields.Many2one("student", string = "Sinh viên", ondelete = 'cascade', required = True)
    student_code = fields.Char(related = 'student_id.student_code', string = "Mã sinh viên")
    full_name = fields.Char(related = 'student_id.full_name', string = "Họ tên")
    student_class_id = fields.Many2one(
                comodel_name='student_class',
                related = "student_id.student_class_id", 
                string = "Lớp",
                store = True,
                )
    student_cohort_id = fields.Many2one(
                comodel_name='student_cohort',
                related = "student_id.student_cohort_id", 
                string = "Khóa",
                store = True,
                )
    semester_id = fields.Many2one("semester", string = "Kỳ học", ondelete = 'cascade', required = True)
    subject_id = fields.Many2one("subject", string = "Môn học", ondelete = 'cascade', required = True)
    class_name = fields.Char("Tên lớp", related = 'student_class_id.class_name', store = True)
    number = fields.Integer("Khoá", related = 'student_cohort_id.number', store = True)
    subject_name = fields.Char("Tên môn học", related = 'subject_id.subject_name', store = True)

    total_lesson_absent = fields.Char("Số tiết vắng")
    total_lessons = fields.Integer("Tổng số tiết học",
                                        related = "subject_id.total_lessons",
                                        store = True
                                        )
    
    number_study_credits = fields.Integer(
                            related = 'subject_id.number_study_credits', 
                            string = "Số tín chỉ",
                            store = True
                        )
    

    _sql_constraints = [
        ('student_subject_semester_uniq', 'unique(student_id, semester_id, subject_id)', 'Đã tồn tại bản ghi sinh viên + môn học + kỳ học'),
    ]

                
    def compute_percent_absent_all(self):
        for record in self:
            student_subject_absent = self.env["student_subject_absent"].search([])
            for vl in student_subject_absent:
                vl._compute_percent_absent()
 
    def crawl_data_student_subject_absent(self):
        print("Chạy vào cronjob Vắng")
        url_get_info_study = (
            "https://nhapdiem.dainam.edu.vn/XemThongTinHocTapSinhVien/_DanhSachSinhVien"
        )
        list_sub = ["b9cbcd85-6080-4313-8863-26227d69b63d",'a26be63c-409b-475c-8314-8bee026aef98', '771a3fad-ed2b-4663-b876-b8ba62df8dac']
        TOKEN = "7462680738:AAEva3MCNgAFVIJw5DvigASpgxtlOhxnw48"
        chat_id = "-4573759753"
        try:
            with requests.Session() as session:
                semester_id = self.env["semester"].search([
                    ('current_semester','=', True)
                ], limit=1)
                                
                map_subject_in_semester = {
                    x.subject_name: x.id for x in semester_id.subject_ids
                }
                
                display_name = semester_id.display_name
                nam_bd = display_name.split(" - ")[0]
                nam_kt = int(nam_bd) + 1
                nam_hoc = f'{nam_bd}-{nam_kt}'
                hoc_ky = semester_id.semester_number

                student_subject_absent_crawl_ids = self.env["student_subject_absent_crawl"].search([
                    ('semester_id','=', semester_id.id),
                ])
                
                map_student_subject_absent_crawl = {
                    f"{x.student_code}_{x.subject_name}": {'id': x.id, 'total_lesson_absent': x.total_lesson_absent} 
                    for x in student_subject_absent_crawl_ids
                }
                
                student_ids = self.env["student"].search([
                    ('status','=', 'Đang học'),
                ])
                
                map_student = {
                    x.student_code: x.id
                    for x in student_ids
                }
                list_subject_not_exist = []
                list_student_not_exist = []
                total_create = 0
                total_update = 0
                for sub in list_sub:
                    headers_general, cookies_data = general_info_crawl(session, sub)    
                    dict_class = get_class_id(session, cookies_data, sub, headers_general)
                    data_create_in_sub = []
                    for lopId in dict_class:
                        response_get_subject = requests.post(
                            url_get_info_study,
                            headers=headers_general,
                            data={ 
                                "Hoc_ky": hoc_ky,
                                "Nam_hoc": nam_hoc,
                                "ID_lop": f"{lopId}",
                            },
                            cookies=cookies_data,
                        )
                        html_content = response_get_subject.text

                        # Tìm phần tử tr có class là "jsgrid-header-row"
                        result = convert_html_to_json(html_content, lopId)
                        for vl in result:
                            student_code_vl = vl['student_code']
                            subject_name_vl = vl['subject_name']
                            total_lesson_absent_vl = vl['total_lesson_absent']
                            if subject_name_vl not in map_subject_in_semester:
                                list_subject_not_exist.append(subject_name_vl)
                            else:
                                if map_student.get(student_code_vl) == None:
                                    list_student_not_exist.append(student_code_vl)
                                else:
                                    key = f'{student_code_vl}_{subject_name_vl}'
                                    if key not in map_student_subject_absent_crawl:
                                        data_create_in_sub.append({
                                            'student_id': map_student.get(student_code_vl),
                                            'subject_id': map_subject_in_semester.get(subject_name_vl),
                                            'semester_id': semester_id.id,
                                            'total_lesson_absent': total_lesson_absent_vl
                                        })
                                        total_create += 1
                                    else:
                                        if total_lesson_absent_vl != map_student_subject_absent_crawl.get(key)['total_lesson_absent']:
                                            id_record = map_student_subject_absent_crawl.get(key)['id']
                                            stu_subject_abs_crawl_id = self.env['student_subject_absent_crawl'].browse(id_record)
                                            stu_subject_abs_crawl_id.write({
                                                'total_lesson_absent': total_lesson_absent_vl,
                                            })
                                            total_update += 1
                    if data_create_in_sub:                   
                        self.env["student_subject_absent_crawl"].create(data_create_in_sub)
                    
                message_succ = f"Lấy data vắng thành công. Thêm: {total_create}, Update: {total_update}"
                if list_subject_not_exist:
                    text = f". Môn học chưa có mã: {list_subject_not_exist}"
                    url_succ = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}"
                url_succ = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message_succ}"
                session.get(url_succ)
        except Exception as e:
            message_fail = "Lấy data vắng thất bại. Lỗi: "
            message_fail += str(e)
            url_fail = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message_fail}"
            session.get(url_fail)
                

def extract_jsgrid_data(html):
    soup = BeautifulSoup(html, "html.parser")

    # Tìm jsgrid trong HTML
    jsgrid_element = soup.find("div", class_="jsgrid")
    if not jsgrid_element:
        # raise ValueError("Không tìm thấy JSGrid trong HTML")
        pass
    # Lấy title hàng
    else:
        headers = [th.text.strip() for th in jsgrid_element.find_all("th")]

        # Trích xuất dữ liệu từ các hàng
        data = []
        rows = jsgrid_element.select(".jsgrid-grid-body .jsgrid-table tbody tr")
        for row in rows:
            cells = row.find_all("td")
            row_data = {
                headers[i]: cells[i].text.strip() if i < len(cells) else ""
                for i in range(len(headers))
            }
            data.append(row_data)

        return data


def convert_html_to_json(html, class_id):
    result = []
    try:
        jsgrid_data = extract_jsgrid_data(html)
        json_data = json.dumps(jsgrid_data, ensure_ascii=False, indent=4)
        ignored_keys = ["STT", "Mã SV", "Họ tên"]
        

        # Duyệt qua từng sinh viên trong danh sách
        for student in jsgrid_data:
            for key, value in student.items():
                # Bỏ qua các trường không phải môn học, các trường có giá trị rỗng, giá trị là "0", nghỉ quá số tiết
                if (
                    key not in ignored_keys
                    and value
                    and value != "0"
                    # and value != "Nghỉ quá số tiết"
                ):
                    data_entry = {
                        "student_code": student["Mã SV"],
                        "subject_name": key,
                        "total_lesson_absent": value,
                    }
                    result.append(data_entry)

        return result

    except Exception as e:
        # print(f"Lỗi khi chuyển đổi HTML sang JSON: {e}")
        return result

