from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("experiment.config.Config")

    from .routes import bp

    app.register_blueprint(bp)
    return app
