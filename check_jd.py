from pymongo import MongoClient

def check_mongodb():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["tuyendung"]
        collection = db["mo_ta_cong_viec"]
        client.server_info()
        print("✅ Kết nối MongoDB thành công")
        count = collection.count_documents({})
        print(f"Số lượng JD trong mo_ta_cong_viec: {count}")
        jds = collection.find({})
        for jd in jds:
            print(jd)
    except Exception as e:
        print(f"❌ Lỗi MongoDB: {e}")

check_mongodb()