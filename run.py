import os

from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_migrate import upgrade as db_upgrade

from app import create_app, db
from config import BASE_DIR

# Load env
dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.getenv('FLASK_ENV') or 'default')
migrate = Migrate(app, db)
