import os

from dotenv import load_dotenv
from yoomoney import Authorize


load_dotenv()


def _get_required_env(name: str) -> str:
    value = os.getenv(name)
    if value:
        return value
    raise RuntimeError(f"Environment variable {name} is required")


Authorize(
    client_id=_get_required_env("YOOMONEY_CLIENT_ID"),
    redirect_uri=_get_required_env("YOOMONEY_REDIRECT_URI"),
    scope=[
        "account-info",
        "operation-history",
        "operation-details",
        "incoming-transfers",
        "payment-p2p",
        "payment-shop",
    ],
)
