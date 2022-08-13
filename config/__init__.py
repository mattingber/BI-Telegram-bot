"""Loads environment variables"""
from pydantic import BaseSettings
from os import environ as env
from dotenv import load_dotenv

# Define the elasticConnectionSettings class (inherits from BaseSettings)


class ConnectionSettings(BaseSettings):
    load_dotenv(dotenv_path=".env")
    TELEGRAM_API_TOKEN: str = env['TELEGRAM_API_TOKEN']
    ELASTICSEARCH_HOST: str = env['ELASTICSEARCH_HOST']
    ELASTIC_USER: str = env['ELASTIC_USER']
    ELASTIC_PASSWORD: str = env['ELASTIC_PASSWORD']

class Config(ConnectionSettings):
    pass

config = Config()