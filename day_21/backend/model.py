import sqlalchemy as sa
from database import Base
from sqlalchemy.orm import Mapped, mapped_column

class ToDoList(Base):
    __tablename__ = "to_do_list"

    id:Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    task_title:Mapped[str] = mapped_column(sa.String, nullable=False)
    description:Mapped[str] = mapped_column(sa.String(200),nullable=False)
    iscompleted:Mapped[bool] = mapped_column(sa.Boolean,default=False)

    def __repr__(self):
        return f"Task(id: {self.id}, title: {self.task_title}, description: {self.description}, iscompleted: {self.iscompleted})"