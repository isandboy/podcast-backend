import datetime
import time
from app.pcasts.dao import users_dao, episodes_dao, series_dao
from . import *

def get_followings(user_id):
  followings = \
    Following.query.filter(Following.follower_id == user_id).all()

  return followings

def get_followers(user_id):
  followers = \
    Following.query.filter(Following.followed_id == user_id).all()

  return followers

def create_following(follower_id, followed_id):
  if int(follower_id) != int(followed_id):
    following = Following(follower_id=follower_id, followed_id=followed_id)
    users = users_dao.get_users_by_id(follower_id, [follower_id, followed_id])
    if len(users) == 2:
      follower = users[0] if users[0].id == follower_id else users[1]
      followed = users[0] if users[0].id == followed_id else users[1]
      follower.followings_count += 1
      followed.followers_count += 1
    else:
      raise Exception("Improper follower_id and/or followed_id")
  else:
    raise Exception("follower_id cannot equal followed_id")

  return db_utils.commit_model(following)

def delete_following(follower_id, followed_id):
  maybe_following = Following.query \
    .filter(Following.follower_id == follower_id,
            Following.followed_id == followed_id) \
    .first()

  if maybe_following:
    users = users_dao.get_users_by_id(follower_id, [follower_id, followed_id])
    follower = users[0] if users[0].id == follower_id else users[1]
    followed = users[0] if users[0].id == followed_id else users[1]
    follower.followings_count -= 1
    followed.followers_count -= 1
    db_utils.delete_model(maybe_following)
  else:
    raise Exception("Specified following does not exist")

def get_following_recommendations(user_id, maxtime, page_size):
  followings = get_followings(user_id)
  following_ids = [f.followed_id for f in followings]
  maxdatetime = datetime.datetime.fromtimestamp(int(maxtime))
  recommendations = Recommendation.query \
    .filter(Recommendation.user_id.in_(following_ids),
            Recommendation.created_at <= maxdatetime) \
    .order_by(Recommendation.created_at.desc()) \
    .limit(page_size) \
    .all()
  episodes = episodes_dao.get_episodes([r.episode_id for r in recommendations],
                                       user_id)
  for r, e in zip(recommendations, episodes):
    r.episode = e
  return recommendations

def get_following_subscriptions(user_id, maxtime, page_size):
  followings = get_followings(user_id)
  following_ids = [f.followed_id for f in followings]
  maxdatetime = datetime.datetime.fromtimestamp(int(maxtime))
  subscriptions = Subscription.query \
    .filter(Subscription.user_id.in_(following_ids),
            Subscription.created_at <= maxdatetime) \
    .order_by(Subscription.created_at.desc()) \
    .limit(page_size) \
    .all()
  series = series_dao.get_multiple_series([s.series_id for s in subscriptions],
                                          user_id)
  for sub, ser in zip(subscriptions, series):
    sub.series = ser
  return subscriptions