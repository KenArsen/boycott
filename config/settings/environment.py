import os

from environs import Env

env = Env()
env_file = os.getenv("ENV_FILE", ".env")
env.read_env(env_file)
