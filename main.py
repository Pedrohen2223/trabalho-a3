from fastapi import FastAPI, HTTPException, Path, Body, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    items = relationship("Item", back_populates="owner", cascade="all, delete")

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]

class ItemOut(ItemBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]

class UserOut(UserBase):
    id: int
    items: List[ItemOut] = []
    class Config:
        orm_mode = True

app = FastAPI(title="API RESTful Exemplo - Users & Items")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_cache_headers(response: Response, max_age: int = 60):
    response.headers["Cache-Control"] = f"public, max-age={max_age}"

@app.get("/users", response_model=List[UserOut])
def list_users(response: Response, db: Session = next(get_db())):
    users = db.query(User).all()
    add_cache_headers(response)
    return users

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int = Path(..., gt=0), response: Response = None, db: Session = next(get_db())):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    add_cache_headers(response)
    return user

@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserCreate, db: Session = next(get_db())):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserCreate, db: Session = next(get_db())):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

@app.patch("/users/{user_id}", response_model=UserOut)
def patch_user(user_id: int, user: UserUpdate, db: Session = next(get_db())):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.name is not None:
        db_user.name = user.name
    if user.email is not None:
        db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = next(get_db())):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return Response(status_code=204)

@app.get("/items", response_model=List[ItemOut])
def list_items(response: Response, db: Session = next(get_db())):
    items = db.query(Item).all()
    add_cache_headers(response)
    return items

@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int = Path(..., gt=0), response: Response = None, db: Session = next(get_db())):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    add_cache_headers(response)
    return item

@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(item: ItemCreate = Body(...), owner_id: int = Body(..., embed=True), db: Session = next(get_db())):
    user = db.query(User).filter(User.id == owner_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Owner user not found")
    db_item = Item(title=item.title, description=item.description, owner_id=owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.put("/items/{item_id}", response_model=ItemOut)
def update_item(item_id: int, item: ItemCreate, db: Session = next(get_db())):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.title = item.title
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

@app.patch("/items/{item_id}", response_model=ItemOut)
def patch_item(item_id: int, item: ItemUpdate, db: Session = next(get_db())):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.title is not None:
        db_item.title = item.title
    if item.description is not None:
        db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = next(get_db())):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return Response(status_code=204)
