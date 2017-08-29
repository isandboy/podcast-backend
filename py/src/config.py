import os

# Ensure Python path
basedir = os.path.abspath(os.path.dirname(__file__))

# Database info
DB_USERNAME  = os.environ['DB_USERNAME']
DB_PASSWORD  = os.environ['DB_PASSWORD']
DB_HOST      = os.environ['DB_HOST']
DB_NAME      = os.environ['DB_NAME']
DB_URL       = 'mysql://{}:{}@{}/{}'.format(
  DB_USERNAME,
  DB_PASSWORD,
  DB_HOST,
  DB_NAME
)

# Separate DB for podcast-specific stuff
PODCAST_DB_USERNAME = os.environ['PODCAST_DB_USERNAME']
PODCAST_DB_PASSWORD = os.environ['PODCAST_DB_PASSWORD']
PODCAST_DB_HOST     = os.environ['PODCAST_DB_HOST']
PODCAST_DB_NAME     = os.environ['PODCAST_DB_NAME']
PODCAST_DB_URL      = 'mysql://{}:{}@{}/{}'.format(
  PODCAST_DB_USERNAME,
  PODCAST_DB_PASSWORD,
  PODCAST_DB_HOST,
  PODCAST_DB_NAME
)

class Config(object):
  DEBUG = False
  TESTING = False
  CSRF_ENABLED = True
  CSRF_SESSION_KEY = "secret"
  SECRET_KEY = "not_this"
  THREADS_PER_PAGE = 2

  # Mounting our DBs
  SQLALCHEMY_BINDS = {
    'db': DB_URL,
    'podcast_db': PODCAST_DB_URL
  }

class ProductionConfig(Config):
  DEBUG = False

class StagingConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class DevelopmentConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class TestingConfig(Config):
  TESTING = True
