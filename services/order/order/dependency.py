from fastapi import HTTPException, Header
import requests

from typing import Annotated

from os import  environ as env

ACCOUNT_SERVICE_URL = env.get("ACCOUNT_SERVICE_URL")
CART_SERVICE_URL = env.get("CART_SERVICE_URL")
PRODUCT_SERVICE_URL = env.get("PRODUCT_SERVICE_URL")


def get_user_cart(authorization: Annotated[str | None, Header(...)] = None):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split("Bearer ")[1]
    try:
        response = requests.get(
            f"{CART_SERVICE_URL}/get-cart/",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()  # Raise an exception for non-2xx status codes
    except requests.RequestException as e:
        if e.response is not None:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.json())
        # Handle connection errors and other issues
        raise HTTPException(status_code=401, detail=f"An error occurred while getting the cart")


def get_user(authorization: Annotated[str | None, Header(...)] = None):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split("Bearer ")[1]
    try:
        response = requests.get(
            f"{ACCOUNT_SERVICE_URL}/verify-token/",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()  # Raise an exception for non-2xx status codes
    except requests.RequestException as e:
        if e.response is not None:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.json())
        # Handle connection errors and other issues
        raise HTTPException(status_code=401, detail=f"An error occurred while getting the cart")


def get_product(product_id: int):
    try:
        response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()  # Raise an exception for non-2xx status codes
    except requests.RequestException as e:
        if e.response is not None:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.json())

        # Handle connection errors and other issues
        raise HTTPException(status_code=500, detail=f"An error occurred while checking the product")


def get_product_stock(product_id: int):
    try:
        response = requests.get(f"{PRODUCT_SERVICE_URL}/products/check-stock/{product_id}")
        if response.status_code == 200:
            return response.json()
        response.raise_for_status()  # Raise an exception for non-2xx status codes
    except requests.RequestException as e:
        if e.response is not None:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.json())

        # Handle connection errors and other issues
        raise HTTPException(status_code=500, detail=f"An error occurred while checking the stock")
