from app import db
from app import Tweet
from sqlalchemy import desc
from datetime import datetime
from datetime import timedelta

'''print(Tweet.query.first())
# newest item = largest date -> order descending
print(Tweet.query.order_by(desc(Tweet.created_at)).limit(3).all())

# This line retrieves the newest item
print(Tweet.query.order_by(desc(Tweet.created_at)).first())'''
print(Tweet.query.order_by(desc(Tweet.created_at)).first().created_at)
date = Tweet.query.order_by(desc(Tweet.created_at)).first().created_at
print(date.day)

print(datetime.isoformat(date)+'Z')

'''print(datetime.now()-date > timedelta(days=7))
print(datetime.now()-date > timedelta(days=21))'''




print('Hellow world')