from fastapi import APIRouter, HTTPException, Body, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
from typing import Optional

# Đảm bảo import jose đúng cách
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
# Sử dụng bcrypt trực tiếp thay vì passlib
import bcrypt

# Cấu hình JWT
SECRET_KEY = os.getenv("JWT_SECRET", "your_super_secret_key_change_this_in_production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 giờ

router = APIRouter()
load_dotenv()

# Lấy chuỗi kết nối từ biến môi trường
mongo_uri = os.environ.get("Mongo_connect")
if not mongo_uri:
    raise ValueError("Biến 'Mongo_connect' không được thiết lập trong file .env")

# Kết nối tới MongoDB
client = MongoClient(mongo_uri)
db = client["tuyendung"]
collection = db["users"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Hàm tạo token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Hàm băm mật khẩu
def hash_password(password: str) -> str:
    # Băm mật khẩu sử dụng bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  # Chuyển bytes thành string để lưu vào MongoDB

# Hàm xác minh mật khẩu
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # Xác minh mật khẩu
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        print(f"Lỗi xác minh mật khẩu: {e}")
        return False

# Hàm xác thực token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Không thể xác thực thông tin đăng nhập",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = collection.find_one({"username": username})
    if user is None:
        raise credentials_exception
    return user

# GET all users
@router.get("/users/")
def get_users():
    try:
        users = []
        for doc in collection.find():
            users.append({
                "id": str(doc["_id"]),
                "username": doc["username"],
                "name": doc.get("name", ""),
                "role": doc.get("role", "")
            })
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POST create new user
@router.post("/register")
def create_user(data: dict = Body(...)):
    username = data.get("username")
    role = data.get("role", "candidate")  # Mặc định là candidate
    raw_password = data.get("password")
    fullName = data.get("fullName", "")
    email = data.get("email", "")

    if not username or not raw_password:
        raise HTTPException(status_code=400, detail="Thiếu thông tin người dùng")

    if collection.find_one({"username": username}):
        raise HTTPException(status_code=409, detail="Người dùng đã tồn tại")

    if collection.find_one({"email": email}) and email:
        raise HTTPException(status_code=409, detail="Email đã được sử dụng")

    # Băm mật khẩu sử dụng hàm mới
    hashed_password = hash_password(raw_password)

    result = collection.insert_one({
        "username": username,
        "password": hashed_password,
        "role": role,
        "fullName": fullName,
        "email": email,
        "created_at": datetime.now()
    })
    return {"message": "Đã tạo người dùng thành công", "id": str(result.inserted_id)}

@router.put("/users/{username}")
def update_user_role(username: str, data: dict = Body(...)):
    update_fields = {}
    if "role" in data:
        update_fields["role"] = data["role"]
    if "fullName" in data:
        update_fields["fullName"] = data["fullName"]
    if "email" in data:
        update_fields["email"] = data["email"]

    if not update_fields:
        raise HTTPException(status_code=400, detail="Không có thông tin để cập nhật")

    result = collection.update_one(
        {"username": username},
        {"$set": update_fields}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")

    return {"message": "Đã cập nhật người dùng", "updated": update_fields}

# DELETE user
@router.delete("/users/{username}")
def delete_user(username: str):
    result = collection.delete_one({"username": username})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    return {"message": f"Đã xoá người dùng '{username}'"}

# Login API phù hợp với LoginPage React
@router.post("/login")
def login(data: dict = Body(...)):
    username = data.get("username")
    password = data.get("password")
    
    user = collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=401, detail="Tên đăng nhập hoặc mật khẩu không đúng")
    
    # Sử dụng hàm verify_password mới
    if not verify_password(password, user.get("password", "")):
        raise HTTPException(status_code=401, detail="Tên đăng nhập hoặc mật khẩu không đúng")
        
    # Tạo token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}, 
        expires_delta=access_token_expires
    )
    
    # Trả về đúng định dạng mà LoginPage đang mong đợi
    return {
        "username": user["username"],
        "role": user["role"],
        "token": access_token
    }

# API để lấy thông tin người dùng hiện tại
@router.get("/me")
def get_current_user_info(current_user: dict = Depends(get_current_user)):
    user_info = {
        "id": str(current_user["_id"]),
        "username": current_user["username"],
        "fullName": current_user.get("fullName", ""),
        "email": current_user.get("email", ""),
        "role": current_user.get("role", "")
    }
    return user_info