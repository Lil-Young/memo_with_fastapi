from fastapi import Request
from settings import Settings

def app_settings(request: Request) -> Settings:
    """Settings Controller"""
    return request.app.settings