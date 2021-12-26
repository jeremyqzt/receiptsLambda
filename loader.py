import datetime
import uuid

class Loader:
    def __init__(self):
        ...

    @staticmethod
    def parse_data(json_dict):
        user_id = json_dict.get("user_id", None)
        business_id = json_dict.get("business_id", None)

        if not user_id or not business_id: raise

        return {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "business_id": business_id,
            "created_at": datetime.datetime.now().isoformat()
        }

