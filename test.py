# import os
# import re
# import unicodedata
# import shutil

# # Đường dẫn đầy đủ
# pdf_folder = "/root/FE/recruitment-api/file_pdf_word/output_cv_pdf"
# word_folder = "/root/FE/recruitment-api/file_pdf_word/output_cv_word"
# cv_folder = "/root/FE/recruitment-api/cv_files"

# # Hàm chuẩn hoá tên file (VD: Đặng → Dang)
# def normalize_filename(filename):
#     name, ext = os.path.splitext(filename)

#     # Thay thế đặc biệt trước khi remove dấu
#     name = name.replace("Đ", "D").replace("đ", "d")

#     # Remove dấu các ký tự khác
#     normalized = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')

#     # Thay thế khoảng trắng bằng dấu _
#     normalized = re.sub(r"\s+", "_", normalized.strip())

#     return normalized + ext


# # Bước 1: XÓA HẾT FILE HIỆN TẠI TRONG FOLDER cv_files
# deleted = 0
# for file in os.listdir(cv_folder):
#     file_path = os.path.join(cv_folder, file)
#     try:
#         os.remove(file_path)
#         deleted += 1
#     except Exception as e:
#         print(f"❌ Lỗi xoá {file}: {e}")
# print(f"🗑️ Đã xoá {deleted} file trong thư mục cv_files.")

# # Bước 2: CHUYỂN FILE LẺ → .docx, FILE CHẴN → .pdf VÀ COPY VÀO cv_files
# index = 1
# moved = 0

# for folder in [pdf_folder, word_folder]:
#     files = sorted(os.listdir(folder))  # đảm bảo xử lý theo thứ tự
#     for file in files:
#         src = os.path.join(folder, file)
#         ext = ".docx" if index % 2 == 1 else ".pdf"
#         if not file.lower().endswith(ext):
#             index += 1
#             continue

#         # Chuẩn hoá tên file (Dang_Hoa_1.pdf)
#         new_name = normalize_filename(file)
#         dst = os.path.join(cv_folder, new_name)

#         try:
#             shutil.copy2(src, dst)
#             print(f"✅ Đã chuyển: {file} → {new_name}")
#             index += 1
#             moved += 1
#         except Exception as e:
#             print(f"❌ Không thể chuyển {file}: {e}")

# print(f"📁 Tổng số file đã chuyển vào cv_files: {moved}")

####################3
#CAP NHAT TEN FILE
from pymongo import MongoClient
import os
import re

client = MongoClient("mongodb://localhost:27017")
db = client["recruitment"]
collection = db["candidates"]

cv_folder = "cv_files"
files = sorted(os.listdir(cv_folder))  # Sắp xếp để giữ thứ tự

# Ánh xạ: số cuối file → tên file
file_mapping = {}
for file in files:
    match = re.search(r"_(\d+)\.(pdf|docx)$", file)
    if match:
        index = int(match.group(1))
        file_mapping[index] = file

# Lấy toàn bộ ứng viên theo thứ tự insert
docs = list(collection.find().sort("_id", 1))  # hoặc sort theo 'ngay_nop'

updated = 0
not_found = 0

for i, doc in enumerate(docs, 1):  # i = 1, 2, 3, ...
    filename = file_mapping.get(i)
    if filename:
        collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"cv_filepath": f"cv_files/{filename}"}}
        )
        print(f"✅ Cập nhật: {doc.get('ho_ten', 'Không rõ')} → {filename}")
        updated += 1
    else:
        print(f"❌ Không tìm thấy file cho ứng viên {i} ({doc.get('ho_ten', 'Không rõ')})")
        not_found += 1

print(f"\n🎯 Tổng cập nhật thành công: {updated}")
print(f"⚠️ Không tìm thấy file ứng với: {not_found} ứng viên")
