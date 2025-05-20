import smtplib
from email.mime.text import MIMEText

# Cấu hình email
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "thaovuong669@gmail.com"
SENDER_PASSWORD = "wgam okla ffjk wxwy"

def generate_email_body(ho_ten, result):
    ho_ten = ho_ten or "bạn"

    if result == "Pass":
        return f"""\
Chào {ho_ten},

Cảm ơn bạn đã tham gia ứng tuyển và phỏng vấn tại công ty chúng tôi.

🎉 Chúng tôi rất vui thông báo rằng bạn đã **TRÚNG TUYỂN**. Bộ phận Nhân sự sẽ liên hệ để hướng dẫn thủ tục tiếp theo trong thời gian sớm nhất.

Chúc mừng bạn và hẹn gặp lại trong ngày làm việc đầu tiên!

Trân trọng,  
Phòng Nhân sự"""
    
    elif result == "Fail CV":
        return f"""\
Chào {ho_ten},

Cảm ơn bạn đã quan tâm và gửi hồ sơ ứng tuyển đến công ty chúng tôi.

Sau khi xem xét kỹ lưỡng hồ sơ của bạn, chúng tôi rất tiếc khi phải thông báo rằng bạn **chưa được chọn** vào vòng phỏng vấn lần này.

Mong rằng sẽ có cơ hội hợp tác trong tương lai.

Trân trọng,  
Phòng Nhân sự"""
    
    elif result == "Fail Interview":
        return f"""\
Chào {ho_ten},

Cảm ơn bạn đã tham gia buổi phỏng vấn tại công ty chúng tôi.

Sau khi tổng hợp kết quả, chúng tôi rất tiếc khi phải thông báo rằng bạn **chưa vượt qua vòng phỏng vấn**.

Chúng tôi đánh giá cao sự quan tâm và hy vọng được đồng hành cùng bạn trong những cơ hội sau.

Trân trọng,  
Phòng Nhân sự"""
    
    else:
        return f"""\
Chào {ho_ten},

Cảm ơn bạn đã ứng tuyển tại công ty chúng tôi.

Kết quả tuyển dụng của bạn hiện tại là: **{result}**.

Chúng tôi sẽ liên hệ nếu có cơ hội phù hợp hơn trong tương lai.

Trân trọng,  
Phòng Nhân sự"""

def send_result_email(to_email, ho_ten, result):
    subject = "Kết quả tuyển dụng"
    body = generate_email_body(ho_ten, result)

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"📧 Đã gửi email đến {to_email}")
    except Exception as e:
        print(f"❌ Gửi email thất bại: {e}")


def send_interview_email(to_email, ho_ten, date, time, location):
    subject = "Thông báo lịch phỏng vấn"
    body = f"""\
Chào {ho_ten or 'bạn'},

Chúc mừng! Hồ sơ của bạn đã được chọn để tiến hành phỏng vấn.

Thông tin buổi phỏng vấn:
- Ngày: {date}
- Giờ: {time}
- Địa điểm: {location}

Vui lòng có mặt đúng giờ. Nếu có thay đổi, vui lòng liên hệ với chúng tôi sớm nhất có thể.

Trân trọng,
Phòng Nhân sự
"""
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"📧 Đã gửi email lịch phỏng vấn đến {to_email}")
    except Exception as e:
        print(f"❌ Gửi email thất bại: {e}")
