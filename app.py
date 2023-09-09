from flask import Flask,render_template,request
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
import os
import json
import requests
global i
i=0

global total_amount
total_amount = 0



app = Flask(__name__)

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = "static/files"


class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")


@app.route('/',methods = ['GET','POST'])

@app.route('/home',methods = ['GET','POST'])


def home():
    global i
    global total_amount
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        url = 'https://ocr2.asprise.com/api/v1/receipt'
        image = "static/files/"+ file.filename
        res = requests.post(url,
                           data={
                               'api_key':'TEST',
                               'recognizer':'auto',
                               'ref_no':'ocr_python_api'
                           },
                            files={
                                'file':open(image,'rb')
                                
                            }
                           )
        i=i+1
        with open("response"+str(i)+".json",'w') as f:
            json.dump(json.loads(res.text),f)
        

        with open("response"+str(i)+".json","r") as f:
            data = json.load(f)


        invoice_date = data['receipts'][0]['date']
        invoice_receipt_no = data['receipts'][0]['receipt_no']
        invoice_merchant_name = data['receipts'][0]['merchant_name']
        invoice_merchant_tax_no = data['receipts'][0]['merchant_tax_reg_no']
        invoice_merchant_address = data['receipts'][0]['merchant_address']
        invoice_items = data['receipts'][0]['items']
        invoice_total = data['receipts'][0]['total']
        # if type(invoice_total) == 'NoneType':
        #     invoice_total = 0
        total_amount += invoice_total
        # return data['receipts'][0]['merchant_name'], data['receipts'][0]['date'] 
        # return '{} {} {} {} {} {} {} {}'.format(invoice_date,invoice_receipt_no,invoice_merchant_name,invoice_merchant_tax_no,invoice_merchant_address,invoice_items,invoice_total,total_amount)
        return render_template('result.html',
                               image=image,
                               invoice_date=invoice_date,
                               invoice_receipt_no=invoice_receipt_no,
                               invoice_merchant_name=invoice_merchant_name,
                               invoice_merchant_tax_no=invoice_merchant_tax_no,
                               invoice_merchant_address=invoice_merchant_address,
                               invoice_items=invoice_items,
                               invoice_total=invoice_total,
                               total_amount=total_amount)
    return render_template('index.html', form = form)


if __name__ == '__main__':
    app.run(debug=True)