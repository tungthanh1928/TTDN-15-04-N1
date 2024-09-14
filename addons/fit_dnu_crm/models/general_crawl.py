

def general_info_crawl(session, sub):
    # Thúy: 'a26be63c-409b-475c-8314-8bee026aef98'
    # Bảo Châu: "b9cbcd85-6080-4313-8863-26227d69b63d"
    # Minh Châu: '771a3fad-ed2b-4663-b876-b8ba62df8dac'
    
    headers_general = {
        "Host": "nhapdiem.dainam.edu.vn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "*/*",
        "Accept-Language": "vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3",
    }
    url_get_session = f"https://nhapdiem.dainam.edu.vn/Account/SignIn?sub={sub}"
    response_get_session = session.get(url_get_session, allow_redirects=False)

    set_cookie_header = (
        response_get_session.headers.get("Set-Cookie").split(";")[0].split("=")[1]
    )
    cookies_data = {"culture": "en", "ASP.NET_SessionId": f"{set_cookie_header}"}
    # return sub, headers_general, cookies_data
    return headers_general, cookies_data

def get_class_id(session, cookies_data, sub, headers_general):
    cohort_id = list()
    list_faculity_id = list()
    
    dict_class = {}
    
    url_list_faculity_id = 'https://nhapdiem.dainam.edu.vn/Common/LoadKhoaLopHanhChinh' # Khoa đào tạo CNTT/KHMT/HTTTT
    response_khoa_id = session.post(
        url_list_faculity_id,
        headers=headers_general,
        data={
            "placeholder": "--Ch%E1%BB%8Dn+khoa--",
            "ID_he": "3",
            "ID_khoa": "0",
            "ID_cb": f"{sub}",
        },
        cookies=cookies_data,
    )
    response_khoa_id_json = response_khoa_id.json()
    
    list_faculity_id.extend(item["id"] for item in response_khoa_id_json["data"])
    for faculity in list_faculity_id:
        # Lấy id Khoá
        url_cohort_id = "http://nhapdiem.dainam.edu.vn/Common/LoadKhoaHocLopHanhChinh"
        response_cohort_id = session.post(
            url_cohort_id,
            headers=headers_general,
            data={
                "placeholder": "--Ch%E1%BB%8Dn+kh%C3%B3a+h%E1%BB%8Dc--",
                "ID_he": "3",
                'ID_khoa': faculity,
            },
            cookies=cookies_data,
        )
        response_cohort_id_json = response_cohort_id.json()
        cohort_id.extend(item["id"] for item in response_cohort_id_json["data"])
        list_set_cohort_id = list(set(cohort_id))
        url_class_id = "http://nhapdiem.dainam.edu.vn/Common/LoadLopHanhChinh"
        for khoa in list_set_cohort_id:
            response_class_id = session.post(
                url_class_id,
                headers=headers_general,
                data={
                    "placeholder": "--Ch%E1%BB%8Dn+l%E1%BB%9Bp--",
                    "ID_he": "3",
                    "Khoa_hoc": f"{khoa}",
                    "ID_khoa": f"{faculity}",
                    # "ID_cb": f"{sub}",
                },
                cookies=cookies_data,
            )
            response_class_id_json = response_class_id.json()
            for item in response_class_id_json["data"]:
                if item["id"] not in dict_class:
                    dict_class[item["id"]] = {
                        'ID_lop': item['item']['ID_lop'],
                        'Ten_lop': item['item']['Ten_lop'],
                        'ID_dt': item['item']['ID_dt'],
                        'ID_khoa': item['item']['ID_khoa'],
                        'ID_chuyen_nganh': item['item']['ID_chuyen_nganh'],
                        'Khoa_hoc': item['item']['Khoa_hoc'],
                    }
        return dict_class