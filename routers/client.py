# file: routers/jobs.py (hoặc tương tự)
from fastapi import APIRouter
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException
from bson.errors import InvalidId
from dotenv import load_dotenv
import os

router = APIRouter()
# Tải biến môi trường từ file .env
load_dotenv()

# Lấy chuỗi kết nối từ biến môi trường
mongo_uri = os.environ.get("Mongo_connect")
if not mongo_uri:
    raise ValueError("Biến 'Mongo_connect' không được thiết lập trong file .env")

# Kết nối tới MongoDB
client = MongoClient(mongo_uri)
db = client["tuyendung"]
collection = db["mo_ta_cong_viec"]

@router.get("/jobs")
def get_jobs():
    jobs = []
    for job in collection.find({}, {"vi_tri": 1, "mo_ta": 1, "yeu_cau": 1, "han_nop": 1}):
        jobs.append({
            "id": str(job["_id"]),
            "vi_tri": job.get("vi_tri", ""),
            "mo_ta": job.get("mo_ta", ""),
            "yeu_cau": job.get("yeu_cau", ""),
            "han_nop": job.get("han_nop", "")  # đã là ISO 8601 nếu đúng chuẩn
        })
    return jobs



@router.get("/jobs/{job_id}")
def get_job_detail(job_id: str):
    try:
        if not ObjectId.is_valid(job_id):
            raise InvalidId
        job = collection.find_one({"_id": ObjectId(job_id)})
        if not job:
            raise HTTPException(status_code=404, detail="Không tìm thấy công việc")
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID không hợp lệ")

    return {
        "id": str(job["_id"]),
        "vi_tri": job.get("vi_tri", ""),
        "mo_ta": job.get("mo_ta", ""),
        "yeu_cau": job.get("yeu_cau", ""),
        "han_nop": job.get("han_nop", "")
    }
