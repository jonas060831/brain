from dotenv import load_dotenv, find_dotenv
import os

#load the .env file
load_dotenv(find_dotenv())


print(os.getenv('SECRET_PHRASE'))
