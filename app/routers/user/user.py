from . import schemas
from ...utils import token_functions
from ...database import database, models
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(prefix='/user', tags=['Users'])

@router.get('/{userId}', response_model=schemas.UserProfileResponse)
def get_user_by_id(
    userId: int,
    db: Session = Depends(database.get_db),
    currentUser: models.User = Depends(token_functions.get_current_user)):
    user = db.query(models.User).filter(models.User.userId == userId).first()
    if user != None:
        questions: list[models.Question] = db.query(models.Question).filter(models.Question.userId == userId).all()
        answers: list[models.Answer] = db.query(models.Answer).filter(models.Answer.userId == userId).all()
        answers_dict = []
        for answer in answers:
            question = db.query(models.Question).filter(models.Question.questionId == answer.questionId).first()
            votes: list[models.Votes] = db.query(models.Votes).filter(models.Votes.answerId == answer.answerId).all()
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
            answers_dict.append({
                'question': question.question if question != None else 'Something went wrong',
                'answer': {
                    **answer.__dict__,
                    'upVotes': upVotes,
                    'downVotes': downVotes,
                    'currentUserUpVoted': currentUsersVote
                }
            })
        return {**user.__dict__, 'questions': questions, 'answers': answers_dict}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {userId} does not exist")

@router.post('/updateBio')
def update_bio(
    body: schemas.UpdateBio,
    db: Session = Depends(database.get_db),
    user: models.User = Depends(token_functions.get_current_user)):
    query = db.query(models.User).filter(models.User.userId == user.userId)
    query.update({
        "bio": body.newBio,
        "lastUpdated": datetime.now()
    })
    db.commit()
    return {'details': 'Bio updated'}
