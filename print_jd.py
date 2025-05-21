# from pymongo import MongoClient

# client = MongoClient("mongodb://localhost:27017/")
# db = client["tuyendung"]
# collection = db["ung_vien"]

# print("📋 Danh sách ứng viên trong 'ung_vien':")
# for doc in collection.find():
#     print("=" * 60)
#     print(f"Họ tên       : {doc.get('ho_ten', '')}")
#     print(f"Email        : {doc.get('email', '')}")
#     print(f"Vị trí       : {doc.get('vi_tri_ung_tuyen', '')}")
#     print(f"Điểm phù hợp : {doc.get('diem_phu_hop', 0)}")
#     print(f"Nhan_xet : {doc.get('nhan_xet', '')}")
#     print(f"Kỹ năng      : {', '.join(doc.get('ky_nang', []))}")
#     print(f"Ngày nộp     : {doc.get('ngay_nop', '')}")
#     print(f"cv_filepath     : {doc.get('cv_filepath', '')}")
#     # Chứng chỉ
#     print("kỹ năng        :")
#     ky_nang_list = doc.get("ky_nang", [])

#     if not isinstance(ky_nang_list, list):
#         ky_nang_list = [ky_nang_list]  # biến thành list dù ban đầu là chuỗi hoặc None

#     for d in ky_nang_list:
#         if isinstance(d, dict):
#             ten = d.get("ten_du_an", "")
#             vai_tro = d.get("vai_tro", "")
#             tg = d.get("thoi_gian", "")
#             mo_ta = d.get("mo_ta", "")
#             print(f"  - {ten} ({tg}) - {vai_tro}")
#             print(f"    {mo_ta}")
#         else:
#             print(f"  - {d}")  # in chuỗi nếu không phải dict
#     print("Chứng chỉ    :")
#     for c in doc.get("chung_chi", []):
#         print(f"  - {c}")
    
#     # Giải thưởng
#     print("Giải thưởng  :")
#     for g in doc.get("giai_thuong", []):
#         print(f"  - {g}")
    
#     # Dự án
#     print("Dự án        :")
#     du_an_list = doc.get("du_an", [])

#     if not isinstance(du_an_list, list):
#         du_an_list = [du_an_list]  # biến thành list dù ban đầu là chuỗi hoặc None

#     for d in du_an_list:
#         if isinstance(d, dict):
#             ten = d.get("ten_du_an", "")
#             vai_tro = d.get("vai_tro", "")
#             tg = d.get("thoi_gian", "")
#             mo_ta = d.get("mo_ta", "")
#             print(f"  - {ten} ({tg}) - {vai_tro}")
#             print(f"    {mo_ta}")
#         else:
#             print(f"  - {d}")  # in chuỗi nếu không phải dict
#     # print("Dự án        :")
#     # du_an_list = doc.get("du_an", [])

#     # if not isinstance(du_an_list, list):
#     #     du_an_list = [du_an_list]  # biến thành list dù ban đầu là chuỗi hoặc None

#     #     for d in du_an_list:
#     #         if isinstance(d, dict):
#     #             ten = d.get("ten_du_an", "")
#     #             vai_tro = d.get("vai_tro", "")
#     #             tg = d.get("thoi_gian", "")
#     #             mo_ta = d.get("mo_ta", "")
#     #             print(f"  - {ten} ({tg}) - {vai_tro}")
#     #             print(f"    {mo_ta}")
#     #         else:
#     #             print(f"  - {d}")  # in chuỗi nếu không phải dict
#         # In chứng chỉ
#     # print("Chứng chỉ    :")
#     # for c in doc.get("chung_chi", []):
#     #     print(f"  - {c.get('ten_chung_chi')} ({c.get('nam_cap')})")

#     # In giải thưởng
#     # print("Chứng chỉ    :")
#     # for c in doc.get("chung_chi", []):
#     #     if isinstance(c, dict):
#     #         print(f"  - {c.get('ten_chung_chi')} ({c.get('nam_cap')})")
#     #     else:
#     #         print(f"  - {c}")  # fallback nếu là chuỗi

#     # print("Giải thưởng  :")
#     # for g in doc.get("giai_thuong", []):
#     #     if isinstance(g, dict):
#     #         print(f"  - {g.get('noi_dung')} ({g.get('nam')})")
#     #     else:
#     #         print(f"  - {g}")

#     # print("Dự án        :")
#     # for d in doc.get("du_an", []):
#     #     if isinstance(d, dict):
#     #         print(f"  - {d.get('ten')} ({d.get('thoi_gian')}) - {d.get('vai_tro')}")
#     #         print(f"    {d.get('mo_ta')}")
#     #         for cv in d.get("cong_viec", []):
#     #             print(f"    • {cv}")
#     #     else:
#     #         print(f"  - {d}")

#     # # In dự án
#     # print("Dự án        :")
#     # for d in doc.get("du_an", []):
#     #     print(f"  - {d.get('ten')} ({d.get('thoi_gian')}) - {d.get('vai_tro')}")
#     #     print(f"    {d.get('mo_ta')}")
#     #     for cv in d.get("cong_viec", []):
#     #         print(f"    • {cv}")

# #############################################################3
# # collection = db["mo_ta_cong_viec"]

# # print("📋 Danh sách ứng viên trong 'ung_vien':")
# # for doc in collection.find():
# #     print("=" * 60)
# #     print(f"vi_tri      : {doc.get('vi_tri', '')}")
# #     print(f"mo_ta       : {doc.get('mo_ta', '')}")
# #     print(f"yeu_cau       : {doc.get('yeu_cau', '')}")
# #     print(f"han_nop : {doc.get('han_nop')}")