Hướng dẫn Cài đặt và Thiết lập Môi trường
1. Cài đặt công cụ, môi trường và các thư viện cần thiết
1.1. Clone Project
Đầu tiên, clone project từ GitHub:

bash
Copy
Edit
git clone https://github.com/tungthanh1928/TTDN-15-04-N1.git
Di chuyển vào thư mục project:

bash
Copy
Edit
cd TTDN-15-04-N1
Chuyển sang nhánh cần làm việc:

bash
Copy
Edit
git checkout TTDN-15-04-N1
1.2. Cài đặt các thư viện cần thiết
Người sử dụng thực thi các lệnh sau để cài đặt các thư viện cần thiết:

bash
Copy
Edit
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
1.3. Khởi tạo môi trường ảo
Khởi tạo môi trường ảo và cài đặt các thư viện yêu cầu từ file requirements.txt:

bash
Copy
Edit
python3.10 -m venv ./venv
Kích hoạt môi trường ảo:

bash
Copy
Edit
source venv/bin/activate
Cài đặt các thư viện từ requirements.txt:

bash
Copy
Edit
pip3 install -r requirements.txt
2. Setup Database
Khởi tạo database trên Docker bằng việc thực thi file docker-compose.yml.

Cài đặt Docker Compose:

bash
Copy
Edit
sudo apt install docker-compose
Khởi động Docker Compose:

bash
Copy
Edit
sudo docker-compose up -d
3. Setup tham số chạy cho hệ thống
3.1. Khởi tạo odoo.conf
Tạo tệp odoo.conf trong thư mục gốc với nội dung sau:

bash
Copy
Edit
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5434
xmlrpc_port = 8069
4. Chạy hệ thống và cài đặt các ứng dụng cần thiết
Chạy hệ thống Odoo và cài đặt các ứng dụng:

bash
Copy
Edit
python3 odoo-bin.py -c odoo.conf -u all
Sau khi hoàn tất, bạn có thể truy cập hệ thống qua đường dẫn:

arduino
Copy
Edit
http://localhost:8069/
Đăng nhập vào hệ thống và hoàn tất thiết lập.

