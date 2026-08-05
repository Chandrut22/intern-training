import sqlalchemy as db
from sqlalchemy.sql import func
from dotenv import load_dotenv
import os

load_dotenv()

engine = db.create_engine(os.getenv("DB_URL"),echo=True)
# print("Connection created successfully")

meta_data = db.MetaData()
meta_data.reflect(bind=engine)

users = db.Table(
    'users', meta_data,
    db.Column('id',db.Integer,primary_key=True),
    db.Column('name',db.String(25),nullable=False),
    db.Column('email',db.String(50),unique=True,nullable=False),
    db.Column("created_at", db.DateTime, server_default=func.now()),
)

meta_data.create_all(engine)

s1 = users.insert().values(name='chandru',email='chandru@gamil.com')
s2 = users.insert().values(name='Hari',email='hari@gamil.com')
s3 = users.insert().values(name='Balaji',email='Balaji@gamil.com')
s4 = users.insert().values(name='Sai',email='sai@gamil.com')
s5 = users.insert().values(name='snegan',email='snegan@gamil.com')


with engine.connect() as conn:
    conn.execute(s1)
    conn.execute(s2)
    conn.execute(s3)
    conn.execute(s4)
    conn.execute(s5)

    conn.commit()

# -----------------------------------------------------------------------------------------------------------------------
# Select Query

search_term = "s" 
with engine.connect() as conn:
    res = conn.execute(
        db.text("SELECT * FROM users WHERE name ILIKE :search_name"),
        {"search_name": f"%{search_term}%"}
    ).fetchall()
    
    for r in res:
        print("\n", r)

# -----------------------------------------------------------------------------------------------------------------------
# Insert 

data = ({"name":"Monish","email":"monish@gmail.com"},
        {"name":"Dhanush","email":"dhanush@gmail.com"})

st = db.text("""
                insert into users (name,email)
                values (:name,:email)
             """)

with engine.connect() as conn:
    # for line in data:
    #     conn.execute(st,line)
    conn.execute(st,data)
    conn.commit()


sql = db.text("select * from users")
with engine.connect() as conn:
    res = conn.execute(sql)
    # print(res)
    for r in res:
        print("\n",r)

# -----------------------------------------------------------------------------------------------------------------------
# Update Query

users = meta_data.tables['users']

stmt = users.update().where(users.c.email == 'dhanush@gmail.com').values(name='Dhanush Raj')
with engine.connect() as conn:
    conn.execute(stmt)
    conn.commit()

sql = db.text("select * from users")
with engine.connect() as conn:
    res = conn.execute(sql)
    for r in res:
        print("\n",r)

# -----------------------------------------------------------------------------------------------------------------------
# Delete Query

stmt = users.delete().where(users.c.email == 'sai@gmail.com')
with engine.begin() as conn:
    conn.execute(stmt)

sql = db.text("select * from users")
with engine.connect() as conn:
    res = conn.execute(sql)
    for r in res:
        print("\n",r)

# -----------------------------------------------------------------------------------------------------------------------
meta_data.drop_all(engine,checkfirst=True)