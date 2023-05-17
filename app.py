from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://sparta:test@cluster0.mctqe10.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

import logging

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/happiipark')
def happy():
    return render_template('happy.html')

@app.route("/savecomment", methods=["POST"])
def savecomment_post():

    count = list(db.guestbook.find({}, {'_id':False})) #db 데이터 수를 카운트
    num = len(count) + 1  # 카운트 한 수에 1을 더해서 새로운 데이터 카운트

    # 화면에서 넘어 오는 값
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    doc = {
    'id':id_receive,
    'pw':pw_receive,
    'name':name_receive,
    'comment':comment_receive,
    'num' : num
}
    
    
    # headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    # data = requests.get(url_receive,headers=headers)

    # soup = BeautifulSoup(data.text, 'html.parser')

    # # 여기에 코딩을 해서 meta tag를 먼저 가져와보겠습니다.
    # ogtitle = soup.select_one('meta[property="og:title"]')['content']
    # ogdesc = soup.select_one('meta[property="og:description"]')['content']
    # ogimage = soup.select_one('meta[property="og:image"]')['content']

   

    db.guestbook.insert_one(doc)
    
    return jsonify({'msg':'방명록 저장완료!'})



@app.route("/deletecomment", methods=["POST"])
def deletecomment_post():

    delete_receive = request.form["num_give"]
    # logging.warn("loglog"+ delete_receive)
    
    db.guestbook.delete_one({'num': int(delete_receive)})
    return jsonify({'msg':'방명록 삭제완료!'})



@app.route("/check", methods=["POST"])
def check_post():

    pw_receive = request.form["pw_give"]
    num_receive = request.form["num_give"]

    print("전달 받은 패스워드 : "+ pw_receive+ "디비 넘버"+ int(num_receive))

    a = list(db.guestbook.find({'pw':pw_receive, 'num':int(num_receive)},{'_id':False}))
    b = list(db.guestbook.find({'num':int(num_receive)},{'_id':False}))

    for i in a:
        print(i)


    logging.warn("")


    for i in b:
        print(i)


    

    
    
    # db.guestbook.delete_one({'num': int(delete_receive)})
    return jsonify({'msg':'본인 확인 완료!'})



@app.route("/guestbook", methods=["GET"])
def guestbook_get():
    guestbook = list(db.guestbook.find({},{'_id':False}))
    return jsonify({'result':guestbook})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
