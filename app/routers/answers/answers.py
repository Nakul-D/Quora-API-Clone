from . import schemas
from ...utils import token_functions
from ...database import database, models
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response


router = APIRouter(prefix='/answer', tags=['Answers'])

@router.get(
    '/id/{answerId}',
    response_model=schemas.AnswerResponseWithVotes)
def get_answer_by_id(
    answerId: int,
    db: Session = Depends(database.get_db),
    user: models.User = Depends(token_functions.get_current_user)):
    answer = db.query(models.Answer).filter(models.Answer.answerId == answerId).first()
    if answer != None:
        votes: list[models.Votes] = db.query(models.Votes).filter(models.Votes.answerId == answerId).all()
        upVotes: int = 0
        downVotes: int = 0
        currentUsersVote = None
        for vote in votes:
            if vote.userId == user.userId:
                currentUsersVote = vote.vote
            if vote.vote == True:
                upVotes += 1
            else:
                downVotes += 1
        data: dict = answer.__dict__
        data['upVotes'] = upVotes
        data['downVotes'] = downVotes
        data['currentUserUpVoted'] = currentUsersVote
        return data
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Answer with id {answerId} does not exist")

@router.post(
    '/post/{questionId}',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.AnswerResponse)
def post_answer(
    questionId: int,
    body: schemas.PostAnswer,
    db: Session = Depends(database.get_db),
    user: models.User = Depends(token_functions.get_current_user)):
    question = db.query(models.Question).filter(models.Question.questionId == questionId).first()
    if question != None:
        answer_exists = db.query(models.Answer).filter(
            models.Answer.questionId == questionId, models.Answer.userId == user.userId).first()
        if answer_exists == None:
            data: dict = body.dict()
            data['userId'] = user.userId
            data['questionId'] = questionId
            new_answer = models.Answer(**data)
            db.add(new_answer)
            db.commit()
            db.refresh(new_answer)
            return new_answer
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Already answered, id: {answer_exists.answerId}, try updating")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Question with id {questionId} does not exist")

@router.put(
    '/update/{answerId}',
    response_model=schemas.AnswerResponse)
def update_answer(
    answerId: int,
    body: schemas.PostAnswer,
    db: Session = Depends(database.get_db),
    user: models.User = Depends(token_functions.get_current_user)):
    query = db.query(models.Answer).filter(models.Answer.answerId == answerId)
    answer = query.first()
    if answer != None:
        if answer.userId == user.userId:
            answer_dict: dict = body.dict()
            answer_dict.update({
                'lastUpdated': datetime.now(),
                'edited': True
            })
            query.update(answer_dict)
            db.commit()
            db.refresh(answer)
            return answer
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Answer with id {answerId} does not exist")

@router.delete('/delete/{answerId}')
def delete_answer(
    answerId: int,
    db: Session = Depends(database.get_db),
    user: models.User = Depends(token_functions.get_current_user)):
    query = db.query(models.Answer).filter(models.Answer.answerId == answerId)
    answer = query.first()
    if answer != None:
        if answer.userId == user.userId:
            query.delete()
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Answer with id {answerId} does not exist")
