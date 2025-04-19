
from database import Database

db = Database()

print(db.get_columns('user_query'))

print(db.fetch_all('user_query'))

print(db.validate_query('SELECT * FROM initiative'))

print(db.validate_query('DELETE FROM initiative'))

