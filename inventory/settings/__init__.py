import os

environment = os.getenv("ENVIRONMENT", "development").lower()

if environment == "production":
    from .production import *  # noqa: F401,F403
else:
    from .development import *  # noqa: F401,F403
