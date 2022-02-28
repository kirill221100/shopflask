import os

current_path = os.path.dirname(os.path.realpath(__file__))

db_path = "sqlite:///" + current_path + "//db.db"

class Config:
    DEBUG = True
    SECRET_KEY = "rueruwahwatwq3pij32q9rjtg4wijpt49iyej9e4j9twjgrdipgvjer0y9uhyjn.orp9-aeuq2-3er-f[whgo"
    SQLALCHEMY_DATABASE_URI = db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False