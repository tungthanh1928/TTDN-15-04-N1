# Hướng dẫn Cài đặt và Thiết lập Môi trường

## 1. Cài đặt công cụ, môi trường và các thư viện cần thiết

### 1.1. Clone Project
Đầu tiên, clone project từ GitHub:
<div class="code-block">
  <pre>
    <code>git clone https://github.com/tungthanh1928/TTDN-15-04-N1.git</code>
  </pre>
  <button onclick="copyCode('git clone https://github.com/tungthanh1928/TTDN-15-04-N1.git')">Copy</button>
</div>

Di chuyển vào thư mục project:
<div class="code-block">
  <pre>
    <code>cd TTDN-15-04-N1</code>
  </pre>
  <button onclick="copyCode('cd TTDN-15-04-N1')">Copy</button>
</div>

Chuyển sang nhánh cần làm việc:
<div class="code-block">
  <pre>
    <code>git checkout TTDN-15-04-N1</code>
  </pre>
  <button onclick="copyCode('git checkout TTDN-15-04-N1')">Copy</button>
</div>

### 1.2. Cài đặt các thư viện cần thiết
Người sử dụng thực thi các lệnh sau để cài đặt các thư viện cần thiết:
<div class="code-block">
  <pre>
    <code>sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev</code>
  </pre>
  <button onclick="copyCode('sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev')">Copy</button>
</div>

### 1.3. Khởi tạo môi trường ảo
Khởi tạo môi trường ảo và cài đặt các thư viện yêu cầu từ file `requirements.txt`:
<div class="code-block">
  <pre>
    <code>python3.10 -m venv ./venv</code>
  </pre>
  <button onclick="copyCode('python3.10 -m venv ./venv')">Copy</button>
</div>

Kích hoạt môi trường ảo:
<div class="code-block">
  <pre>
    <code>source venv/bin/activate</code>
  </pre>
  <button onclick="copyCode('source venv/bin/activate')">Copy</button>
</div>

Cài đặt các thư viện từ `requirements.txt`:
<div class="code-block">
  <pre>
    <code>pip3 install -r requirements.txt</code>
  </pre>
  <button onclick="copyCode('pip3 install -r requirements.txt')">Copy</button>
</div>

## 2. Setup Database
Khởi tạo database trên Docker bằng việc thực thi file `docker-compose.yml`.

Cài đặt Docker Compose:
<div class="code-block">
  <pre>
    <code>sudo apt install docker-compose</code>
  </pre>
  <button onclick="copyCode('sudo apt install docker-compose')">Copy</button>
</div>

Khởi động Docker Compose:
<div class="code-block">
  <pre>
    <code>sudo docker-compose up -d</code>
  </pre>
  <button onclick="copyCode('sudo docker-compose up -d')">Copy</button>
</div>

## 3. Setup tham số chạy cho hệ thống

### 3.1. Khởi tạo `odoo.conf`
Tạo tệp `odoo.conf` trong thư mục gốc với nội dung sau:
<div class="code-block">
  <pre>
    <code>[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5434
xmlrpc_port = 8069</code>
  </pre>
  <button onclick="copyCode('[options]\naddons_path = addons\ndb_host = localhost\ndb_password = odoo\ndb_user = odoo\ndb_port = 5434\nxmlrpc_port = 8069')">Copy</button>
</div>

## 4. Chạy hệ thống và cài đặt các ứng dụng cần thiết

Chạy hệ thống Odoo và cài đặt các ứng dụng:
<div class="code-block">
  <pre>
    <code>python3 odoo-bin.py -c odoo.conf -u all</code>
  </pre>
  <button onclick="copyCode('python3 odoo-bin.py -c odoo.conf -u all')">Copy</button>
</div>

Sau khi hoàn tất, bạn có thể truy cập hệ thống qua đường dẫn:
