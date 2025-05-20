from pymongo import MongoClient

# Kết nối tới MongoDB

client = MongoClient("mongodb+srv://thaolinh:Linlin2512%40@cluster0.nlpqh.mongodb.net/")
db = client["tuyendung"]

result = db["email_tracking"].delete_many({})
print("✅ Đã xoá", result.deleted_count, "email đã xử lý")



# # Xoá collection
# if "ung_vien" in db.list_collection_names():
#     db["ung_vien"].drop()
#     print("✅ Đã xoá collection 'ung_vien'")
# else:
#     print("⚠️ Collection 'ung_vien' không tồn tại.")

#Lay danh sach:
# from pymongo import MongoClient

# client = MongoClient("mongodb://localhost:27017/")
# db = client["tuyendung"]

# print("📦 Danh sách collection hiện có:")
# print(db.list_collection_names())
# Kết nối tới MongoDB
# client = MongoClient("mongodb://localhost:27017/")
# db = client["tuyendung"]


# from pymongo import MongoClient

# client = MongoClient("mongodb://localhost:27017")
# db = client["tuyendung"]  # hoặc tên database bạn đang dùng
# db["processed_emails"].delete_many({})  # Xóa toàn bộ UID đã xử lý

# print("✅ Đã xoá toàn bộ UID đã xử lý.")

# from pymongo import MongoClient

client = MongoClient("mongodb+srv://thaolinh:Linlin2512%40@cluster0.nlpqh.mongodb.net/")  # Điều chỉnh nếu backend dùng URI khác
db = client["tuyendung"]
collection = db["email_tracking"]

print("🔍 Số UID đã xử lý:", collection.count_documents({}))
result = collection.delete_many({})
print("🧹 Đã xóa", result.deleted_count, "UID đã xử lý.")

###Xoá collection
if "ung_vien" in db.list_collection_names():
    db["ung_vien"].drop()
    print("✅ Đã xoá collection 'ung_vien'")
else:
    print("⚠️ Collection 'ung_vien' không tồn tại.")


# result_mo_ta = db["mo_ta_cong_viec"].delete_many({})
# print("✅ Đã xoá", result_mo_ta.deleted_count, "mo ta cong viec")

