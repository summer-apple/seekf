# encoding:utf-8
import datetime
import os

import simplejson
from flask import Flask,request, render_template, send_from_directory
from flask import flash
from flask import redirect
from flask import url_for
from werkzeug.utils import secure_filename
from global_param  import *

from export import Exporter
from order import OrderService
from input import ExcelParser


"""
seekf
	添加订单
	删除订单
	订单列表
	今日汇总
	月汇总
"""

ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

odsvs = OrderService()


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/<filename>', methods=['GET'])
def route_to_page(filename):
    return render_template(filename)



@app.route('/orders/<trans_day>', methods=['GET'])
def get_orders(trans_day):
    if trans_day is None or trans_day == '':
        trans_day = datetime.datetime.now().strftime('%Y-%m-%d')

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
    args.append(x['defective'])

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


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return ''


@app.route('/export/<trans_date>', methods=['GET'])
def export(trans_date):
    e = Exporter()
    filename = e.export(trans_date)
    return send_from_directory('excel',filename,as_attachment=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))



            parser = ExcelParser(filename)
            parser.parser()


            return redirect('/export/'+ filename)



    return '''
    <!doctype html>
    <title>上传原始数据文件</title>
    <h1>格式：2017-04-21.xlsx 月份日期的0不能省略</h1>
    <h1>上传原始数据文件</h1>
    <h2>点击上传后会自动下载统计好的文件</h2>
    <h3>如有问题请呼叫你的大可爱</h3>
    <form method=post enctype=multipart/form-data>
      <input type='file' name='file' style="width:300px;height:30px;display:block;">
      <br><br>
      <input type='submit' value='上传' style="width:100px;height:30px;display:block;">
    </form>
    '''




if __name__ == '__main__':
    app.run()
