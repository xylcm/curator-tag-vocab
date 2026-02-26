"""
Flask application factory for the curator tag vocabulary application.
"""

import os
from flask import Flask

from .config import get_config
from .utils.error_handlers import register_error_handlers
from .utils.logging_config import setup_logging


def create_app(config_name: str = None) -> Flask:
    """Create and configure the Flask application.

    Args:
        config_name: Configuration environment name (development, testing, production)

    Returns:
        Configured Flask application
    """
    # Load configuration
    config = get_config(config_name)

    # Setup logging
    setup_logging(level=logging.DEBUG if config.DEBUG else logging.INFO)

    # Create Flask app
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static',
        instance_relative_config=True,
    )

    # Configure paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app.template_folder = os.path.join(base_dir, 'templates')
    app.static_folder = os.path.join(base_dir, 'static')

    # Load config
    app.config.from_object(config)

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints
    from .api.routes import api_bp
    app.register_blueprint(api_bp)

    return app


import logging


def main():
    """Main entry point for running the application."""
    config = get_config()
    app = create_app()

    port = config.PORT
    host = config.HOST
    debug = config.DEBUG

    print(f"Tag Manager: http://localhost:{port}/tagging/vocab\n")
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
