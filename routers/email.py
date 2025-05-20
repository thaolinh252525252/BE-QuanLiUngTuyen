from fastapi import APIRouter, BackgroundTasks
from pymongo import MongoClient
from services.email_processor import process_all_emails

router = APIRouter()

client = MongoClient("${import.meta.env.Mongo_connect}")
db = client["tuyendung"]
collection = db["ung_vien"]

@router.post("/process-emails/")
def trigger_email_scan(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_all_emails, mongo_collection=collection)
    return {"message": "Đã bắt đầu quét email ứng tuyển"}
@router.get("/email-test")
def test_email():
    return {"status": "OK"}
