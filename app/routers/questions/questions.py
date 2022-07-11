from . import schemas
from ...utils import token_functions
from ...database import database, models
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response


router = APIRouter(prefix='/question', tags=['Questions'])

@router.get(
    '/id/{questionId}',
    response_model=schemas.QuestionWithAnswersResponse)
def get_question_by_id(
    questionId: int,
    db: Session = Depends(database.get_db),
    user: models.User = Depends(token_functions.get_current_user)):
    query = db.query(models.Question).filter(models.Question.questionId == questionId)
    question = query.first()
    if question != None:
        answers: list[models.Answer] = db.query(models.Answer).filter(models.Answer.questionId == questionId).all()
        data: dict = question.__dict__
        answers_dict: list[dict] = []
        for answer in answers:
            answers_dict.append(answer.__dict__)
        data['answers'] = answers_dict
        return data
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Question with id {questionId} not found")

@router.get(
    '/search',
    response_model=List[schemas.QuestionResponse])
def search_question(
    keyword: str,
    limit: int,
    db: Session = Depends(database.get_db),
    user: models.User = Depends(token_functions.get_current_user)):
    if limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't fetch more than 100 questions")
    query = db.query(models.Question).filter(models.Question.question.contains(keyword)).limit(limit=limit)
    search_result: list[models.Question] = query.all()
    return search_result

@router.post(
    '/post',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.QuestionResponse)
def post_question(
    body: schemas.PostQuestion,
    db: Session = Depends(database.get_db),
    user: models.User = Depends(token_functions.get_current_user)):
    new_question = models.Question(question=body.question, userId=user.userId)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

@router.put('/update/{questionId}', response_model=schemas.QuestionResponse)
def update_question(
    questionId: int,
    body: schemas.PostQuestion,
    db: Session = Depends(database.get_db),
    user: models.User = Depends(token_functions.get_current_user)):
    query = db.query(models.Question).filter(models.Question.questionId == questionId)
    question: models.Question | None = query.first()
    if question != None:
        if question.userId == user.userId:
            question_dict: dict = body.dict()
            question_dict.update({
                'lastUpdated': datetime.now(),
                'edited': True
            })
            query.update(question_dict)
            db.commit()
            db.refresh(question)
            return question
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Question with id {questionId} not found")

@router.delete('/delete/{questionId}')
def delete_question(
    questionId: int,
    db: Session = Depends(database.get_db),
    user: models.User = Depends(token_functions.get_current_user)):
    query = db.query(models.Question).filter(models.Question.questionId == questionId)
    question: models.Question | None = query.first()
    if question != None:
        if question.userId == user.userId:
            query.delete()
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Question with id {questionId} not found")
