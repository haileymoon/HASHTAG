from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
from pytz import timezone
import bcrypt
import jwt
from JWT_info import secret, algorithm, MIN
today = datetime.now(timezone('Asia/Seoul'))


app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbmakingchallenge


#DB속 유저 리스트
users = list(db.user.find({},{'_id':False}))

#유저 jwt 체크 데코레이터
def check(func):
    def check_Token():
        cookie = request.cookies.get('Authorization')
        # cookie = request.headers['Authorization'] client -> server 헤더로 쿠키값을 싫어서 보낸다.
        try:
            print('{}'.format(func.__name__))
            #유저 아이디값 불러와서 인자로 넣어주기!
            user_id = jwt.decode(cookie, secret, algorithm)['user_id']
            return func(user_id)
        except jwt.ExpiredSignatureError:
            return jsonify({'msg':'로그인 시간이 만료되었습니다.'})
        except jwt.exceptions.DecodeError:
            return jsonify({'msg': "로그인 정보가 존재하지 않습니다."})
    check_Token.__name__ = func.__name__
    return check_Token

#메인페이지
@app.route('/')
def mainPage():
    return render_template('Mainlogout.html')


@app.route('/main-page')
@check
def mainPage2(user_id):
    return render_template('Mainlogin.html', name=user_id)

#로그인페이지
@app.route('/login-page')
def login_page():
    return render_template('Login.html')

#회원가입페이지
@app.route('/signup-page')
def signup_Page():
    return render_template('Account.html')

#관심단어 등록 페이지
@app.route('/myword-page')
def mywordPage():
    return render_template('record_list.html')

#로그인버튼
@app.route('/login', methods=['POST'])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    for target in users:
        if id_receive == target['user_id']:
            check_password = target['user_pw'].encode('utf-8')
            if bcrypt.checkpw(pw_receive.encode('utf-8'), check_password):
                payload={
                    'user_id':id_receive,
                    'exp':datetime.utcnow() + timedelta(minutes=MIN)
                    # 'exp': datetime.utcnow() + timedelta(minutes=10)
                }
                # 토큰인코딩
                access_token = jwt.encode(payload, secret, algorithm)
                # 토큰디코딩
                # check_token = jwt.decode(access_token, secret, algorithm)
                # 유저 아이디 값
                return jsonify({'signIn': '1', 'Authorization': access_token})
    return jsonify({'msg': '아이디/비밀번호가 틀립니다'})

#회원가입버튼
@app.route('/signup', methods=['POST'])
def signup():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    # 아이디값 공백 검사
    if id_receive == "":
        return({'msg':'아이디를 입력해주세요'})
    # DB에서 중복 아이디 검사
    elif db.user.find_one({'user_id':id_receive},{'_id':False}):
        return jsonify({'msg':'아이디가 있습니다'})
    # 패스워드값 공백 검사
    elif pw_receive == "":
        return ({'msg': '비밀번호를 입력해주세요'})
    #비밀번호 해싱
    encode_password = bcrypt.hashpw(pw_receive.encode('utf-8'), bcrypt.gensalt())
    #해싱값 str변환 -> DB저장
    hashed_password = encode_password.decode('utf-8')

    user ={
        'user_id':id_receive,
        'user_pw':hashed_password,
    }
    db.user.insert_one(user)
    return jsonify({'signUp': '1'})

#검색어 저장
@app.route('/searchword', methods=['POST'])
def search_post():
    search_word_receive = request.form['searchWord_give']
    doc = {
        'search': search_word_receive
    }
    db.searchword.insert_one(doc)

@app.route('/search', methods=['GET'])
def searchaaa():
    word = list(db.searchword.find({}, {'_id': False}))
    return jsonify({'search_word': word})

#검색어와 메모 저장
@app.route('/result', methods=['POST'])
def saving_memo():
    myword_receive = request.form['myword_give'] #검색한 단어
    num_receive = request.form['num_give'] #아이디값 저장
    memo_receive = request.form['memo_give']
    keyword_receive = request.form['keyword_give']
    link_receive = request.form['link_give']

    doc = {
        'myword': myword_receive,
        'saving-num': num_receive,
        'memo': memo_receive,
        'keyword': keyword_receive,
        'link': link_receive
    }
    db.onedaylive.insert_one(doc)
    return jsonify({'msg' : '검색어가 저장되었습니다.'}) #검색어 보여주기


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)