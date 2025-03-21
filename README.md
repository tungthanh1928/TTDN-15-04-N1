# 1. Giới thiệu về dự án Quản lý dự án
### Dự án quản lý dự án là một hệ thống hỗ trợ quản lý và theo dõi các dự án. Dưới đây là mô tả tổng quan về các chức năng chính của dự án:
1. Danh sách dự án
- Hiển thị tất cả các dự án hiện có.
- Cho phép người dùng xem thông tin chi tiết về từng dự án.
2. Phân bố trạng thái dự án
- Quản lý và theo dõi trạng thái của từng dự án (ví dụ: đang thực hiện, hoàn thành, tạm hoãn).
- Cung cấp cái nhìn tổng quan về tiến độ của các dự án.
3. Tiến độ hoàn thành các dự án
- Hiển thị tiến độ hiện tại của từng dự án.
- Ghi nhận và báo cáo về mức độ hoàn thành dự án để các bên liên quan có thể theo dõi.
4. Phân bố công việc dự án
- Chia sẻ và phân công công việc cho các thành viên trong nhóm.
- Quản lý các nhiệm vụ và đảm bảo rằng các công việc được thực hiện đúng thời hạn.
5. Tổng chi phí từng dự án
- Theo dõi chi phí phát sinh của từng dự án.
- Cung cấp báo cáo về chi phí để giúp người quản lý dễ dàng kiểm soát ngân sách dự án.
6. Báo cáo dự án
- Cung cấp các báo cáo chi tiết về tình hình dự án.
- Giúp các bên liên quan có cái nhìn tổng quan và đưa ra quyết định hợp lý.


![alt text](image-1.png)
![alt text](image-2.png)
![alt text](image-3.png)
![alt text](image-4.png)
![alt text](image-5.png)
![alt text](image-6.png)






# 2. Cài đặt công cụ, môi trường và các thư viện cần thiết

### 2.1. Clone project.

```
git clone https://github.com/nguyenngocdantruong/TTDN-15-04-N6.git
git checkout 
```

### 2.2. cài đặt các thư viện cần thiết

Người sử dụng thực thi các lệnh sau đề cài đặt các thư viện cần thiết

```
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
```
### 2.3. khởi tạo môi trường ảo.

Thay đổi trình thông dịch sang môi trường ảo và chạy requirements.txt để cài đặt tiếp các thư viện được yêu cầu
```
python3.10 -m venv ./venv
```
```
source venv/bin/activate
```
```
pip3 install -r requirements.txt
```

# 3. Setup database

Khởi tạo database trên docker bằng việc thực thi file dockercompose.yml.
```
sudo apt install docker-compose
```
```
sudo docker-compose up -d
```

# 4. Setup tham số chạy cho hệ thống

### 4.1. Khởi tạo odoo.conf

Tạo tệp **odoo.conf** có nội dung như sau:

```
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5434
xmlrpc_port = 8069
```

# 5. Chạy hệ thống và cài đặt các ứng dụng cần thiết

Lệnh chạy
```
python3 odoo-bin.py -c odoo.conf -u all
```


Người sử dụng truy cập theo đường dẫn _http://localhost:8069/_ để đăng nhập vào hệ thống.

Hoàn tất