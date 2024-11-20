### Instructions

Install dependencies: `pip install -r requirements.txt`

### Database Initialization
During database setup, all subclasses will automatically create their respective tables:

```python
from app.database import Base, engine
from app.models import *  # Import all sensor/controller classes

Base.metadata.create_all(bind=engine)
```

CLI script to create users:
```
python
>>> from app.database import SessionLocal
>>> from app.models import User
>>> from app.utils import hash_password
>>> db = SessionLocal()
>>> new_user = User(username="admin", password=hash_password("securepassword"))
>>> db.add(new_user)
>>> db.commit()

```
### Run

Run the server: `python run.py`