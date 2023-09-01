from fastapi import HTTPException, Header
from os import environ as env
import requests

from typing import Annotated


def get_user_by_token(authorization: Annotated[str | None, Header(...)] = None):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = authorization.split("Bearer ")[1]

    try:
        response = requests.post(
            f"http://localhost:8001/verify-token/",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Token invalid")

        print(response)
        return response.json()

    except Exception as e:
        print(e)
        # Handle any other unexpected exceptions
        raise HTTPException(status_code=401, detail="An error occurred while verifying token")
