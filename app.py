from flask import Flask, render_template, request, jsonify
from datetime import datetime
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca=certifi.where()

# 조우진 : mongodb+srv://sparta:test@cluster0.89nsamy.mongodb.net/?retryWrites=true&w=majority
client = MongoClient('mongodb+srv://sparta:test@cluster0.89nsamy.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    #기본 페이지 불러오기
   return render_template('index.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)