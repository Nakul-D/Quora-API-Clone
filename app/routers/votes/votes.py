from . import schemas
from ...utils import token_functions
from ...database import database, models
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Response


router = APIRouter(prefix='/vote', tags=['Vote'])

@router.post('/{answerId}')
def post_vote(
    answerId: int,
    body: schemas.PostVote,
    db: Session = Depends(database.get_db),
    user: models.User = Depends(token_functions.get_current_user)):
    answer = db.query(models.Answer).filter(models.Answer.answerId == answerId).first()
    if answer != None:
        query = db.query(models.Votes).filter(models.Votes.answerId == answerId, models.Votes.userId == user.userId)
        vote = query.first()
        if vote == None:
            new_vote = models.Votes(**{
                'answerId': answerId,
                'userId': user.userId,
                'vote': body.upvoted
            })
            db.add(new_vote)
            db.commit()
            return Response(status_code=status.HTTP_201_CREATED, content="vote added")
        else:
            if vote.vote == body.upvoted:
                query.delete()
                db.commit()
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            else:
                query.update({
                    'vote': body.upvoted,
                    'lastUpdated': datetime.now(),
                    'edited': True
                })
                db.commit()
                return Response(status_code=status.HTTP_200_OK, content="vote updated")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Answer with id {answerId} does not exist")
