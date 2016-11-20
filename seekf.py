import datetime

import simplejson
from flask import Flask,request, render_template

from order import OrderService

"""
seekf
	添加订单
	删除订单
	订单列表
	今日汇总
	月汇总
"""


app = Flask(__name__)
odsvs = OrderService()

class Order():
    def __init__(self, **kvs):
        self.__dict__.update(kvs)


@app.route('/', methods=['POST','GET'])
def hello_world():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        return request.form['name']

@app.route('/<filename>', methods=['GET'])
def route_to_page(filename):
    return render_template(filename)

@app.route('/orders/<trans_day>', methods=['GET'])
def get_orders(trans_day):
    if trans_day is None or trans_day == '':
        trans_day = datetime.datetime.now().strftime('%Y-%m-%d')
    # TODO
    trans_day = '2016-10-23'
    result = odsvs.get_orders_by_date(trans_day)
    return simplejson.dumps(result)

@app.route('/orders/<order_id>', methods=['GET'])
def get_order_by_id(order_id):
    result = odsvs.get_order_by_id(order_id)
    return simplejson.dumps(result)


@app.route('/orders/', methods=['PUT'])
def add_order():
    x = request.form
    args = list()

    args.append(x['trans_day'])
    args.append(x['model'])
    args.append(x['packages'])
    args.append(x['pairs'])
    args.append(x['price'])
    args.append(x['discount'])
    args.append(x['amount'])

    try:
        odsvs.create_order(args)
        return '0'
    except Exception as e:
        return e


@app.route('/orders/<order_id>', methods=['DELETE'])
def delete_order_by_id(order_id):
    try:
        odsvs.delete_order_by_id(order_id)
        return '0'
    except Exception as e:
        return e

@app.route('/stat/<trans_day>/model-price', methods=['GET'])
def stat_day_by_model_price(trans_day):
    result = odsvs.stat_by_model_price(trans_day)
    return simplejson.dumps(result)

@app.route('/stat/<trans_day>/model', methods=['GET'])
def stat_day_by_model(trans_day):
    result = odsvs.stat_by_model(trans_day)
    return simplejson.dumps(result)






if __name__ == '__main__':
    app.run()
