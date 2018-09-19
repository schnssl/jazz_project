from .app import app
from .db_setup import init_db

init_db()

if __name__ == '__main__':
    app.run()
