from fastapi import APIRouter, BackgroundTasks
from pymongo import MongoClient
from services.email_processor import process_all_emails
from dotenv import load_dotenv
import os
router = APIRouter()

load_dotenv()

# Lấy chuỗi kết nối từ biến môi trường
mongo_uri = os.environ.get("Mongo_connect")
if not mongo_uri:
    raise ValueError("Biến 'Mongo_connect' không được thiết lập trong file .env")

# Kết nối tới MongoDB
client = MongoClient(mongo_uri)
db = client["tuyendung"]
collection = db["ung_vien"]

@router.post("/process-emails/")
def trigger_email_scan(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_all_emails, mongo_collection=collection)
    return {"message": "Đã bắt đầu quét email ứng tuyển"}
@router.get("/email-test")
def test_email():
    return {"status": "OK"}
