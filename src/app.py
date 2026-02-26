"""Flask application factory."""

import os
from typing import Optional

from flask import Flask

from src.core.config import Config, init_config
from src.api.routes.tags import bp as tags_bp


def create_app(config: Optional[Config] = None) -> Flask:
    """Create and configure Flask application.

    Args:
        config: Optional configuration object. If not provided, uses default config.

    Returns:
        Configured Flask application instance.
    """
    # Initialize config
    app_config = config or init_config()

    # Create Flask app
    app = Flask(
        __name__,
        template_folder=app_config.full_template_folder,
        static_folder=app_config.full_static_folder,
        instance_relative_config=True,
    )

    # Configure app
    app.config["SECRET_KEY"] = app_config.secret_key
    app.config["DEBUG"] = app_config.debug
    app.config["SESSION_COOKIE_HTTPONLY"] = app_config.session_cookie_httponly
    app.config["SESSION_COOKIE_SAMESITE"] = app_config.session_cookie_samesite

    # Register blueprints
    app.register_blueprint(tags_bp)

    return app


def run_app():
    """Run the Flask application."""
    app = create_app()
    port = int(os.environ.get("PORT", 80))
    print(f"Tag Manager: http://localhost:{port}/tagging/vocab\n")
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])


if __name__ == "__main__":
    run_app()
