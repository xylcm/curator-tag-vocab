
import sys
import os
from flask import Flask
from src.routers import tag_manager

def create_tagging_app(config_name='development'):
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static',
        instance_relative_config=True
    )
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app.template_folder = os.path.join(base_dir, 'templates')
    app.static_folder = os.path.join(base_dir, 'static')
    
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['DEBUG'] = True if config_name == 'development' else False
    
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    
    app.register_blueprint(tag_manager.bp)
    
    return app

if __name__ == '__main__':
    app = create_tagging_app()
    port = int(os.environ.get('PORT', 80))
    print(f"Tag Manager: http://localhost:{port}/tagging/vocab\n")
    app.run(host='0.0.0.0', port=port, debug=True)

