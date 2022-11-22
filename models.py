from redis_om import get_redis_connection,JsonModel,EmbeddedJsonModel,Field,Migrator
import datetime

redis = get_redis_connection(
    host = "redis-15502.c258.us-east-1-4.ec2.cloud.redislabs.com",
    port = 15502,
    password = "EJSzsC24rap3y1UaUnyPhRiALpezG41R",
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