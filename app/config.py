import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', default="hassan's_super_secret_key_that_nobody_will_decode")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
