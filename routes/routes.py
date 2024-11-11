from controllers.controller_cryptos import *
from controllers.controller_users import *
from controllers.controller_tokens import *

def cryptos_routes(app):
    app.route("/api/crypto/graphic", methods=['GET'])(get_graphic)
    app.route("/api/crypto/value", methods=['GET'])(get_value)

def users_routes(app):
    app.route("/api/login", methods=['POST'])(login)
    app.route("/api/register", methods=['POST'])(register)

def tokens_routes(app):
    app.route("/api/token", methods=['GET'])(check_token)
    app.route("/api/token", methods=['DELETE'])(logout)