from redis_om import get_redis_connection,JsonModel,EmbeddedJsonModel,Field,Migrator
import datetime
import os
from dotenv import load_dotenv




load_dotenv()

redis = get_redis_connection(
    host = os.environ.get("HOST"),
    port = os.environ.get("PORT"),
    password = os.environ.get("PASSWORD"),
    decode_responses = True,
)

class Author(EmbeddedJsonModel):
    firstname: str = Field(index=True,full_text_search=True)
    lastname: str
    email: str
    bio: str
    date_joined: datetime.date = Field(default=datetime.datetime.now())

    class Meta:
        database = redis

class Blog(JsonModel):
    title: str = Field(index=True,full_text_search=True)
    content: str
    author: Author
    date_posted: datetime.date = Field(default = datetime.datetime.today().strftime("%Y-%m-%d"))

    class Meta:
        database = redis

Migrator().run()