import models

from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI()

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

# Pydantic models for request validation
class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# POST endpoint to create a question with choices
@app.post("/questions/")
def create_question(question: QuestionBase, db: db_dependency):
    try:
        # Create question
        db_question = models.Questions(question_text=question.question_text)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        # Add choices
        for choice in question.choices:
            db_choice = models.Choices(
                choice_text=choice.choice_text,
                is_correct=choice.is_correct,
                question_id=db_question.id
            )
            db.add(db_choice)

        db.commit()
        db.refresh(db_question)  # Refresh to include choices

        # Return full question with choices
        return {
            "message": "Question created successfully",
            "question": {
                "id": db_question.id,
                "question_text": db_question.question_text,
                "choices": [
                    {"choice_text": c.choice_text, "is_correct": c.is_correct}
                    for c in db_question.choices
                ]
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# GET endpoint to read a question by ID
@app.get("/questions/{question_id}")
def read_question(question_id: int, db: db_dependency):
    question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found!")
    
    return {
        "id": question.id,
        "question_text": question.question_text,
        "choices": [
            {"choice_text": c.choice_text, "is_correct": c.is_correct} for c in question.choices
        ]
    }

# GET endpoint to read all choices for a question
@app.get("/choices/{question_id}")
def read_choices(question_id: int, db: db_dependency):
    choices = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    if not choices:
        raise HTTPException(status_code=404, detail="Choices not found!")
    
    return [
        {"choice_text": c.choice_text, "is_correct": c.is_correct} for c in choices
    ]

# Optional: GET endpoint to list all questions
@app.get("/questions/")
def get_all_questions(db: db_dependency):
    questions = db.query(models.Questions).all()
    result = []
    for q in questions:
        result.append({
            "id": q.id,
            "question_text": q.question_text,
            "choices": [
                {"choice_text": c.choice_text, "is_correct": c.is_correct} for c in q.choices
            ]
        })
    return result