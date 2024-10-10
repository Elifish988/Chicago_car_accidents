from flask import Flask

from blue_prins.initial_database_bp import bp_init
from repository.csv_repository import init_accidents
from repository.querys_repository import count_accidents_by_region

app = Flask(__name__)

# app.register_blueprint(bp_init)

init_accidents()
count_accidents_by_region('225')
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
