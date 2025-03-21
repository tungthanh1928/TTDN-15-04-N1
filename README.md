# Hướng dẫn Cài đặt và Thiết lập Môi trường

## 1. Cài đặt công cụ, môi trường và các thư viện cần thiết

### 1.1. Clone Project
Đầu tiên, clone project từ GitHub:
<div class="code-block">
  <pre>
    <code>git clone https://github.com/tungthanh1928/TTDN-15-04-N1.git</code>
  </pre>
  <button onclick="copyCode('git clone https://github.com/tungthanh1928/TTDN-15-04-N1.git')"></button>
</div>

Di chuyển vào thư mục project:
<div class="code-block">
  <pre>
    <code>cd TTDN-15-04-N1</code>
  </pre>
  <button onclick="copyCode('cd TTDN-15-04-N1')"></button>
</div>

Chuyển sang nhánh cần làm việc:
<div class="code-block">
  <pre>
    <code>git checkout TTDN-15-04-N1</code>
  </pre>
  <button onclick="copyCode('git checkout TTDN-15-04-N1')"></button>
</div>

### 1.2. Cài đặt các thư viện cần thiết
Người sử dụng thực thi các lệnh sau để cài đặt các thư viện cần thiết:
<div class="code-block">
  <pre>
    <code>sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev</code>
  </pre>
  <button onclick="copyCode('sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev')"></button>
</div>

### 1.3. Khởi tạo môi trường ảo
Khởi tạo môi trường ảo và cài đặt các thư viện yêu cầu từ file `requirements.txt`:
<div class="code-block">
  <pre>
    <code>python3.10 -m venv ./venv</code>
  </pre>
  <button onclick="copyCode('python3.10 -m venv ./venv')"></button>
</div>

Kích hoạt môi trường ảo:
<div class="code-block">
  <pre>
    <code>source venv/bin/activate</code>
  </pre>
  <button onclick="copyCode('source venv/bin/activate')"></button>
</div>

Cài đặt các thư viện từ `requirements.txt`:
<div class="code-block">
  <pre>
    <code>pip3 install -r requirements.txt</code>
  </pre>
  <button onclick="copyCode('pip3 install -r requirements.txt')"></button>
</div>

## 2. Setup Database
Khởi tạo database trên Docker bằng việc thực thi file `docker-compose.yml`.

Cài đặt Docker Compose:
<div class="code-block">
  <pre>
    <code>sudo apt install docker-compose</code>
  </pre>
  <button onclick="copyCode('sudo apt install docker-compose')"></button>
</div>

Khởi động Docker Compose:
<div class="code-block">
  <pre>
    <code>sudo docker-compose up -d</code>
  </pre>
  <button onclick="copyCode('sudo docker-compose up -d')"></button>
</div>

## 3. Setup tham số chạy cho hệ thống

### 3.1. Khởi tạo `odoo.conf`


<<<<<<< HEAD


# 1. Cài đặt công cụ, môi trường và các thư viện cần thiết

## 1.1. Clone project.
git clone https://gitlab.com/anhlta/odoo-fitdnu.git
git checkout 

## 1.2. cài đặt các thư viện cần thiết

Người sử dụng thực thi các lệnh sau đề cài đặt các thư viện cần thiết

```
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
```
## 1.3. khởi tạo môi trường ảo.

`python3.10 -m venv ./venv`
Thay đổi trình thông dịch sang môi trường ảo và chạy requirements.txt để cài đặt tiếp các thư viện được yêu cầu

```
source venv/bin/activate
pip3 install -r requirements.txt
```

# 2. Setup database

Khởi tạo database trên docker bằng việc thực thi file dockercompose.yml.

`docker-compose up -d`

# 3. Setup tham số chạy cho hệ thống

## 3.1. Khởi tạo odoo.conf

Tạo tệp **odoo.conf** có nội dung như sau:

```
[options]
=======
Mở file `odoo.conf` để chỉnh sửa:
<div class="code-block">
  <pre>
    <code>nano odoo.conf</code>
  </pre>
  <button onclick="copyCode('nano odoo.conf')"></button>
</div>
 Tệp odoo.conf có nội dung như sau:
<div class="code-block">
  <pre>
    <code>[options]
>>>>>>> phuc
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5434
xmlrpc_port = 8069</code>
  </pre>
  <button onclick="copyCode('[options]\naddons_path = addons\ndb_host = localhost\ndb_password = odoo\ndb_user = odoo\ndb_port = 5434\nxmlrpc_port = 8069')"></button>
</div>


## 4. Chạy hệ thống và cài đặt các ứng dụng cần thiết

Chạy hệ thống Odoo và cài đặt các ứng dụng:
<div class="code-block">
  <pre>
    <code>python3 odoo-bin.py -c odoo.conf -u all</code>
  </pre>
  <button onclick="copyCode('python3 odoo-bin.py -c odoo.conf -u all')"></button>
</div>
