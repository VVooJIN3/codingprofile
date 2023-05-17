from flask import Flask, render_template, request, jsonify
from datetime import datetime
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca=certifi.where()

# 조우진 : mongodb+srv://sparta:test@cluster0.89nsamy.mongodb.net/?retryWrites=true&w=majority
client = MongoClient('mongodb+srv://sparta:test@cluster0.mctj20j.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    #기본 페이지 불러오기
   return render_template('index.html')

@app.route('/subin')
def subinpage():
    #멤버 수빈 페이지 불러오기
   return render_template('subin.html')

@app.route("/guestbook", methods=["POST"])
def guestbook_post():
    
    name_receive = request.form['name_give']
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']
    comment_receive = request.form['comment_give']
    doc = {
        'name' : name_receive,
        'id' : id_receive,
        'password' : password_receive,
        'comment' : comment_receive
    }
    db.guestbook.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})

@app.route("/guestbook", methods=["GET"])
def guestbook_get():
    all_comments = list(db.guestbook.find({}, {'_id': False}))
    return jsonify({'result': all_comments})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)