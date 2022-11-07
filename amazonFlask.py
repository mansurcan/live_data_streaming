
from flask import Flask, jsonify, render_template
import pandas as pd

# creating a Flask app
app = Flask(__name__)

@app.route('/amazon')
def home():

    lst1=pd.read_csv("/home/cdp/amazon.csv")
    data = lst1.to_json(orient='records')

    return data
    #return render_template('table.html', tables=[lst1.to_html()], titles=[''])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7070)

