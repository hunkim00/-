from flask import Flask, request, jsonify, render_template, url_for, redirect
from pymongo import MongoClient

devmongo = 'mongodb+srv://test:sparta@cluster0.stp4v.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(devmongo)
db = client.ogamemu

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


@app.route('/')
def home():
    # 쿠키에 저장된 jwt 토큰을 가져온다
    token_receive = request.cookies.get('mytoken')
    try:
        # 서버에 지정된 비밀 문자열로 토큰을 해석한다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 해석된 토큰값에서 id를 가져온다.
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('index.html', nickname=user_info["nick"])
    # 토큰 시간이 만료되었다면
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    # 비밀 문자열이 틀리거나 하는 이유로 해석에 실패했다면
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


# 회원 로그인 / 가입 / 탈퇴
# 로그아웃은 내가 가진 토큰을 쿠키에서 지우기

# 로그인 api
@app.route("/api/login", methods=["POST"])
def login():
    id_receive = request.form['user_id']
    pw_receive = request.form['user_pw']

    user = db.user.find_one({'user_id': id_receive, 'user_pw': pw_receive}, {'_id': False})

    if user is None:
        return jsonify({'msg': '유저 존재하지 않음'})

    return jsonify({'user': user})


# 회원가입 api
@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['user_id']
    pw_receive = request.form['user_pw']
    birthday_receive = request.form['user_birthday']
    # hashlib 함수로 비밀번호 암호화
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'user_id': id_receive, 'user_pw': pw_hash, 'user_birthday': birthday_receive})

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
