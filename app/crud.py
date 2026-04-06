from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(models.User).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_record(db: Session, record: schemas.RecordCreate):
    db_record = models.FinancialRecord(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_records(db: Session, category=None, type_=None):
    query = db.query(models.FinancialRecord)
    if category:
        query = query.filter(models.FinancialRecord.category == category)
    if type_:
        query = query.filter(models.FinancialRecord.type == type_)
    return query.all()


def get_record(db: Session, record_id: int):
    return db.query(models.FinancialRecord).filter(models.FinancialRecord.id == record_id).first()


def update_record(db: Session, record_id: int, record_data: schemas.RecordUpdate):
    record = get_record(db, record_id)
    if not record:
        return None

    for key, value in record_data.model_dump(exclude_unset=True).items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record


def delete_record(db: Session, record_id: int):
    record = get_record(db, record_id)
    if not record:
        return None
    db.delete(record)
    db.commit()
    return record


def get_summary(db: Session):
    total_income = db.query(func.sum(models.FinancialRecord.amount)).filter(
        models.FinancialRecord.type == "income"
    ).scalar() or 0

    total_expenses = db.query(func.sum(models.FinancialRecord.amount)).filter(
        models.FinancialRecord.type == "expense"
    ).scalar() or 0

    net_balance = total_income - total_expenses

    category_totals = (
        db.query(
            models.FinancialRecord.category,
            func.sum(models.FinancialRecord.amount).label("total")
        )
        .group_by(models.FinancialRecord.category)
        .all()
    )

    recent_activity = (
        db.query(models.FinancialRecord)
        .order_by(models.FinancialRecord.date.desc())
        .limit(5)
        .all()
    )

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": net_balance,
        "category_totals": [
            {"category": item.category, "total": item.total} for item in category_totals
        ],
        "recent_activity": recent_activity
    }