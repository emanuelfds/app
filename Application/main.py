from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from prometheus_client import make_wsgi_app
from flask_prometheus_metrics import register_metrics
from .views import bp
from .uptime import start_uptime_thread
from . import config

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    register_metrics(app, app_version=config.APP_VERSION, app_config=config.APP_CONFIG)
    return app

if __name__ == "__main__":
    app = create_app()
    start_uptime_thread()
    app_dispatch = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})
    run_simple("0.0.0.0", 5000, app_dispatch)