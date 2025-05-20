# Sử dụng image Python chính thức
FROM python:3.9-slim

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Cài đặt các gói hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    python3-distutils \
    python3-apt \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && apt-get clean

# Tạo thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt vào container
COPY requirements.txt /app/

# Cài đặt các thư viện từ requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . /app/

# Chạy ứng dụng
CMD ["python", "main.py"]
