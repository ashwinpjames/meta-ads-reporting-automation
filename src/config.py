"""Application configuration loaded from environment variables."""

import os

from dotenv import load_dotenv

load_dotenv()


def get_meta_config() -> dict[str, str]:
    """Return Meta API configuration without exposing credentials in logs."""
    return {
        "access_token": os.getenv("META_ACCESS_TOKEN", "").strip(),
        "ad_account_id": os.getenv("META_AD_ACCOUNT_ID", "").strip(),
        "api_version": os.getenv("META_API_VERSION", "").strip(),
    }
