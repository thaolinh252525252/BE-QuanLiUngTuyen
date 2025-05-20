from datetime import datetime

def init_tracking_collection(db):
    return db["email_tracking"]

def has_processed_email(tracking_collection, uid: str) -> bool:
    return tracking_collection.find_one({"uid": uid}) is not None

def mark_email_as_processed(tracking_collection, uid: str, from_email: str, subject: str):
    tracking_collection.insert_one({
        "uid": uid,
        "from": from_email,
        "subject": subject,
        "processed_at": datetime.now()
    })
