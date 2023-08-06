import os

RIVER_HOME = os.getenv("RIVER_HOME", os.getcwd())

POSTGRESQL_USER = os.getenv("POSTGRESQL_USER", "river")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD", "river")
POSTGRESQL_HOST = os.getenv("POSTGRESQL_HOST", "127.0.0.1")
POSTGRESQL_DB = os.getenv("POSTGRESQL_DB", "river")
SQLALCHEMY_DATABASE_URI = "postgresql://%s:%s@%s/%s" % \
                          (POSTGRESQL_USER,
                           POSTGRESQL_PASSWORD,
                           POSTGRESQL_HOST,
                           POSTGRESQL_DB)

STATIC_FOLDER = os.path.join(RIVER_HOME, "client")
TEMPLATE_FOLDER = os.path.join(RIVER_HOME, "client/templates")


SQLALCHEMY_DATABASE_URI = "sqlite:///{}/.river/river.db".format(RIVER_HOME)
