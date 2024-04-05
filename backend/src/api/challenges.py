from datetime import datetime, timedelta
import os
from typing import List
from sqlalchemy import desc, or_
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Form
from src.db_models.likes import LikesTable
from src.db_models.challenges import ChallengeTable, ChallengeStatus, ChallengeStatus
from src.db_models.text_reaction import TextReactionTable
from src.db_models.users import UserTable
from src.api_models.challenge_accepted import *
from src.db.session import get_db
from src.chatgpt.api_call import check_user_challenge_for_legal
import uuid
from src.email.send_email import send_email_background
from src.api_models.email import ChallengeEmail

router = APIRouter(tags=["Challenges"])

ALLOWED_EXTENSIONS = ["mp4", "png", "jpeg", "jpg"]


@router.post("/challenges")
async def create_challenge(
    challenge: ChallengeForm,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> int:
    challenges_per_user = db.exec(
        select(ChallengeTable).where(
            ChallengeTable.receiver_user_id == challenge.friend_id
        )
    ).all()
    number_of_active_challenges = 0
    for challenge_per_user in challenges_per_user:
        if challenge_per_user.status in (
            ChallengeStatus.PENDING,
            ChallengeStatus.ACCEPTED,
        ):
            number_of_active_challenges += 1
    if number_of_active_challenges >= 5:
        raise HTTPException(
            status_code=406, detail="Freund hat bereits 5 Challenges bzw. Anfragen."
        )

    if challenge.chatgpt_check:
        answer = check_user_challenge_for_legal(challenge.description)
        if answer == "illegal":
            raise HTTPException(status_code=406, detail="Challenge ist illegal.")

    if challenge.email_check:
        sent_from_user = db.exec(
            select(UserTable).where(UserTable.id == challenge.user_id)
        ).first()
        sent_to_user = db.exec(
            select(UserTable).where(UserTable.id == challenge.friend_id)
        ).first()
        email_data = ChallengeEmail(
            sent_from_username=sent_from_user.username,
            send_to_email=sent_to_user.email,
            send_to_username=sent_to_user.username,
        )
        send_email_background(background_tasks=background_tasks, email_data=email_data)

    if challenge.friend_id == None:
        create_status = ChallengeStatus.ASLINK
    else:
        create_status = ChallengeStatus.PENDING

    list_hashtags = []
    if challenge.hashtags_list:
        hashtags = challenge.hashtags_list.split(",")

        for hashtag in hashtags:
            existing_hashtag_entry = db.exec(
                select(HashtagTable).where(HashtagTable.text == hashtag)
            ).first()
            if existing_hashtag_entry:
                list_hashtags.append(existing_hashtag_entry)
            else:
                hashtag_entry = HashtagTable()
                hashtag_entry.text = hashtag
                list_hashtags.append(hashtag_entry)

    challenge_entry = ChallengeTable(
        sender_user_id=challenge.user_id,
        receiver_user_id=challenge.friend_id,
        title=challenge.challenge_name,
        description=challenge.description,
        reward=challenge.reward,
        challenge_resources="/",
        prove_resource="",
        status=create_status,
        hashtags=list_hashtags,
    )
    db.add(challenge_entry)
    db.commit()
    db.refresh(challenge_entry)
    return challenge_entry.id


@router.get("/challenges")
async def get_challenges(
    user_id: int, db: Session = Depends(get_db)
) -> List[Challenge]:
    challenges_entries = db.exec(select(ChallengeTable)).all()
    challenges = map_challenge_list(user_id, challenges_entries, db)

    return challenges


def map_challenge_list(
    logged_in_user_id: int, challenges_entries: List[ChallengeTable], db: Session
) -> List[Challenge]:
    challenges = []

    for challenge in challenges_entries:
        user = db.exec(
            select(UserTable).where(UserTable.id == challenge.sender_user_id)
        ).first()
        comments = []
        for comment in db.exec(
            select(TextReactionTable).where(
                TextReactionTable.challenge_id == challenge.id
            )
        ).all():
            username = (
                db.exec(select(UserTable).where(UserTable.id == comment.user_id))
                .first()
                .username
            )
            comment_obj = Comment(
                id=comment.id,
                user_id=comment.user_id,
                challenge_id=comment.challenge_id,
                username=username,
                text=comment.text,
                image_path=comment.image_path,
            )
            comments.append(comment_obj)
        likes_count = len(
            db.exec(
                select(LikesTable).where(
                    LikesTable.challenge_id == challenge.id, LikesTable.state == True
                )
            ).all()
        )
        has_liked = db.exec(
            select(LikesTable.state).where(
                LikesTable.challenge_id == challenge.id,
                LikesTable.user_id == logged_in_user_id,
            )
        ).first()
        if has_liked == None:
            has_liked = False
        likes = LikeChallengeResponse(likes_count=likes_count, has_liked=has_liked)
        receiver_name = (
            db.exec(select(UserTable).where(UserTable.id == challenge.receiver_user_id))
            .first()
            .username
        )
        challenge_obj = Challenge(
            id=challenge.id,
            publisher_name=user.username,
            receiver_name=receiver_name,
            receiver_id=challenge.receiver_user_id,
            title=challenge.title,
            description=challenge.description,
            prove_resource_path=challenge.prove_resource,
            done_date=challenge.done_date,
            hashtags=challenge.hashtags,
            comments=comments,
            likes=likes,
            reward=challenge.reward,
        )

        challenges.append(challenge_obj)

    return challenges


@router.get("/challenges/{userId}/pending")
async def get_pending_challenges(
    userId: str, db: Session = Depends(get_db)
) -> List[Challenge]:
    challenges_entries = db.exec(
        select(ChallengeTable).where(
            ChallengeTable.status == ChallengeStatus.PENDING,
            ChallengeTable.receiver_user_id == userId,
        )
    ).all()
    challenges = map_challenge_list(userId, challenges_entries, db)

    return challenges


@router.get("/challenges/{userId}/done")
async def get_done_challenges(
    userId: str, logged_in_user_id: int, db: Session = Depends(get_db)
) -> List[Challenge]:
    challenges_entries = db.exec(
        select(ChallengeTable)
        .order_by(desc(ChallengeTable.done_date))
        .where(
            ChallengeTable.status == ChallengeStatus.DONE,
            ChallengeTable.receiver_user_id == userId,
        )
    ).all()
    challenges = map_challenge_list(logged_in_user_id, challenges_entries, db)
    return challenges


@router.get("/challenges/{userId}/accepted")
async def get_accepted_challenges(
    userId: str, db: Session = Depends(get_db)
) -> List[Challenge]:
    challenges_entries = db.exec(
        select(ChallengeTable).where(
            ChallengeTable.status == ChallengeStatus.ACCEPTED,
            ChallengeTable.receiver_user_id == userId,
        )
    ).all()
    challenges = map_challenge_list(userId, challenges_entries, db)
    return challenges


@router.get("/challenges/{userId}/created")
async def get_created_challenges(
    userId: int, db: Session = Depends(get_db)
) -> List[CreatedChallenges]:
    challenge_entries: List[ChallengeTable] = db.exec(
        select(ChallengeTable).where(
            or_(
                ChallengeTable.status == ChallengeStatus.ACCEPTED,
                ChallengeTable.status == ChallengeStatus.PENDING,
            ),
            ChallengeTable.sender_user_id == userId,
        )
    ).all()
    created_challenges = []
    for challenge_entry in challenge_entries:
        receiver_user = db.exec(
            select(UserTable).where(UserTable.id == challenge_entry.receiver_user_id)
        ).first()
        created_challenges.append(
            CreatedChallenges(
                receiver_user_name=receiver_user.username,
                receiver_user_id=receiver_user.id,
                reward=challenge_entry.reward,
                hashtags=challenge_entry.hashtags,
                title=challenge_entry.title,
                description=challenge_entry.description,
                status=challenge_entry.status,
            )
        )
    return created_challenges


@router.put("/challenges/{challenge_id}/comment")
async def accept_challenge(
    challenge_id: int,
    image: UploadFile = File(None),
    user_id: int = Form(...),
    comment_text: str = Form(None),
    db: Session = Depends(get_db),
):
    comment_entry = TextReactionTable()
    comment_entry.user_id = user_id
    comment_entry.challenge_id = challenge_id
    if comment_text:
        comment_entry.text = comment_text

    if image:
        file_extension = image.filename.split(".")[-1].lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file format. Allowed formats: mp4, png, jpeg, jpg",
            )

        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        file_path = os.path.join("/backend/resources", unique_filename)

        with open(file_path, "wb") as f:
            f.write(image.file.read())
        comment_entry.image_path = unique_filename

    db.add(comment_entry)
    db.commit()


@router.put("/challenges/{challenge_id}/accept")
async def accept_challenge(challenge_id: int, db: Session = Depends(get_db)):
    challenge = db.exec(
        select(ChallengeTable).where(ChallengeTable.id == challenge_id)
    ).first()
    challenge.status = ChallengeStatus.ACCEPTED

    db.add(challenge)
    db.commit()


@router.get("/challenges/ListDir")
async def complete_challenge_image():
    return os.listdir("resources")


@router.put("/challenges/{challenge_id}/done")
async def complete_challenge(
    challenge_id: int, image: UploadFile, db: Session = Depends(get_db)
):
    challenge = db.exec(
        select(ChallengeTable).where(ChallengeTable.id == challenge_id)
    ).first()
    challenge.status = ChallengeStatus.DONE
    time_offset = timedelta(hours=1)
    challenge.done_date = datetime.utcnow() + time_offset

    if image:
        file_extension = image.filename.split(".")[-1].lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file format. Allowed formats: mp4, png, jpeg, jpg",
            )

        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        file_path = os.path.join("/backend/resources", unique_filename)

        with open(file_path, "wb") as f:
            f.write(image.file.read())
        challenge.prove_resource = unique_filename

    db.add(challenge)
    db.commit()


@router.put("/challenges/{challenge_id}/decline")
async def decline_challenge(challenge_id: int, db: Session = Depends(get_db)):
    challenge = db.exec(
        select(ChallengeTable).where(ChallengeTable.id == challenge_id)
    ).first()
    challenge.status = ChallengeStatus.DECLINED

    db.add(challenge)
    db.commit()


@router.get("/challenges/{hashtag}")
async def get_challenges_by_hashtag(
    userId: int, hashtag: str, db: Session = Depends(get_db)
) -> List[Challenge]:
    hashtag_entry = db.exec(
        select(HashtagTable).where(HashtagTable.text == hashtag)
    ).first()
    done_challenges = [
        challenge
        for challenge in hashtag_entry.challenges
        if challenge.status == ChallengeStatus.DONE
    ]
    sorted_entries = sorted(done_challenges, key=lambda x: x.done_date, reverse=True)
    challenges = map_challenge_list(userId, sorted_entries, db)
    return challenges


@router.get("/challenges/latest/{limit}")
async def get_latest_challenges(
    limit: int, userId: int, db: Session = Depends(get_db)
) -> List[Challenge]:
    latest_entires = db.exec(
        select(ChallengeTable)
        .order_by(desc(ChallengeTable.done_date))
        .where(ChallengeTable.status == ChallengeStatus.DONE)
        .limit(limit)
    ).all()
    challenges = map_challenge_list(userId, latest_entires, db)
    return challenges


@router.put("/challenges/{challenge_id}/like")
async def toggle_challenge_like(
    request: LikeChallengeRequest, db: Session = Depends(get_db)
):
    like_entry = db.exec(
        select(LikesTable).where(
            LikesTable.user_id == request.user_id,
            LikesTable.challenge_id == request.challenge_id,
        )
    ).first()
    if like_entry:
        like_entry.state = not like_entry.state
        db.add(like_entry)
        db.commit()
    else:
        like_entry = LikesTable(
            user_id=request.user_id, challenge_id=request.challenge_id, state=True
        )
        db.add(like_entry)
        db.commit()


@router.get("/challenges/{challenge_id}/like")
async def get_likes(challenge_id: int, db: Session = Depends(get_db)) -> int:
    liked_entries = db.exec(
        select(LikesTable).where(
            LikesTable.challenge_id == challenge_id, LikesTable.state == True
        )
    ).all()
    if liked_entries:
        return len(liked_entries)
    else:
        return 0
