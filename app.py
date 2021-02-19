from flask import Flask, render_template, jsonify
from main import get_all_data
from get_resource_dynamo import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def get_data_from_db():
    data = get_all_data()
    return render_template('data.html', data=data)


# @app.route('/livedata')
# def get_updated_data_from_db():


@app.route('/livedata', methods=['POST'])
def updatedecimal():
    temp = Device.create_from_dict
    return jsonify('', render_template('random_decimal_model.html', x=temp))


if __name__ == '__main__':
    app.run()

