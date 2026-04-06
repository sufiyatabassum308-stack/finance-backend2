from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import Base, engine
from app.deps import get_db
from app import schemas, crud, models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finance Data Processing and Access Control Backend",
    description="Backend assignment using FastAPI, SQLite, SQLAlchemy, and role-based access control.",
    version="1.0.0"
)


def role_checker(required_roles: list, x_role: str = Header(...)):
    if x_role not in required_roles:
        raise HTTPException(status_code=403, detail="Access denied")
    return x_role


@app.get("/")
def root():
    return {"message": "Finance Backend API is running"}


@app.post("/users", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    x_role: str = Depends(lambda: "admin")
):
    return crud.create_user(db, user)


@app.get("/users", response_model=list[schemas.UserResponse])
def list_users(
    db: Session = Depends(get_db),
    x_role: str = Header(...)
):
    if x_role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can view users")
    return crud.get_users(db)


@app.post("/records", response_model=schemas.RecordResponse)
def create_record(
    record: schemas.RecordCreate,
    db: Session = Depends(get_db),
    x_role: str = Header(...)
):
    if x_role not in ["admin", "analyst"]:
        raise HTTPException(status_code=403, detail="Only admin or analyst can create records")

    if record.type not in ["income", "expense"]:
        raise HTTPException(status_code=400, detail="Type must be either income or expense")

    user = crud.get_user(db, record.owner_id)
    if not user:
        raise HTTPException(status_code=404, detail="Owner user not found")

    return crud.create_record(db, record)


@app.get("/records", response_model=list[schemas.RecordResponse])
def list_records(
    category: str | None = None,
    type: str | None = None,
    db: Session = Depends(get_db),
    x_role: str = Header(...)
):
    if x_role not in ["admin", "analyst", "viewer"]:
        raise HTTPException(status_code=403, detail="Invalid role")
    return crud.get_records(db, category=category, type_=type)


@app.put("/records/{record_id}", response_model=schemas.RecordResponse)
def edit_record(
    record_id: int,
    record: schemas.RecordUpdate,
    db: Session = Depends(get_db),
    x_role: str = Header(...)
):
    if x_role not in ["admin", "analyst"]:
        raise HTTPException(status_code=403, detail="Only admin or analyst can update records")

    updated = crud.update_record(db, record_id, record)
    if not updated:
        raise HTTPException(status_code=404, detail="Record not found")
    return updated


@app.delete("/records/{record_id}")
def remove_record(
    record_id: int,
    db: Session = Depends(get_db),
    x_role: str = Header(...)
):
    if x_role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete records")

    deleted = crud.delete_record(db, record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted successfully"}


@app.get("/dashboard-summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    x_role: str = Header(...)
):
    if x_role not in ["admin", "analyst", "viewer"]:
        raise HTTPException(status_code=403, detail="Invalid role")

    return crud.get_summary(db)