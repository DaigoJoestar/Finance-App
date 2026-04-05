from flask import Flask
from config import Config
from extensions import db, migrate, jwt
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.record_routes import record_bp
from routes.dashboard_routes import dashboard_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(record_bp, url_prefix='/api/records')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

    @app.cli.command('seed')
    def seed_admin():
        from models import User
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com', role='admin', active=True)
            admin.set_password('adminpass')
            db.session.add(admin)
            db.session.commit()
            print("Admin created: admin / adminpass")
        else:
            print("Admin already exists.")
    return app