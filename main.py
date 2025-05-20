from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import candidates, email, job_descriptions
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from routers import users
from routers import client
from utils import scheduler  # Import scheduler from utils
from threading import Thread
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(email.router)
app.include_router(candidates.router, prefix="/candidates")
app.include_router(job_descriptions.router)
app.include_router(users.router)
app.include_router(client.router)

app.mount(
    "/cv_files",
    StaticFiles(directory="/root/FE/recruitment-api/cv_files"),
    name="cv_files"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def show_routes():
    logger.info("\n📌 ROUTES ĐANG ĐĂNG KÝ:")
    for route in app.routes:
        if isinstance(route, APIRoute):
            logger.info(f"→ {route.path} [{','.join(route.methods)}]")

@app.on_event("startup")
def start_scheduler():
    logger.info("🚀 Khởi động scheduler để quét email")
    try:
        scheduler_thread = Thread(target=scheduler.schedule_email_scan, daemon=True)
        scheduler_thread.start()
        logger.info("✅ Scheduler thread đã khởi động thành công")
    except Exception as e:
        logger.error(f"❌ Lỗi khi khởi động scheduler: {str(e)}")
        raise