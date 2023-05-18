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


#########################################################################################################
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
            
# #방명록 불러오기 
# @app.route('/guestbook',methods=['GET'])
# def guestbook_get():
#     name_give = request.args.get('name',"")
#     print(name_give)
#     all_guestbook = list(db.guestbook.find({"name":name_give}))    
    
#     for guestbook in all_guestbook:#_id값을 timestmp로 변경하여 html에 전달
#         objectid = guestbook["_id"]
#         guestbook["_id"]=str(guestbook["_id"])
#         timestamp = objectid.generation_time#objectID값을 이용하여 타임스탬프 값 얻기
#         korea_timezone = timedelta(hours=9) #UTC와 한국의 시차
#         timestamp_kr = timestamp + korea_timezone
#         formatted_timestamp = timestamp_kr.strftime("%Y.%m.%d %H:%M:%S")
#         guestbook["timestamp"] = formatted_timestamp
#     # 지정된 name의 방명록 데이터 모두 가져오기 ,'_id': 가져옴 - 기본값 (true)
#     # "_id"값을 html로 넘겨주면 방명록 데이터가 정상 조회되지 않음
#     return jsonify({'result': all_guestbook})
    
# #방명록 작성하기    
# @app.route('/guestbook',methods=['POST'])
# def guestbook_add():
#     name_receive = request.form['name_give']
#     comment_receive = request.form['comment_give']
#     id_receive = request.form['id_give']
#     password_receive = request.form['password_give']
#     print(name_receive,comment_receive,id_receive,password_receive)
#     doc = {'name' : name_receive,
#            'comment' : comment_receive,
#            'id' : id_receive,
#            'password' : password_receive
#            }
#     db.guestbook.insert_one(doc)
#     return jsonify({'result':'success', 'msg': '댓글 저장이 완료되었습니다.'})
  

###########################################################################
# woojin



############################################################################################################
# 박수빈 : 메인 프론트엔드

# @app.route("/guestbook", methods=["POST"])
# def guestbook_post():
    
#     name_receive = request.form['name_give']
#     id_receive = request.form['id_give']
#     password_receive = request.form['password_give']
#     comment_receive = request.form['comment_give']
#     doc = {
#         'name' : name_receive,
#         'id' : id_receive,
#         'password' : password_receive,
#         'comment' : comment_receive
#     }
#     db.guestbook.insert_one(doc)

#     return jsonify({'msg': '저장 완료!'})

# @app.route("/guestbook", methods=["GET"])
# def guestbook_get():
#     all_comments = list(db.guestbook.find({}, {'_id': False}))
#     return jsonify({'result': all_comments})
#############################################################################################
#subin

#############################################################################################
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

# @app.route("/savecomment", methods=["POST"])
# def savecomment_post():

#     count = list(db.guestbook.find({}, {'_id':False})) #db 데이터 수를 카운트
#     num = len(count) + 1  # 카운트 한 수에 1을 더해서 새로운 데이터 카운트

#     # 화면에서 넘어 오는 값
#     id_receive = request.form['id_give']
#     pw_receive = request.form['pw_give']
#     name_receive = request.form['name_give']
#     comment_receive = request.form['comment_give']

#     doc = {
#     'id':id_receive,
#     'pw':pw_receive,
#     'name':name_receive,
#     'comment':comment_receive,
#     'num' : num
# }
    
    # headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    # data = requests.get(url_receive,headers=headers)

    # soup = BeautifulSoup(data.text, 'html.parser')

    # # 여기에 코딩을 해서 meta tag를 먼저 가져와보겠습니다.
    # ogtitle = soup.select_one('meta[property="og:title"]')['content']
    # ogdesc = soup.select_one('meta[property="og:description"]')['content']
    # ogimage = soup.select_one('meta[property="og:image"]')['content']

    # db.guestbook.insert_one(doc)
    
    # return jsonify({'msg':'방명록 저장완료!'})



# @app.route("/deletecomment", methods=["POST"])
# def deletecomment_post():

#     delete_receive = request.form["num_give"]
#     # logging.warn("loglog"+ delete_receive)
    
#     db.guestbook.delete_one({'num': int(delete_receive)})
#     return jsonify({'msg':'방명록 삭제완료!'})



# @app.route("/check", methods=["POST"])
# def check_post():

#     pw_receive = request.form["pw_give"]
#     num_receive = request.form["num_give"]

#     print("전달 받은 패스워드 : "+ pw_receive+ "디비 넘버"+ int(num_receive))

#     a = list(db.guestbook.find({'pw':pw_receive, 'num':int(num_receive)},{'_id':False}))
#     b = list(db.guestbook.find({'num':int(num_receive)},{'_id':False}))

#     for i in a:
#         print(i)


#     logging.warn("")


#     for i in b:
#         print(i)

    
#     # db.guestbook.delete_one({'num': int(delete_receive)})
#     return jsonify({'msg':'본인 확인 완료!'})



# @app.route("/guestbook", methods=["GET"])
# def guestbook_get():
#     guestbook = list(db.guestbook.find({},{'_id':False}))
#     return jsonify({'result':guestbook})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
