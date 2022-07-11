from flask import Flask, request, jsonify
from pymongo import MongoClient

devmongo = 'mongodb+srv://test:sparta@cluster0.stp4v.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(devmongo)
db = client.ogamemu

app = Flask(__name__)

# hashlib 모듈로 비밀번호 암호화
import hashlib


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
