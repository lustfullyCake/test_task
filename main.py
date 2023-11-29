from fastapi import FastAPI, status, Depends, Response
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import UUID

from crud import add_secret, find_secret, delete_secret
from database import engine, get_session
from encrypt import compare_phrase, decrypt
from schemas import SecretRecord
from responses import GenerateSecretResponse, GetSecretResponse, MessageResponse
from requests import GenerateSecretRequest, GetSecretRequest
from models import Base
from settings import get_settings


app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/", response_model=MessageResponse)
def homepage() -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "ok",
        },
    )


@app.post(
    "/secret/",
    response_model=GenerateSecretResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Secret with provided secret and phrase for control out security and returns key.",
    description="Create secret record.",
    response_description="'Key' is unique value storages your secret."
)
async def generate_secret(
    request: GenerateSecretRequest,
    database: Session = Depends(get_session),
) -> Response:
    record = SecretRecord(
        secret=request.secret,
        phrase=request.phrase,
    )
    record.process_request()
    add_secret(database, record)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"key": record.key_to_str}
    )


@app.post(
    "/secret/{secret_key}/",
    response_model=GetSecretResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": MessageResponse},
        404: {"model": MessageResponse},
    },
    summary="Get secret key and find related secret. Then compare provided phrase with storaged one and if they equal,"
            "returns your secret and delete the record from database.",
    description="Get secret by secret key and phrase.",
    response_description="'secret' is your saved decrypted message."
)
async def get_secret(
    secret_key: UUID,
    request: GetSecretRequest,
    database: Session = Depends(get_session),
) -> Response:
    record = find_secret(database, secret_key)

    if record is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": "Secret with such secret_key not found.",
            },
        )

    if not compare_phrase(record.phrase, request.phrase):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "Phases are mismatch.",
            }
        )

    settings = get_settings()
    secret = decrypt(record.secret, settings.secret_key)
    delete_secret(database, record)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"secret": secret},
    )
