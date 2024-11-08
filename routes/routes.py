from controllers.controller_graphics import *
from controllers.controller_users import *
from controllers.controller_tokens import *

def graphics_routes(app):
    app.route("/api/graphic", methods=['GET'])(get_graphic)

def users_routes(app):
    app.route("/api/login", methods=['POST'])(login)
    app.route("/api/register", methods=['POST'])(register)

def tokens_routes(app):
    app.route("/api/token", methods=['GET'])(check_token)
    app.route("/api/token", methods=['DELETE'])(logout)