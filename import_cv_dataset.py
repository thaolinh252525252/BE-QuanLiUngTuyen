# import os
# import re
# import unicodedata
# import json
# import google.generativeai as genai
# from datetime import datetime
# from pymongo import MongoClient

# # Cấu hình API key cho Gemini (thay bằng API key thực tế của bạn)
# genai.configure(api_key="AIzaSyAVZplOCSPwJpdtnSeHfPDNstBze_gUZ2Y")


# # Hàm từ code cũ (đã được sao chép)
# def safe_filename(filename):
#     filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('utf-8')
#     filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
#     return filename

# def list_cv_files(cv_dir="/root/FE/recruitment-api/cv_files"):
#     cv_files = {}
#     for filename in os.listdir(cv_dir):
#         if filename.endswith((".pdf", ".docx")):
#             match = re.match(r"(.+)_(\d+)\.(pdf|docx)$", filename)
#             if match:
#                 base_name, index, extension = match.groups()
#                 index = int(index)
#                 filepath = os.path.join(cv_dir, filename)
#                 relative_path = os.path.relpath(filepath, start=os.path.dirname(cv_dir))
#                 cv_files[index] = {
#                     "filename": filename,
#                     "filepath": relative_path,
#                     "extension": extension,
#                     "base_name": base_name
#                 }
#     return cv_files

# def extract_text_from_file(filepath):
#     if filepath.endswith(".pdf"):
#         from PyPDF2 import PdfReader
#         reader = PdfReader(filepath)
#         text = ""
#         for page in reader.pages:
#             text += page.extract_text() or ""
#         return text
#     elif filepath.endswith(".docx"):
#         from docx import Document
#         doc = Document(filepath)
#         text = "\n".join([para.text for para in doc.paragraphs])
#         return text
#     return ""

# def normalize_position(position):
#     if not position:
#         return "Vị trí chưa xác định"
#     position = unicodedata.normalize("NFKC", position).strip().lower()
#     position = re.sub(r"ứng tuyển vị trí\s*|apply for\s*|vị trí\s*:", "", position)
#     position = re.sub(r"\s*-\s*.+$", "", position)
#     position = re.sub(r"\s+", " ", position)
#     mappings = {
#         r"devops|ansible|jenkins|terraform|prometheus|grafana|cicd|ci/cd": "ky su devops",
#         r"kinh doanh|sales": "nhan vien kinh doanh",
#         r"ha tang|network|infrastructure": "ky su ha tang",
#         r"lap trinh vien|developer|python": "lap trinh vien python",
#         r"phan tich du lieu|data analyst": "chuyen vien phan tich du lieu"
#     }
#     for pattern, normalized in mappings.items():
#         if re.search(pattern, position, re.IGNORECASE):
#             return normalized
#     return position.title()

# def normalize_text(text):
#     if not text:
#         return ""
#     text = unicodedata.normalize("NFKC", text)
#     text = text.encode("ascii", "ignore").decode("utf-8")
#     return re.sub(r"\s+", " ", text).strip().lower()

# def extract_info_with_gemini(text, filename, subject, jd):
#     if not jd:
#         print("⚠️ Không có JD phù hợp — để Gemini tự phân tích vị trí")
#         jd = {
#             "vi_tri": "Không xác định",
#             "mo_ta": "Không có mô tả cụ thể",
#             "yeu_cau": "Không rõ yêu cầu"
#         }
#         fallback_mode = True
#     else:
#         fallback_mode = False

#     def safe_string(value):
#         if not isinstance(value, str):
#             value = str(value)
#         return value.replace("{", "{{").replace("}", "}}").strip()

#     vi_tri = safe_string(jd.get("vi_tri", ""))
#     mo_ta = safe_string(jd.get("mo_ta", ""))
#     yeu_cau = safe_string(jd.get("yeu_cau", ""))

#     jd_section = f"""
# - Tự đánh giá xem vị trí ứng tuyển có khớp với JD hay không, không cần chuẩn hóa trước.
# - So sánh kỹ năng, kinh nghiệm, chứng chỉ, giải thưởng, dự án, trình độ học vấn với JD:

# [Mô tả công việc]
# - Vị trí: {vi_tri}
# - Mô tả: {mo_ta}
# - Yêu cầu: {yeu_cau}

# **Hướng dẫn so sánh và tính điểm**:
# 1. **Kỹ năng (40%)**: Đếm số kỹ năng trong CV khớp với `yeu_cau`. Tính tỷ lệ kỹ năng khớp (số kỹ năng khớp / tổng kỹ năng yêu cầu) và nhân với 40.
# 2. **Kinh nghiệm (30%)**: Đánh giá số năm kinh nghiệm hoặc số dự án liên quan. Nếu kinh nghiệm >= yêu cầu, cho 30 điểm; nếu đạt 50–99% yêu cầu, cho 15–29 điểm; nếu <50%, cho 0–14 điểm.
# 3. **Học vấn và chứng chỉ (20%)**: Nếu trình độ học vấn hoặc chứng chỉ khớp với yêu cầu, cho 20 điểm; nếu thiếu một phần, cho 0–19 điểm.
# 4. **Khác (10%)**: Dự án, giải thưởng hoặc các yếu tố khác liên quan đến JD, tối đa 10 điểm.
# 5. Tổng điểm (`diem_phu_hop`) từ 0–100
# 6. Nếu vị trí ứng tuyển không khớp với JD, trả về `nhan_xet`: "Hiện không có JD phù hợp với vị trí này" và `diem_phu_hop` tối đa 50.
# """

#     prompt = f"""
# Bạn là AI chuyên gia tuyển dụng. Dựa trên CV và JD, hãy trích xuất thông tin theo mẫu JSON sau và đánh giá mức độ phù hợp.

# **Văn bản CV**:
# {text}

# **Trả về JSON chuẩn sau**:
# {{
#   "ho_ten": "",
#   "so_dien_thoai": "",
#   "ngay_sinh": "",
#   "que_quan": "",
#   "noi_o": "",
#   "trinh_do_hoc_van": [],
#   "kinh_nghiem": [],
#   "vi_tri_ung_tuyen": "",
#   "ky_nang": [],
#   "chung_chi": [],
#   "giai_thuong": [],
#   "du_an": [],
#   "trang_thai": "",
#   "diem_phu_hop": 0,
#   "nhan_xet": "",
#   "muc_tieu_nghe_nghiep": "",
#   "so_thich": [],
#   "nguoi_gioi_thieu": [],
#   "hoat_dong": []
# }}

# **Lưu ý**:
# - Chỉ trả về đúng JSON, không thêm mô tả ngoài.
# - `diem_phu_hop` phải từ 0–100, tính theo hướng dẫn trên.
# - `nhan_xet` phải nêu rõ những điểm CV còn thiếu so với JD và gợi ý cải thiện. Nếu vị trí không khớp, ghi "Hiện không có JD phù hợp với vị trí này".
# - Không điền thông tin nếu không có trong CV.
# - Các trường mới như `muc_tieu_nghe_nghiep`, `so_thich`, `nguoi_gioi_thieu`, `hoat_dong` chỉ điền nếu có dữ liệu trong CV.
# - ⚠️ Lưu ý: Vì không tìm thấy JD phù hợp nên bạn phải tự xác định vị trí ứng tuyển từ nội dung CV. Nếu không xác định được, hãy để trống trường `vi_tri_ung_tuyen`. Trong mọi trường hợp, `nhan_xet` phải ghi rõ 'Không tìm thấy JD phù hợp' và điểm tối đa không vượt quá 50.
# {jd_section}
# """

#     try:
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         response = model.generate_content(prompt)
#         print("📜 Phản hồi thô từ Gemini:", response.text)

#         text = response.text.strip()
#         if "```" in text:
#             parts = [part for part in text.split("```") if "{" in part]
#             raw_json = parts[0] if parts else text
#         else:
#             raw_json = text

#         match = re.search(r"\{.*\}", raw_json, re.DOTALL)
#         if not match:
#             print("❌ Không tìm thấy JSON hợp lệ trong phản hồi Gemini")
#             return None

#         result = json.loads(match.group())

#         if "diem_phu_hop" not in result or not isinstance(result["diem_phu_hop"], (int, float)):
#             print("❌ Gemini không trả về trường 'diem_phu_hop' hợp lệ, trả về giá trị mặc định")
#             result["diem_phu_hop"] = 0
#             result["nhan_xet"] = "Không thể đánh giá mức độ phù hợp do thiếu thông tin từ Gemini."

#         return result

#     except Exception as e:
#         print(f"❌ Lỗi khi gọi Gemini: {e}")
#         import traceback
#         traceback.print_exc()
#         return None

# # Hàm cập nhật để lấy JD từ collection mo_ta_cong_viec
# import os
# import json
# from datetime import datetime
# import re
# import unicodedata

# def safe_filename(name: str) -> str:
#     name = name.replace("Đ", "D").replace("đ", "d")
#     name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')
#     return re.sub(r'[^a-zA-Z0-9_.-]', '_', name)

# def insert_json_to_ung_vien(mongo_collection, json_data):
#     from_email = json_data["thong_tin_ca_nhan"].get("email", "no_email@example.com")
#     subject = f"Ứng tuyển vị trí {json_data['chuc_danh']} - {json_data['ho_ten']}"
#     index = json_data.get("index", 1)
#     ho_ten_norm = safe_filename(json_data["ho_ten"])

#     # 🔍 Tên file có dạng: Ho_Ten_Index.pdf hoặc .docx
#     filepath_pdf = f"cv_files/{ho_ten_norm}_{index}.pdf"
#     filepath_docx = f"cv_files/{ho_ten_norm}_{index}.docx"

#     if os.path.exists(filepath_pdf):
#         cv_filepath = filepath_pdf
#     elif os.path.exists(filepath_docx):
#         cv_filepath = filepath_docx
#     else:
#         print(f"❌ Không tìm thấy file CV phù hợp cho: {ho_ten_norm}_{index}")
#         cv_filepath = ""

#     # 🧠 Tạo văn bản CV từ JSON (không cần đọc file)
#     text = json.dumps(json_data, ensure_ascii=False, indent=2)

#     # 🔍 Lấy JD từ vị trí
#     jd_collection = mongo_collection.database["mo_ta_cong_viec"]
#     jd_docs = list(jd_collection.find({}, {"vi_tri": 1, "mo_ta": 1, "yeu_cau": 1, "han_nop": 1}))
#     vi_tri_chuan = json_data["chuc_danh"].strip().lower()
#     print("vi tri chuan: ",vi_tri_chuan)
#     # Tìm JD gần đúng thay vì phải khớp tuyệt đối
#     matched_jd = None
#     for doc in jd_docs:
#         print("📋 Danh sách JD trong MongoDB:")
#         for jd in jd_docs:
#             print("-", jd["vi_tri"])

#         # ten_jd = doc["vi_tri"].strip().lower()
#         # print("vi tri:" , ten_jd)

#         # if vi_tri_chuan in ten_jd or ten_jd in vi_tri_chuan or vi_tri_chuan.startswith(ten_jd) or ten_jd.startswith(vi_tri_chuan):
#         #     print("vi tri trong mo ta cong viec ",ten_jd)
#         #     matched_jd = doc
#         #     break



#     # 🤖 Gọi Gemini xử lý
#     info = extract_info_with_gemini(text, os.path.basename(cv_filepath), subject, matched_jd)
#     if not info:
#         print(f"❌ Không thể trích xuất thông tin từ Gemini cho {ho_ten_norm}")
#         return

#     # 📝 Tạo document lưu vào MongoDB
#     doc = {
#         "ho_ten": info.get("ho_ten", json_data["ho_ten"]),
#         "email": from_email,
#         "so_dien_thoai": info.get("so_dien_thoai", json_data["thong_tin_ca_nhan"].get("so_dien_thoai", "")),
#         "ngay_sinh": info.get("ngay_sinh", json_data["thong_tin_ca_nhan"].get("ngay_sinh", "")),
#         "que_quan": info.get("que_quan", json_data["thong_tin_ca_nhan"].get("dia_chi", "")),
#         "noi_o": info.get("noi_o", json_data["thong_tin_ca_nhan"].get("dia_chi", "")),
#         "trinh_do_hoc_van": info.get("trinh_do_hoc_van", [f"{hv.get('nganh', '')} tại {hv.get('truong', '')}" for hv in json_data.get("hoc_van", [])]),
#         "kinh_nghiem": info.get("kinh_nghiem", [
#             {
#                 "cong_ty": kn.get("cong_ty", ""),
#                 "thoi_gian": kn.get("thoi_gian", ""),
#                 "chuc_vu": kn.get("chuc_danh", ""),
#                 "mo_ta": "\n".join(kn.get("mo_ta", []))
#             } for kn in json_data.get("kinh_nghiem_lam_viec", [])
#         ]),
#         "vi_tri_ung_tuyen": info.get("vi_tri_ung_tuyen", matched_jd["vi_tri"] if matched_jd else vi_tri_chuan),
#         "ky_nang": info.get("ky_nang", json_data.get("ky_nang", [])),
#         "chung_chi": info.get("chung_chi", [cc.get("noi_dung", "") for cc in json_data.get("chung_chi", [])]),
#         "giai_thuong": info.get("giai_thuong", [gt.get("noi_dung", "") for gt in json_data.get("danh_hieu_giai_thuong", [])]),
#         "du_an": info.get("du_an", [
#             {
#                 "ten_du_an": da.get("ten", ""),
#                 "cong_ty": da.get("cong_ty", ""),
#                 "nam": da.get("thoi_gian", ""),
#                 "mo_ta": f"{da.get('mo_ta', '')}\n{'Công việc: ' + ', '.join(da.get('cong_viec', [])) if da.get('cong_viec') else ''}"
#             } for da in json_data.get("du_an", [])
#         ]),
#         "trang_thai": json_data.get("trang_thai", "Đang ứng tuyển"),
#         "trang_thai_gui_email": "Chưa gửi",
#         "ngay_nop": datetime.now(),
#         "diem_phu_hop": int(info.get("diem_phu_hop", 0)),
#         "nhan_xet": info.get("nhan_xet", ""),
#         "cv_filepath": cv_filepath,
#         "ngay_gui": datetime.now(),
#         "muc_tieu_nghe_nghiep": info.get("muc_tieu_nghe_nghiep", json_data.get("muc_tieu_nghe_nghiep", "")),
#         "so_thich": info.get("so_thich", json_data.get("so_thich", [])),
#         "nguoi_gioi_thieu": info.get("nguoi_gioi_thieu", [
#             {
#                 "ten": ng.get("ten", ""),
#                 "chuc_danh": ng.get("chuc_danh", ""),
#                 "email": ng.get("email", ""),
#                 "so_dien_thoai": ng.get("dien_thoai", "")
#             } for ng in json_data.get("nguoi_gioi_thieu", [])
#         ]),
#         "hoat_dong": info.get("hoat_dong", [
#             {
#                 "noi_dung": f"{hd.get('vi_tri', '')} tại {hd.get('to_chuc', '')} ({hd.get('thoi_gian', '')}): {', '.join(hd.get('mo_ta', []))}"
#             } for hd in json_data.get("hoat_dong", [])
#         ])
#     }

#     # ✅ Lưu vào collection 'ung_tuyen'
#     db = mongo_collection.database
#     db["ung_tuyen"].insert_one(doc)
#     print(f"✅ Đã lưu ứng viên: {doc['ho_ten']} (file: {cv_filepath}, điểm: {doc['diem_phu_hop']})")

# # Ví dụ sử dụng (dùng JSON của Hoàng Minh Trí)
# if __name__ == "__main__":
#     # Kết nối MongoDB
#     client = MongoClient("mongodb://localhost:27017/")
#     db = client["recruitment_db"]
#     mongo_collection = db["mo_ta_cong_viec"]  # dùng để tra JD; lưu sang "ung_tuyen"

#     # Đọc danh sách ứng viên từ file JSON
#     with open("/root/FE/recruitment-api/cv_dataset_1000_full_updated.json", "r", encoding="utf-8") as f:
#         danh_sach = json.load(f)

#     # Lặp và xử lý từng ứng viên
#     # Lặp và xử lý từng ứng viên, tăng chỉ số index
#     for i, ung_vien in enumerate(danh_sach, start=1):
#         try:
#             ung_vien["index"] = i  # ✅ Gán index cho từng ứng viên
#             insert_json_to_ung_vien(mongo_collection, ung_vien)
#         except Exception as e:
#             print(f"❌ Lỗi xử lý ứng viên {ung_vien.get('ho_ten', '')}: {e}")
