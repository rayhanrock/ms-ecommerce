from fastapi import HTTPException, Header
import requests
from fastapi import Query

from typing import Annotated

from os import environ as env

ACCOUNT_SERVICE_URL = env.get("ACCOUNT_SERVICE_URL")


def get_user_by_token(authorization: Annotated[str | None, Header(...)] = None):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split("Bearer ")[1]
    try:
        response = requests.get(
            f"{ACCOUNT_SERVICE_URL}/verify-token/",
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()  # Raise an exception for non-2xx status codes
    except requests.RequestException as e:
        if e.response.status_code == 401:
            raise HTTPException(status_code=401, detail="Invalid token")
        # Handle connection errors and other issues
        raise HTTPException(status_code=401, detail=f"An error occurred while verifying the token")

    return response.json()


class ProductQueryParams:
    def __init__(
            self,
            skip: int = Query(0, description="Number of items to skip", ge=0),
            limit: int = Query(100, description="Maximum number of items to retrieve", ge=1, le=100),
            category_id: int = Query(None, description="Category ID for filtering products"),
            search_query: str = Query(None, description="Search query for product names"),
            sort_order: str = Query(None, description="Sorting order for prices", enum=["low_to_high", "high_to_low"])
    ):
        self.skip = skip
        self.limit = limit
        self.category_id = category_id
        self.search_query = search_query
        self.sort_order = sort_order
