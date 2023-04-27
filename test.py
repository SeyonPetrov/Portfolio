from data import db_session
from data.users import User

db_session.global_init('db/owners12.db')
sess = db_session.create_session()

user = sess.query(User).all()
for x in user:
    print(x.name)