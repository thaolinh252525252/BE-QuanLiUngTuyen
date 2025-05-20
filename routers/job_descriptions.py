from fastapi import APIRouter, HTTPException, Body
from pymongo import MongoClient, errors
from bson import ObjectId
from datetime import datetime
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
collection = db["mo_ta_cong_viec"]

@router.get("/job-descriptions/")
def get_all_job_descriptions():
    try:
        docs = collection.find()
        result = []
        for doc in docs:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            result.append(doc)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi truy vấn JD: {e}")

@router.post("/job-descriptions/")
def add_job(job: dict):
    try:
        job["created_at"] = datetime.now()
        result = collection.insert_one(job)
        return {"message": "Đã thêm JD", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi thêm JD: {e}")

@router.put("/job-descriptions/{job_id}")
def update_job_description(job_id: str, data: dict = Body(...)):
    try:
        try:
            object_id = ObjectId(job_id)
        except errors.InvalidId:
            raise HTTPException(status_code=400, detail="ID không hợp lệ")

        job = collection.find_one({"_id": object_id})
        if not job:
            raise HTTPException(status_code=404, detail="Không tìm thấy mô tả công việc")

        collection.update_one(
            {"_id": object_id},
            {"$set": {
                "vi_tri": data.get("vi_tri", job.get("vi_tri", "")),
                "mo_ta": data.get("mo_ta", job.get("mo_ta", "")),
                "yeu_cau": data.get("yeu_cau", job.get("yeu_cau", "")),
                "han_nop": data.get("han_nop", job.get("han_nop", ""))
            }}
        )

        updated_job = collection.find_one({"_id": object_id})
        return {
            "id": str(updated_job["_id"]),
            "vi_tri": updated_job.get("vi_tri", ""),
            "mo_ta": updated_job.get("mo_ta", ""),
            "yeu_cau": updated_job.get("yeu_cau", ""),
            "han_nop": updated_job.get("han_nop", "")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi server: {e}")

@router.delete("/job-descriptions/{job_id}")
def delete_job_description(job_id: str):
    try:
        try:
            object_id = ObjectId(job_id)
        except errors.InvalidId:
            raise HTTPException(status_code=400, detail="ID không hợp lệ")

        result = collection.delete_one({"_id": object_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Không tìm thấy JD để xoá")

        return {"message": "Đã xoá JD", "id": job_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi xoá JD: {e}")
