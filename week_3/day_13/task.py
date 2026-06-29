from sqlalchemy import String, func, ForeignKey
from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship, sessionmaker
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import select
from dotenv import load_dotenv
import os

load_dotenv()

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"


class Post(Base):  
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(String(500), nullable=False)

    author: Mapped["User"] = relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, user_id={self.user_id!r}, content={self.content[:20]!r})"



# engine = create_engine(os.getenv("DB_URL"),echo=True)
engine = create_engine(os.getenv("DB_URL"))

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


SessionLocal = sessionmaker(bind=engine)

# CREATE 
db = SessionLocal()

user1 = User(name="Chandru", email="chandru@gmail.com")
user2 = User(name="Hari", email="hari@gmail.com")
db.add_all([user1, user2])
db.flush()  

post1 = Post(content="SQLAlchemy Basics Fundamentals", user_id=user1.id)
post2 = Post(content="Mastering ORM Relationships Details")
user1.posts.append(post2)  
post3 = Post(content="Postgres Performance Tips Indexing", user_id=user2.id)

db.add_all([post1, post3])
db.commit()
db.close()  


# READ 
db = SessionLocal()

user = db.query(User).filter(User.email == "chandru@gmail.com").first()
print("Found User:", user)

# 2. Like/ILike Filter
matching_users = db.query(User).filter(User.name.ilike("c%")).all()
print("Matches starting with C:", matching_users)

# 3. JOIN Query
results = db.query(Post.content, User.name).join(User).all()
for content, author_name in results:
    print(f"Post Content: '{content}' written by {author_name}")

user_with_posts = db.query(User).filter(User.id == 1).first()
print(f"{user_with_posts.name}'s Posts:")
for post in user_with_posts.posts:
    print(f"{post.content}")

db.close()

# UPDATE 
db = SessionLocal()

target_post = db.query(Post).filter(Post.content == "SQLAlchemy Basics Fundamentals").first()

if target_post:
    target_post.content = "SQLAlchemy 2.0 Core & ORM Basics"  
    db.commit()

db.close()

# DELETE
db = SessionLocal()

post_to_delete = db.query(Post).filter(Post.content == "Postgres Performance Tips Indexing").first()

if post_to_delete:
    db.delete(post_to_delete)  
    db.commit()

all_posts = db.query(Post).all()
print("Remaining Posts:", all_posts)

db.close()