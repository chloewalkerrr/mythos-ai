from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import get_db
from models.all_models import Book
from schemas.book import BookCreate, BookResponse, BookUpdate

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.get("", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@router.get("/{id}", response_model=BookResponse)
def get_book(id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Not found")

    return book


@router.post("", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(**book.model_dump())

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


@router.put("/{id}", response_model=BookResponse)
def update_book(id: int, book: BookUpdate, db: Session = Depends(get_db)):
    existing = db.query(Book).filter(Book.id == id).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Not found")

    for field, value in book.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)

    db.commit()
    db.refresh(existing)

    return existing


@router.delete("/{id}")
def delete_book(id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(book)
    db.commit()

    return {"message": "Deleted"}
