#! python shell
#! >>> from models.user_models_db import UserDB
#! >>> UserDB.__table__
from DB import Base, engine

from models.hdv_db_models import *
from models.user_models_db import *

print("Creating database ....")

Base.metadata.create_all(engine)
