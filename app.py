from flask import Flask, request, jsonify, render_template, url_for, redirect
from pymongo import MongoClient

devmongo = 'mongodb+srv://test:sparta@cluster0.stp4v.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(devmongo)
db = client.jwtTest

app = Flask(__name__)

### for JWT
# JWT 토큰을 만들 때 필요한 비밀문자열
SECRET_KEY = 'OGAMEMU'

# JWT 패키지를 사용, PyJWT 패키지 설치
import jwt

# datetime 모듈로 토큰 만료시간 설정
import datetime

# hashlib 모듈로 비밀번호 암호화
import hashlib


#######
# 화면 #
#######
# 홈 화면
@app.route('/')
def home():
    # 쿠키에 저장된 jwt 토큰을 가져온다
    token_receive = request.cookies.get('mytoken')
    try:
        # 서버에 지정된 비밀 문자열로 토큰을 해석한다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 해석된 토큰값에서 id를 가져온다.
        user_info = db.user.find_one({"user_id": payload['user_id']})
        return render_template('index.html', birthday=user_info["user_birthday"])
    # 토큰 시간이 만료되었다면
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    # 비밀 문자열이 틀리거나 하는 이유로 해석에 실패했다면
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


# 로그인 화면
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


# 회원가입 화면
@app.route('/signup')
def register():
    return render_template('signup.html')


#######
# api #
#######
# 로그아웃은 내가 가진 토큰을 쿠키에서 지우기

# 로그인 api
@app.route("/api/login", methods=["POST"])
def api_login():
    id_receive = request.form['user_id']
    pw_receive = request.form['user_pw']

    # 회원가입 때와 같은 방법으로 pw를 암호화
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    # 암호화된 pw를 이용하여 사용자 찾기
    user = db.user.find_one({'user_id': id_receive, 'user_pw': pw_hash}, {'_id': False})
    # 사용자가 존재하면 JWT 토큰을 만들어 발급
    if user is not None:
        # JWT 토큰에 저장될 값으로 아이디와 토큰 만료 시간을 저장
        payload = {
            'user_id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        }
        # 시크릿 키를 사용하여 암호화 한 토큰을 생성
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # token 리턴
        return jsonify({'result': 'success', 'token': token})
    # 사용자가 없다면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# 로그인 api
@app.route("/api/checkid", methods=["POST"])
def api_check_id():
    id_receive = request.form['user_id']
    user = db.user.find_one({'user_id': id_receive}, {'_id': False})

    # 사용자가 존재한다면
    if user is not None:
        return jsonify({'result': 'fail', 'msg': '중복된 아이디 입니다.'})
    else:
        return jsonify({'result': 'success', 'msg': '사용 가능한 아이디 입니다.'})



# 회원가입 api
@app.route('/api/signup', methods=['POST'])
def api_signup():
    id_receive = request.form['user_id']
    pw_receive = request.form['user_pw']
    birthday_receive = request.form['user_birthday']
    # hashlib 함수로 비밀번호 암호화
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'user_id': id_receive, 'user_pw': pw_hash, 'user_birthday': birthday_receive})

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
