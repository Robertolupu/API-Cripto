from controllers.controller_graphics import *

def graphics_routes(app):
    app.route("/api/graphic", methods=['GET'])(get_graphic)