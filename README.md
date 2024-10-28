---
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![GitLab](https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)



# 1. Cài đặt công cụ, môi trường và các thư viện cần thiết

## 1.1. Cài đặt pycharm.

Nhóm phát triển khuyến nghị người sử dụng chạy hệ thống trên Pycharm

`sudo snap install pycharm-community –classic`

## 1.2. khởi tạo môi trường ảo.

`python3 -m venv ./venv`

## 1.3. cài đặt các thư viện cần thiết

Người sử dụng thực thi các lệnh sau đề cài đặt các thư viện cần thiết

```
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev
python3-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev
```

Thay đổi trình thông dịch sang môi trường ảo và chạy requirements.txt để cài đặt tiếp các thư viện được yêu cầu

```
source venv/bin/activate
pip3 install -r requirements.txt
```

# 2. Setup database

Khởi tạo database trên docker bằng việc thực thi file dockercompose.yml.

`dockercompose up -d`

**_thiếu đoạn connect odoo và đặt tên db_**

```buildoutcfg
Config database hiện tại cho APD:

container_name: postgres_container_apd
POSTGRES_DB: postgres
POSTGRES_USER: odoo_apd
POSTGRES_PASSWORD: odoo_apd
port: 5435:5432

```

# 3. Setup tham số chạy cho hệ thống

## 3.1. Khởi tạo odoo.conf

Tạo tệp **odoo.conf** có nội dung như sau:

```
[options]
db_host = localhost
db_port = <cổng của postgres>
db_user = <user của postgres>
db_password = <mật khẩu của postgres>
addons_path = <đường dẫn đến thư mục addons> (mặc định là "addons")
```
Có thể kế thừa từ **odoo.conf.template**

Ngoài ra có thể thêm mổ số parameters như:

```
-c _<đường dẫn đến tệp odoo.conf>_
-u _<tên addons>_ giúp cập nhật addons đó trước khi khởi chạy
-d _<tên database>_ giúp chỉ rõ tên database được sử dụng
--dev=all giúp bật chế độ nhà phát triển 
```

# 4. Chạy hệ thống và cài đặt các ứng dụng cần thiết

Sau khi cài đặt và thiết lập đây đủ, ngươi sử dụng nhấn nút Run trên PyCharm (hoặc Shift+f10) để khởi chạy hệ thống.

Người sử dụng truy cập theo đường dẫn _http://localhost:8069/_ để đăng nhập vào hệ thống.

Hoàn tất
    
