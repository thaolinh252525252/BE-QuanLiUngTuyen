# from pymongo import MongoClient
# from datetime import datetime
# import logging

# # Cấu hình logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# try:
#     # Kết nối tới MongoDB
#     client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
#     client.server_info()  # Kiểm tra kết nối
#     logger.info("✅ Kết nối tới MongoDB thành công")
# except Exception as e:
#     logger.error(f"❌ Lỗi kết nối tới MongoDB: {str(e)}")
#     raise

# # Chọn database và collection
# db = client["tuyendung"]
# collection = db["mo_ta_cong_viec"]

# try:
#     # Xóa toàn bộ mô tả cũ (chỉ thực hiện nếu cần khởi tạo lại dữ liệu)
#     delete_confirm = input("Bạn có chắc chắn muốn xóa toàn bộ dữ liệu cũ trong collection 'mo_ta_cong_viec'? (y/n): ")
#     if delete_confirm.lower() == 'y':
#         result = collection.delete_many({})
#         logger.info(f"🗑️ Đã xóa {result.deleted_count} bản ghi cũ")
#     else:
#         logger.info("⛔ Không xóa dữ liệu cũ")

#     # Dữ liệu để chèn
#     job_descriptions = [
#         {
#             "vi_tri": "Lập trình viên Front-end",
#             "mo_ta": "Phát triển giao diện website với ReactJS, tối ưu hiệu suất và SEO",
#             "yeu_cau": "Kinh nghiệm 2 năm với ReactJS, Redux, TailwindCSS, hiểu RESTful API, CI/CD",
#             "han_nop": datetime(2025, 7, 30).isoformat()  # Chuyển thành chuỗi ISO để đồng nhất với API
#         },
#         {
#             "vi_tri": "Nhân viên Kinh doanh",
#             "mo_ta": "Tìm kiếm và phát triển khách hàng mới, duy trì mối quan hệ với khách hàng hiện tại, đạt chỉ tiêu doanh số được giao.",
#             "yeu_cau": "Kỹ năng giao tiếp, đàm phán, thuyết phục khách hàng; sử dụng thành thạo tin học văn phòng (Word, Excel); kinh nghiệm sử dụng CRM là lợi thế; khả năng lập kế hoạch và chịu áp lực công việc; trình độ tiếng Anh (TOEIC 600 trở lên) là điểm cộng.",
#             "han_nop": datetime(2025, 7, 30).isoformat()
#         },
#         {
#             "vi_tri": "Kỹ sư An toàn thông tin",
#             "mo_ta": "Phân tích và bảo vệ hệ thống CNTT khỏi các mối đe dọa an ninh mạng, triển khai các biện pháp bảo mật, giám sát và xử lý sự cố bảo mật.",
#             "yeu_cau": "Kinh nghiệm 2 năm trong lĩnh vực an toàn thông tin, thành thạo các công cụ như Wireshark, Metasploit, hiểu biết về firewall, IDS/IPS, có chứng chỉ như CEH, CISSP là lợi thế.",
#             "han_nop": datetime(2025, 7, 30).isoformat()
#         },
#         {
#             "vi_tri": "Lập trình viên Full-stack",
#             "mo_ta": "Phát triển cả giao diện người dùng (Front-end) và hệ thống backend cho các ứng dụng web, tích hợp API và cơ sở dữ liệu.",
#             "yeu_cau": "Kinh nghiệm 2-3 năm với Front-end (ReactJS, VueJS, TailwindCSS) và Backend (Node.js, Python, MongoDB hoặc PostgreSQL), hiểu biết về RESTful API, GraphQL, CI/CD.",
#             "han_nop": datetime(2025, 7, 30).isoformat()
#         },
#         {
#             "vi_tri": "Chuyên viên Kiểm thử phần mềm",
#             "mo_ta": "Chịu trách nhiệm kiểm thử và đảm bảo chất lượng các sản phẩm phần mềm. Phát hiện lỗi, báo cáo và theo dõi quá trình khắc phục. Xây dựng và thực hiện các kịch bản kiểm thử tự động và thủ công.",
#             "yeu_cau": "Có ít nhất 2 năm kinh nghiệm trong lĩnh vực kiểm thử phần mềm. Thành thạo các công cụ kiểm thử như Selenium, JUnit, TestNG. Hiểu biết về quy trình phát triển phần mềm Agile/Scrum. Kỹ năng phân tích và giải quyết vấn đề tốt.",
#             "han_nop": datetime(2025, 7, 20).isoformat()
#         },
#         {
#             "vi_tri": "Chuyên viên Phân tích Dữ liệu",
#             "mo_ta": "Thu thập, xử lý và phân tích dữ liệu để hỗ trợ ra quyết định kinh doanh. Xây dựng các báo cáo và dashboard trực quan hóa dữ liệu. Phát hiện xu hướng và đưa ra các đề xuất dựa trên dữ liệu.",
#             "yeu_cau": "Tốt nghiệp đại học chuyên ngành Toán, Thống kê, CNTT hoặc tương đương. Thành thạo SQL, Python/R và các công cụ phân tích dữ liệu như Pandas, NumPy. Kinh nghiệm với các công cụ BI như Power BI, Tableau. Kỹ năng truyền đạt thông tin và kể chuyện bằng dữ liệu.",
#             "han_nop": datetime(2025, 6, 20).isoformat()
#         },
#         {
#             "vi_tri": "Kỹ sư DevOps",
#             "mo_ta": "Xây dựng và duy trì cơ sở hạ tầng CI/CD. Tự động hóa quy trình triển khai và vận hành. Quản lý hệ thống cloud và container. Tối ưu hóa hiệu suất và độ tin cậy của hệ thống.",
#             "yeu_cau": "Kinh nghiệm 3+ năm với các công cụ CI/CD như Jenkins, GitLab CI. Thành thạo Docker, Kubernetes và các nền tảng cloud (AWS, Azure, GCP). Kiến thức về Infrastructure as Code (Terraform, Ansible). Kỹ năng scripting tốt (Bash, Python).",
#             "han_nop": datetime(2025, 7, 20).isoformat()
#         },
#         {
#             "vi_tri": "Kỹ sư Dữ liệu",
#             "mo_ta": "Thiết kế và xây dựng các hệ thống xử lý dữ liệu quy mô lớn. Phát triển và duy trì data pipeline. Tối ưu hóa lưu trữ và truy xuất dữ liệu. Đảm bảo chất lượng và tính nhất quán của dữ liệu.",
#             "yeu_cau": "Tốt nghiệp đại học chuyên ngành CNTT, Khoa học máy tính hoặc tương đương. Thành thạo các công nghệ Big Data như Hadoop, Spark, Kafka. Kinh nghiệm với các hệ thống cơ sở dữ liệu SQL và NoSQL. Kỹ năng lập trình tốt với Python, Scala hoặc Java.",
#             "han_nop": datetime(2025, 6, 20).isoformat()
#         },
#         {
#             "vi_tri": "Kỹ sư Hạ tầng Mạng",
#             "mo_ta": "Thiết kế, triển khai và bảo trì hệ thống mạng của công ty. Quản lý các thiết bị mạng như router, switch, firewall. Giải quyết sự cố và tối ưu hóa hiệu suất mạng. Đảm bảo tính khả dụng và an toàn của hệ thống mạng.",
#             "yeu_cau": "Có ít nhất 3 năm kinh nghiệm trong quản trị mạng. Có chứng chỉ CCNA, CCNP hoặc tương đương. Kiến thức sâu về các giao thức mạng, VPN, VLAN, routing và switching. Kinh nghiệm với các thiết bị của Cisco, Juniper hoặc các nhà cung cấp khác.",
#             "han_nop": datetime(2025, 6, 20).isoformat()
#         },
#         {
#             "vi_tri": "Kỹ sư Machine Learning",
#             "mo_ta": "Phát triển và triển khai các mô hình machine learning. Nghiên cứu và áp dụng các thuật toán mới. Tối ưu hóa hiệu suất của các mô hình. Hợp tác với các đội phát triển sản phẩm để tích hợp các giải pháp ML.",
#             "yeu_cau": "Tốt nghiệp Thạc sĩ trở lên về Khoa học Máy tính, Toán học hoặc lĩnh vực liên quan. Kinh nghiệm với các framework ML như TensorFlow, PyTorch, scikit-learn. Hiểu biết sâu về các thuật toán học máy và deep learning. Kỹ năng lập trình tốt với Python và các thư viện xử lý dữ liệu.",
#             "han_nop": datetime(2025, 7, 20).isoformat()
#         },
#         {
#             "vi_tri": "Kỹ sư Trí tuệ Nhân tạo",
#             "mo_ta": "Nghiên cứu và phát triển các giải pháp AI tiên tiến. Xây dựng các hệ thống thông minh có khả năng học hỏi và ra quyết định. Tích hợp các công nghệ AI vào sản phẩm của công ty. Theo dõi và áp dụng các xu hướng mới trong lĩnh vực AI.",
#             "yeu_cau": "Tốt nghiệp Tiến sĩ hoặc Thạc sĩ về AI, ML, Khoa học Máy tính. Kinh nghiệm nghiên cứu và phát triển trong lĩnh vực AI. Thành thạo các kỹ thuật xử lý ngôn ngữ tự nhiên, thị giác máy tính hoặc học tăng cường. Có các công bố khoa học là lợi thế.",
#             "han_nop": datetime(2025, 7, 20).isoformat()
#         },
#         {
#             "vi_tri": "Lập trình viên Python",
#             "mo_ta": "Phát triển và bảo trì các ứng dụng backend bằng Python. Thiết kế và triển khai các API RESTful. Tối ưu hóa hiệu suất và khả năng mở rộng của hệ thống. Viết unit test và đảm bảo chất lượng mã.",
#             "yeu_cau": "Có ít nhất 3 năm kinh nghiệm lập trình Python. Thành thạo các framework như Django, Flask hoặc FastAPI. Kinh nghiệm với cơ sở dữ liệu SQL và NoSQL. Hiểu biết về các nguyên tắc thiết kế phần mềm và mô hình kiến trúc.",
#             "han_nop": datetime(2025, 7, 20).isoformat()
#         }
#     ]

#     # Chèn dữ liệu vào collection
#     result = collection.insert_many(job_descriptions)
#     logger.info(f"✅ Đã chèn thành công {len(result.inserted_ids)} bản ghi vào collection 'mo_ta_cong_viec'")

#     # Kiểm tra số lượng bản ghi sau khi chèn
#     count = collection.count_documents({})
#     logger.info(f"📊 Tổng số bản ghi hiện tại trong collection: {count}")

# except Exception as e:
#     logger.error(f"❌ Lỗi khi chèn dữ liệu vào MongoDB: {str(e)}")
#     raise
# finally:
#     # Đóng kết nối
#     client.close()
#     logger.info("🔌 Đã đóng kết nối tới MongoDB")

# # # Thêm dữ liệu mới
# # collection.insert_many([
#     # {
#     #     "vi_tri": "Lập trình viên Python",
#     #     "mo_ta": "Tham gia phát triển hệ thống API phục vụ nền tảng học trực tuyến quy mô lớn. Làm việc cùng đội ngũ backend để tối ưu hiệu suất hệ thống.",
#     #     "yeu_cau": "Tốt nghiệp Đại học chuyên ngành CNTT. 2–3 năm kinh nghiệm phát triển Python (Flask hoặc FastAPI). Có kiến thức về cơ sở dữ liệu MongoDB, PostgreSQL. Hiểu biết về CI/CD và triển khai Docker là lợi thế.",
#     #     "han_nop": datetime(2025, 6, 30)
#     # },
#     # {
#     #     "vi_tri": "Chuyên viên Phân tích Dữ liệu",
#     #     "mo_ta": "Phân tích số liệu bán hàng, xây dựng báo cáo hỗ trợ ban lãnh đạo ra quyết định kinh doanh.",
#     #     "yeu_cau": "Tối thiểu 2 năm kinh nghiệm phân tích dữ liệu thực tế. Thành thạo SQL, Excel nâng cao, Power BI hoặc Tableau. Biết xử lý dữ liệu với Python (pandas, numpy). Tư duy logic và khả năng trình bày tốt.",
#     #     "han_nop": datetime(2025, 7, 10)
#     # },
#     # {
#     #     "vi_tri": "Chuyên viên Marketing Online",
#     #     "mo_ta": "Quản lý và triển khai các chiến dịch quảng cáo trên nền tảng Google Ads và Facebook.",
#     #     "yeu_cau": "1–3 năm kinh nghiệm chạy quảng cáo performance. Có hiểu biết về SEO, content marketing là lợi thế. Kỹ năng phân tích dữ liệu marketing tốt.",
#     #     "han_nop": datetime(2025, 6, 25)
#     # },
#     # {
#     #     "vi_tri": "Nhân viên Hành chính – Nhân sự",
#     #     "mo_ta": "Quản lý hồ sơ nhân sự, hỗ trợ tuyển dụng và chấm công lương thưởng.",
#     #     "yeu_cau": "Có kinh nghiệm 1 năm trở lên ở vị trí tương đương. Biết sử dụng phần mềm HRM như Bravo, BaseHR. Kỹ năng giao tiếp và xử lý tình huống tốt.",
#     #     "han_nop": datetime(2025, 6, 30)
#     # },
#     # {
#     #     "vi_tri": "UI/UX Designer",
#     #     "mo_ta": "Thiết kế giao diện người dùng cho website và ứng dụng mobile.",
#     #     "yeu_cau": "2+ năm kinh nghiệm thiết kế UI/UX. Sử dụng thành thạo Figma, Adobe XD. Có tư duy logic về luồng người dùng và trải nghiệm.",
#     #     "han_nop": datetime(2025, 7, 15)
#     # },
#     # {
#     #     "vi_tri": "Lập trình viên ReactJS",
#     #     "mo_ta": "Phát triển giao diện frontend tương tác cho các ứng dụng nội bộ.",
#     #     "yeu_cau": "Ít nhất 2 năm kinh nghiệm với ReactJS. Hiểu biết về Redux, Hooks, Context API. Biết dùng TailwindCSS là điểm cộng.",
#     #     "han_nop": datetime(2025, 7, 1)
#     # },
#     # {
#     #     "vi_tri": "DevOps Engineer",
#     #     "mo_ta": "Quản lý CI/CD pipeline, đảm bảo hệ thống hoạt động ổn định và có khả năng mở rộng.",
#     #     "yeu_cau": "2–4 năm kinh nghiệm triển khai DevOps. Thành thạo Docker, Jenkins, GitLab CI/CD. Biết dùng Kubernetes và giám sát Prometheus/Grafana.",
#     #     "han_nop": datetime(2025, 7, 20)
#     # },
#     # {
#     #     "vi_tri": "Chuyên viên Tư vấn Tuyển dụng",
#     #     "mo_ta": "Làm việc với các bộ phận để xác định nhu cầu tuyển dụng, triển khai quy trình phỏng vấn.",
#     #     "yeu_cau": "Tối thiểu 1 năm kinh nghiệm tuyển dụng. Kỹ năng giao tiếp, phỏng vấn ứng viên tốt. Biết sử dụng hệ thống ATS là lợi thế.",
#     #     "han_nop": datetime(2025, 6, 28)
#     # },
#     # {
#     #     "vi_tri": "Chuyên viên SEO Content",
#     #     "mo_ta": "Viết bài chuẩn SEO cho website, xây dựng nội dung phục vụ marketing.",
#     #     "yeu_cau": "Hiểu cơ bản về công cụ Google Search Console, Ahrefs. Có kinh nghiệm viết bài blog hoặc landing page. Biết viết nội dung chuyển đổi tốt.",
#     #     "han_nop": datetime(2025, 7, 12)
#     # },
#     # {
#     #     "vi_tri": "Chuyên viên Hỗ trợ Khách hàng",
#     #     "mo_ta": "Tiếp nhận, xử lý khiếu nại và hỗ trợ người dùng sử dụng sản phẩm dịch vụ.",
#     #     "yeu_cau": "1 năm kinh nghiệm CSKH. Giọng nói dễ nghe, thân thiện. Sử dụng thành thạo công cụ chat & CRM như Zendesk.",
#     #     "han_nop": datetime(2025, 7, 5)
#     # }
# # ])

# # print("✅ Đã chèn lại toàn bộ mô tả công việc")

# from pymongo import MongoClient
# from datetime import datetime
# import logging

# # Cấu hình logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("InitUsers")

# try:
#     # Kết nối MongoDB
#     client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
#     client.server_info()  # Kiểm tra kết nối
#     logger.info("✅ Kết nối tới MongoDB thành công")
# except Exception as e:
#     logger.error(f"❌ Lỗi kết nối MongoDB: {e}")
#     raise

# # Chọn database và collection
# from pymongo import MongoClient
# from datetime import datetime
# import logging

# # Cấu hình logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Kết nối MongoDB
# client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
# db = client["tuyendung"]
# collection = db["users"]

# try:
#     # Xác nhận xóa
#     confirm = input("Bạn có muốn xóa toàn bộ người dùng cũ? (y/n): ")
#     if confirm.lower() == "y":
#         deleted = collection.delete_many({})
#         logger.info(f"🗑️ Đã xóa {deleted.deleted_count} người dùng cũ")
#     else:
#         logger.info("❌ Không xóa người dùng cũ")

#     # Dữ liệu mẫu (bổ sung trường 'name')
#     user_data = [
#         {"username": "admin", "name": "Quản trị viên hệ thống", "role": "Quản trị viên", "created_at": datetime.now()},
#         {"username": "hr01", "name": "Nguyễn Văn A", "role": "Nhân sự", "created_at": datetime.now()},
#         {"username": "viewer01", "name": "Lê Thị B", "role": "Người xem", "created_at": datetime.now()},
#     ]

#     result = collection.insert_many(user_data)
#     logger.info(f"✅ Đã thêm {len(result.inserted_ids)} người dùng")

#     count = collection.count_documents({})
#     logger.info(f"📊 Tổng số người dùng: {count}")

# except Exception as e:
#     logger.error(f"❌ Lỗi khi khởi tạo dữ liệu người dùng: {e}")
#     raise
# finally:
#     client.close()
#     logger.info("🔌 Đã đóng kết nối MongoDB")
