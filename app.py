#pip install flask requests dnspython pymongo
from flask import Flask, render_template, request, jsonify
from datetime import datetime,timedelta
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca=certifi.where()

from bson import ObjectId

# 조우진 : mongodb+srv://sparta:test@cluster0.89nsamy.mongodb.net/?retryWrites=true&w=majority
# 박수빈 : mongodb+srv://sparta:test@cluster0.mctj20j.mongodb.net/?retryWrites=true&w=majority
client = MongoClient('mongodb+srv://sparta:test@cluster0.89nsamy.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


@app.route('/')
def home():
    #기본 페이지 불러오기
   return render_template('woojin.html')
######woojin
#방명록 불러오기 
@app.route('/guestbook',methods=['GET'])
def guestbook_get():
    name_give = request.args.get('name',"")
    print(name_give)
    all_guestbook = list(db.guestbook.find({"name":name_give}))    
    
    for guestbook in all_guestbook:#_id값을 timestmp로 변경하여 html에 전달
        objectid = guestbook["_id"]
        guestbook["_id"]=str(guestbook["_id"])
        timestamp = objectid.generation_time#objectID값을 이용하여 타임스탬프 값 얻기
        korea_timezone = timedelta(hours=9) #UTC와 한국의 시차
        timestamp_kr = timestamp + korea_timezone
        formatted_timestamp = timestamp_kr.strftime("%Y.%m.%d %H:%M:%S")
        guestbook["timestamp"] = formatted_timestamp
    # 지정된 name의 방명록 데이터 모두 가져오기 ,'_id': 가져옴 - 기본값 (true)
    # "_id"값을 html로 넘겨주면 방명록 데이터가 정상 조회되지 않음
    return jsonify({'result': all_guestbook})
    
#방명록 작성하기    
@app.route('/guestbook',methods=['POST'])
def guestbook_add():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']
    print(name_receive,comment_receive,id_receive,password_receive)
    doc = {'name' : name_receive,
           'comment' : comment_receive,
           'id' : id_receive,
           'password' : password_receive
           }
    db.guestbook.insert_one(doc)
    return jsonify({'result':'success', 'msg': '댓글 저장이 완료되었습니다.'})
  
#방명록 삭제하기
@app.route('/guestbook/2',methods=["GET","POST"])
def guestbook_delete():
    #방명록 삭제기능
   return render_template('woojin.html')

#방명록 수정하기
@app.route('/guestbook/3',methods=["POST","PUT"])
def guestbook_update():
    if request.method == "POST": #수정할 방명록을 페이지에서 가져오기
        objectId_receive = request.form['objectId_give'] #db 키(_id)값
        targetpassword_receive = request.form['targetpassword_give']

        target = db.guestbook.find_one({'_id':ObjectId(objectId_receive)}) #댓글 테이블에 (_id)값을 가진 아이디와 댓글이 있는지 확인
        if target['password'] != targetpassword_receive: #입력한 비밀번호가 다를 때
            return jsonify({'result':'fail', 'msg': '비밀번호가 틀립니다.'})
        else: # 입력한 비밀번호가 맞을 때
            return jsonify({'result':'success', 'msg': '수정할 내용을 작성하세요.'})    

    #요청메서드가 PUT인 경우 : 변경 반영
    if request.method == "PUT":                        
        objectId_receive = request.form['objectId_give']
        targetpassword_receive = request.form['targetpassword_give']
        comment_receive = request.form['updatecomment_give']        #새로 작성한 comment 불러오기
        target = db.guestbook.find_one({'_id':ObjectId(objectId_receive)})

        if target['password'] != targetpassword_receive: #비밀번호 한번 더 검증
            return jsonify({'result':'fail', 'msg': '비밀번호가 틀립니다.'})
        else:
            # DB에 수정
            db.guestbook.update_one(target,{'$set':{'comment':comment_receive}})

            return jsonify({'result' : 'success', 'msg' : '수정이 완료되었습니다'})
#####woojin



##################subin
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
####subin


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)