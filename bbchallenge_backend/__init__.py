from os import getenv

from flask import Flask
from flask_cors import CORS
from redis import Redis


from bbchallenge_backend.ping import ping_bp
from bbchallenge_backend.machines import machines_bp
from bbchallenge_backend.metrics import metrics_bp


import os

import redis


def create_app(config={}):

    app = Flask(__name__)
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))

    app.r = redis.Redis()
    # if "TESTING" not in config:
    #     config["TESTING"] = False

    # if getenv("ENV") is not None:
    #     config["ENV"] = getenv("ENV")

    # app.config.update(config)

    # app.mongo = PyMongo(app)

    # # Email API
    # if not "POSTMARK_API_KEY" in app.config:
    #     print("No Postmark key was given. Abort.")
    #     sys.exit(-1)

    # app.postmark = PostmarkClient(server_token=app.config["POSTMARK_API_KEY"])

    app.register_blueprint(ping_bp)
    app.register_blueprint(machines_bp)
    app.register_blueprint(metrics_bp)
    CORS(app, supports_credentials=True)
    return app


app = create_app()

# This allows the client to read the Content-Disposition header
@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
    return response


# @app.before_request
# def check_user_is_logged():
#     if request.method == "OPTIONS":
#         return

#     print(request, request.endpoint, session)
#     if request.endpoint == "auth.login":
#         return
#     if "email" not in session:
#         return "Not Authorized", 403