import os
from dotenv import load_dotenv
from fastapi import FastAPI
from settings import settings

print(settings.mysql_uri)