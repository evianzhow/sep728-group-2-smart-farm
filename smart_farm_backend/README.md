## Docker deployment

```
docker-compose up --build
```

## Python development & deployment

### Instructions

Install dependencies: `pip install -r requirements.txt`

### Database Initialization

Use `init_db.py` to create database and create users

**OR**

Manually create database and create users through the Python CLI:

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

### Todos

- [x] Fix MQTT on_message callback, should be able to store different types of sensors and controllers states to the database (SQLite), had issues right now.
- [x] Implement login and authentication features, validate user token from headers with all endpoints except for the login endpoint
- [x] Added sensors and controllers `GET /sensors/*/preview` and `GET /controllers/*/preview` endpoints, should be able to get the latest state of a sensor or controller
- [x] Added controllers `POST /controllers/*` endpoints for controlling controllers
- [x] Added sensors and controllers `GET /sensors/*/history` and `GET /controllers/*/history` endpoints with pagination features
- [x] Added sensors and controllers `GET /sensors/*/chart` endpoints, should be able to convert history data to chart-compatible data for better frontend processing
- [x] Added rules CRUD endpoints
- [x] Added rules engine to trigger controllers based on rules
- [x] Better error handling for HTTP exceptions

