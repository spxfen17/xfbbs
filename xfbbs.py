from flask import Flask
from apps.cms import bp as cms_bp
from apps.common import bp as common_bp
from apps.front import bp as front_bp
from apps.ueditor import bp as ueditor_bp
from exts import db,mail,alidayu
import config

# from flask_wtf import CSRFProtect


def create_app():
    app = Flask(__name__)

    app.register_blueprint(cms_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(ueditor_bp)

    app.config.from_object(config)
    db.init_app(app)
    mail.init_app(app)
    alidayu.init_app(app)
    # CSRFProtect(app)

    return app





if __name__ == '__main__':
    app = create_app()
    app.run()
