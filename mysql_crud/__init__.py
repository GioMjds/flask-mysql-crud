from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from mysql_crud.crud_operation.crud import crud
    app.register_blueprint(crud)
    
    return app