from fastapi import HTTPException, Header
import requests

from typing import Annotated

from os import environ as env

ACCOUNT_SERVICE_HOST = env.get('ACCOUNT_SERVICE_HOST')
ORDER_SERVICE_HOST = env.get('ORDER_SERVICE_HOST')


def get_user(authorization: Annotated[str | None, Header(...)] = None):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split("Bearer ")[1]
    try:
        response = requests.get(
            f"{ACCOUNT_SERVICE_HOST}/verify-token/",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()  # Raise an exception for non-2xx status codes
    except requests.RequestException as e:
        if e.response is not None:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.json())
        # Handle connection errors and other issues
        raise HTTPException(status_code=401, detail=f"An error occurred while verifying the token")


def get_order(order_id: int):
    try:
        response = requests.get(f"{ORDER_SERVICE_HOST}/get-order/{order_id}")
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()  # Raise an exception for non-2xx status codes
    except requests.RequestException as e:
        if e.response is not None:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.json())

        # Handle connection errors and other issues
        raise HTTPException(status_code=500, detail=f"An error occurred while checking the order")
