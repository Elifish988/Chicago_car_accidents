from flask import Flask

from blue_prins.initial_database_bp import bp_init
from blue_prins.quwrys_bp import bp_query
from repository.csv_repository import init_accidents
from repository.querys_repository import count_accidents_by_region, count_accidents_by_region_and_period, \
    count_accidents_by_cause_and_region

app = Flask(__name__)

app.register_blueprint(bp_init)
app.register_blueprint(bp_query)

init_accidents()
# print(count_accidents_by_region('225'))
# print(count_accidents_by_region_and_period('225', 'month', '18/09/2023'))
# print(count_accidents_by_cause_and_region('225'))
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
