from bson import ObjectId
from accounts.db.connection import get_db
from accounts.models.user_model import User
from bson import ObjectId

class UserRepository:
    def __init__(self):
        self.collection = get_db()["users"]
        self.collection.create_index("email", unique=True)

    def exists_by_email(self, email: str) -> bool:
        return self.collection.count_documents({"email": email}, limit=1) > 0

    def find_by_email(self, email: str) -> User | None:
        doc = self.collection.find_one({"email": email})
        return User.from_document(doc) if doc else None

    def find_by_id(self, user_id: str) -> User | None:
        try:
            doc = self.collection.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None
        return User.from_document(doc) if doc else None

    def create(self, name: str, email: str, hashed_password: str) -> User:
        user = User(name=name, email=email, password=hashed_password)
        result = self.collection.insert_one(user.to_document())
        user.id = str(result.inserted_id)
        return user

    def update_password(self, user_id: str, hashed_password: str):
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password": hashed_password}}
        )
        return result.modified_count