import schedule
import time
import logging
from pymongo import MongoClient
from services.email_processor import process_all_emails

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('app.log')]
)
logger = logging.getLogger(__name__)

def connect_to_mongodb():
    try:
        client = MongoClient("${import.meta.env.Mongo_connect}")
        db = client["tuyendung"]
        logger.info("✅ Kết nối MongoDB thành công")
        return db
    except Exception as e:
        logger.error(f"❌ Lỗi kết nối MongoDB: {str(e)}")
        raise

def job():
    logger.info("🕒 Bắt đầu quét email ứng tuyển")
    try:
        db = connect_to_mongodb()
        mongo_collection = db["ung_vien"]
        process_all_emails(mongo_collection)
        logger.info("✅ Hoàn thành quét email")
    except Exception as e:
        logger.error(f"❌ Lỗi khi quét email: {str(e)}")

def schedule_email_scan():
    schedule.every().day.at("08:00").do(job)
    # schedule.every().day.at("14:50").do(job)

    logger.info("📅 Scheduler đã được thiết lập để quét email lúc 8:00 sáng hàng ngày")
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except Exception as e:
            logger.error(f"❌ Lỗi trong vòng lặp scheduler: {str(e)}")
            time.sleep(60)