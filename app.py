from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://sparta:test@cluster0.atah4wp.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('kyeongwon.html')

@app.route('/guestbook', methods=['POST'])
def guestbook_post():
   name_receive = request.form['name_give']
   id_receive = request.form['id_give']
   password_receive = request.form['password_give']
   comment_receive = request.form['comment_give']
   doc = {
        'name':name_receive,
        'id':id_receive,
        'password':password_receive,
        'comment':comment_receive
    }
   db.guestbook.insert_one(doc)

   return jsonify({'msg': '저장완료!'})

@app.route("/guestbook", methods=["GET"])
def guestbook_get():
    guestbook_data = list(db.guestbook.find({},{'_id':False}))
    return jsonify({'result': guestbook_data})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)