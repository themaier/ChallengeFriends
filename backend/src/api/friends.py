from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException, Response, status
from src.api_models.challenge_accepted import Friend
from src.db_models.users import UserTable
from src.utils.error import raise_404
from src.db_models.friends import FriendsTable
from src.db.session import get_db
from sqlmodel import Session, select, delete

router = APIRouter(tags=["Friends"])

@router.get("/friendship")
async def get_all_friends(
    db: Session = Depends(get_db)
) -> List[FriendsTable]:
    db_friends = db.exec(select(FriendsTable)).all()
    return db_friends


@router.get("/friendship/{user_id}")
async def get_friends_for(
        user_id: str,  
        db: Session = Depends(get_db)
) -> List[Friend]:

    friends = db.exec(select(FriendsTable).where(FriendsTable.user_id == user_id))

    friendsList = []
    for friend in friends:
         friend_username = db.exec(select(UserTable.username).where(UserTable.id == friend.friend_user_id)).first()
         friend_entity = Friend(
              user_id=friend.friend_user_id,
              username=friend_username
         )
         friendsList.append(friend_entity)

    return friendsList

@router.delete("/friendship")
async def delete_friendship(
    user_id: str,
    friend_user_id: str,
    db: Session = Depends(get_db)
) -> Response:
    db.exec(delete(FriendsTable).where(FriendsTable.user_id == user_id, FriendsTable.friend_user_id == friend_user_id))
    db.exec(delete(FriendsTable).where(FriendsTable.user_id == friend_user_id, FriendsTable.friend_user_id == user_id))
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/friendship")
async def post_new_friendship(
    friendship_request: FriendsTable,
    db: Session = Depends(get_db)
) -> Friend:

    if(friendship_request.user_id == friendship_request.friend_user_id):
         return

    exisiting_friend = db.exec(select(FriendsTable)
            .where(FriendsTable.user_id == friendship_request.user_id, FriendsTable.friend_user_id == friendship_request.friend_user_id )).first()
    
    if(exisiting_friend != None):
            return
        

    friend_request_counterpart = FriendsTable(
        user_id=friendship_request.friend_user_id,
        friend_user_id=friendship_request.user_id,
        status=True
    )
    
    friend_request_counterpart.user_id, friend_request_counterpart.friend_user_id = friendship_request.friend_user_id, friendship_request.user_id

    db.add(friendship_request)
    db.add(friend_request_counterpart)
    db.commit()
    # db.refresh(friendship_request)
    
    friend_username = db.exec(select(UserTable.username).where(UserTable.id == friendship_request.friend_user_id)).first()

    response = Friend(
         user_id= friendship_request.friend_user_id,
         username= friend_username
    )

    return response
