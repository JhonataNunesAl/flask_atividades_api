import pytest
import os
import sys
from config import app, db
from controllers.atividadeCONTROLLER import atividades_blueprint

def create_app():
    app.register_blueprint(atividades_blueprint, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    # ELE SÓ VAI INICIAR SE TODOS OS BLUEPRINTS INICIAREM TAMBÉM!!!
    app = create_app()  
    app.run(host=app.config["HOST"], port=app.config['PORT'], debug=app.config['DEBUG'])