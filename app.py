# 역할 분담
# 최신혜 : 페이지 이동
# 박행복 : 방명록 조회
# 이경원 : 방명록 작성
# 조우진 : 방명록 수정/삭제
# 박수빈 : 메인 페이지 프론트엔드
# 공통 : 개인 프로필 프론트엔드

from flask import Flask, render_template, request, jsonify
from datetime import datetime,timedelta
app = Flask(__name__)

from pymongo import MongoClient
import certifi
from bson import ObjectId
import logging
import requests


# 조우진 : mongodb+srv://sparta:test@cluster0.89nsamy.mongodb.net/?retryWrites=true&w=majority
# 박수빈 : mongodb+srv://sparta:test@cluster0.mctj20j.mongodb.net/?retryWrites=true&w=majority
# 이경원 : mongodb+srv://sparta:test@cluster0.atah4wp.mongodb.net/?retryWrites=true&w=majority
# 박행복 : mongodb+srv://sparta:test@cluster0.mctqe10.mongodb.net/?retryWrites=true&w=majority
ca = certifi.where()
client = MongoClient('mongodb+srv://sparta:test@cluster0.89nsamy.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)

db = client.dbsparta


#페이지 이동하기
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/subin')
def subinpage():
    #멤버 수빈 페이지 불러오기
   return render_template('subin.html')

@app.route('/woojin')   
def woojinpage():
    #멤버 우진 페이지 불러오기
   return render_template('woojin.html')

@app.route('/happiipark')   
def happypage():
    #멤버 행복 페이지 불러오기
   return render_template('happy.html')

@app.route('/lee')  
def kyeongwonpage():
    #멤버 경원 페이지 불러오기
   return render_template('kyeongwon.html')

@app.route('/choi')  
def choipage():
    #멤버 경원 페이지 불러오기
   return render_template('choi.html')


# 조우진 : 방명록 수정, 삭제하기

#방명록 삭제하기
@app.route('/guestbook/2',methods=["DELETE"])
def guestbook_delete():
    objectId_receive = request.form['objectId_give'] #db 키(_id)값
    targetpassword_receive = request.form['targetpassword_give']

    target = db.guestbook.find_one({'_id':ObjectId(objectId_receive)}) #댓글 테이블에 (_id)값을 가진 아이디와 댓글이 있는지 확인
    if target['password'] != targetpassword_receive: #입력한 비밀번호가 다를 때
        return jsonify({'result':'fail', 'msg': '비밀번호가 틀립니다.'})
    else: # 입력한 비밀번호가 맞을 때
        db.guestbook.delete_one(target)
        return jsonify({'result':'success', 'msg': '삭제가 완료되었습니다.'})    


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
            
#이경원 : 박명록 작성하기
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
    name_give = request.args.get('name',"")
    print(name_give)
    all_guestbook = list(db.guestbook.find({"name":name_give})) #방명록 이름에 맞게 가져오도록 수정
    
    for guestbook in all_guestbook:#[_id값을 string 타입으로 변경하여 전달]
        objectid = guestbook["_id"]
        guestbook["_id"]=str(guestbook["_id"])
    return jsonify({'result':all_guestbook})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
