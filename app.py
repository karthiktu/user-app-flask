from flask import Flask, Blueprint
from api.users import users


app = Flask(__name__)
app.register_blueprint(users.users)


if __name__ == '__main__':
    app.run()
    
    