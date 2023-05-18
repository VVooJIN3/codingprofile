from flask import Flask, render_template, request, jsonify
from datetime import datetime,timedelta
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

from bson import ObjectId

client = MongoClient('mongodb+srv://sparta:test@cluster0.mctqe10.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/choi')
def choi():
    return render_template('choi.html')

@app.route('/woojin')
def woojin():
    return render_template('woojin.html')

@app.route('/subin')
def subin():
    return render_template('subin.html')

@app.route('/kyeongwon')
def kyeongwon():
    return render_template('kyeongwon.html')

@app.route('/happiipark')
def happy():
    return render_template('happy.html')


@app.route("/guestbook", methods=["POST"])
def savecomment_post():

    count = list(db.guestbook.find({}, {'_id':False})) #db 데이터 수를 카운트
    num = len(count) + 1  # 카운트 한 수에 1을 더해서 새로운 데이터에 숫자 넣어주기

    # 화면에서 넘어 오는 값
    id_receive = request.form['id_give']
    pw_receive = request.form['password_give']
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    doc = {
    'id':id_receive,
    'pw':pw_receive,
    'name':name_receive,
    'comment':comment_receive,
    'num' : num
}
    db.guestbook.insert_one(doc)
    
    return jsonify({'msg':'방명록 저장완료!'})



@app.route("/deletecomment", methods=["POST"])
def deletecomment_post():

    delete_receive = request.form["num_give"]
    # logging.warn("loglog"+ delete_receive)
    
    db.guestbook.delete_one({'num': int(delete_receive)})
    return jsonify({'msg':'방명록 삭제완료!'})


@app.route("/guestbook", methods=["GET"])
def guestbook_get():
    guestbook = list(db.guestbook.find({},{'_id':False}))
    return jsonify({'result':guestbook})


###### 우진님 기능 

#방명록 불러오기 
@app.route('/guestbook1',methods=['GET'])
def guestbook_get1():
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


#방명록 삭제하기
@app.route('/guestbook/2',methods=["GET","POST"])
def guestbook_delete():
    #방명록 삭제기능
   return render_template('woojin.html')



#방명록 수정하기
@app.route('/guestbook/3',methods=["POST","PUT"])
def guestbook_update():
    if request.method == "POST": #수정할 방명록을 페이지에서 가져오기
        objectId_receive = request.form['objectId_give'] #db _id값
        targetpassword_receive = request.form['targetpassword_give']

        target = db.guestbook.find_one({'_id':ObjectId(objectId_receive)}) #댓글 테이블에 아이디와 댓글이 있는지 확인
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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
    ##### 맥 사용자 port=5001, window 사용자 port=5000 ####
