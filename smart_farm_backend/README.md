### Instructions

Install dependencies: `pip install -r requirements.txt`

### Database Initialization

CLI script to create database and create users:

Type `python` to enter the Python CLI:

```
# During database setup, all subclasses will automatically create their respective tables:
from app.database import Base, engine
from app.models import *  # Import all sensor/controller classes

Base.metadata.create_all(bind=engine)

# Create users
from app.database import SessionLocal
from app.models import User
from app.utils import hash_password
db = SessionLocal()
new_user = User(username="admin", password=hash_password("securepassword"))
db.add(new_user)
db.commit()

```

### Run

MQTT broker credentials can be edit from `app/config.py` and username and password can be specified from the command line:

Run the server: `python run.py --mqtt-username username --mqtt-password password`