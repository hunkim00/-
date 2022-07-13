from flask import Flask, request, jsonify, render_template, url_for, redirect
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import jwt
import datetime
import hashlib

client = MongoClient('mongodb+srv://test:sparta@cluster0.2qnmgye.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

# JWT 토큰을 만들 때 필요한 비밀문자열
SECRET_KEY = 'OGAMEMU'


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
        user_info = db.user.find_one({"user_id": payload['user_id']}, {'_id': False, 'user_pw': False})
        return render_template('index.html', user_info=user_info)
    # 토큰 시간이 만료되었다면
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    # 비밀 문자열이 틀리거나 하는 이유로 해석에 실패했다면
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


# 로그인 화면이앙
@app.route('/login')
def login():
    return render_template('login.html')


# 회원가입 화면
@app.route('/signup')
def register():
    return render_template('signup.html')


@app.route('/reviewpage')
def review():
    return render_template('reviewpage.html')


# 마이페이지 화면
@app.route('/mypage/<user_id>')
def mypage(user_id):
    # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (user_id == payload["user_id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False

        user_info = db.user.find_one({'user_id': user_id}, {'_id': False, 'user_pw': False})
        return render_template('mypage.html', user_info=user_info, status=status)
    # 토큰 시간이 만료되었거나 해석에 실패했다면
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        }
        # 시크릿 키를 사용하여 암호화 한 토큰을 생성
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # token 리턴
        return jsonify({'result': 'success', 'token': token})
    # 사용자가 없다면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# 아이디 중복 확인 api
@app.route("/api/checkid", methods=["POST"])
def api_check_id():
    id_receive = request.form['user_id']
    exist = bool(db.user.find_one({'user_id': id_receive}, {'_id': False}))

    # 사용자가 존재한다면
    if exist:
        return jsonify({'result': 'fail', 'msg': '중복된 아이디 입니다.'})
    else:
        return jsonify({'result': 'success', 'msg': '사용 가능한 아이디 입니다.'})


# 회원가입 api
@app.route('/api/signup', methods=['POST'])
def api_signup():
    id_receive = request.form['user_id']
    pw_receive = request.form['user_pw']
    name_receive = request.form['user_name']
    birthday_receive = request.form['user_birthday']
    # hashlib 함수로 비밀번호 암호화
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({
        'user_id': id_receive,
        'user_pw': pw_hash,
        'user_name': name_receive,
        'user_comment': '',
        'user_birthday': birthday_receive
    })

    return jsonify({'result': 'success'})


# 회원 수정 api
@app.route('/api/update_user', methods=['POST'])
def api_update_user():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_id = payload["user_id"]
        name_receive = request.form["name_give"]
        comment_receive = request.form["comment_give"]
        doc = {
            'user_name': name_receive,
            'user_comment': comment_receive
        }
        db.user.update_one({'user_id': user_id}, {'$set': doc})
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


# 나의 리뷰 불러오기 api
@app.route('/api/my-reviews/<user_id>', methods=['GET'])
def api_my_reviews(user_id):
    reviews = list(db.games.find({'user_id': user_id}, {'_id': False}))
    print(reviews)
    return jsonify({'result': 'success', 'reviews': reviews})


@app.route("/game", methods=["POST"])
def game_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    # 가격 입력 삭제
    # price_receive = request.form['price_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    image = soup.select_one(
        'body > app-root > div > app-game-overview > div > div.header-image-container > picture > source:nth-child(2)')[
        'srcset']
    title = soup.select_one(
        'body > app-root > div > app-game-overview > app-page-container-right-nav > div > div.d-flex.mb-4 > div.flex-grow-1 > div.card.mt-4 > div > h1').text.strip()
    maker = soup.select_one(
        'body > app-root > div > app-game-overview > app-page-container-right-nav > div > div.d-flex.mb-4 > div.flex-grow-1 > div.card.mt-4 > div > div > div.col-lg-7 > div.companies > span').text.strip()
    date = soup.select_one(
        'body > app-root > div > app-game-overview > app-page-container-right-nav > div > div.d-flex.mb-4 > div.flex-grow-1 > div.card.mt-4 > div > div > div.col-lg-7 > div.platforms').text[
           0:13].strip()
    platform = soup.select_one(
        'body > app-root > div > app-game-overview > app-page-container-right-nav > div > div.d-flex.mb-4 > div.flex-grow-1 > div.card.mt-4 > div > div > div.col-lg-7 > div.platforms').text[
               14:1000].strip()
    critic = soup.select_one(
        'body > app-root > div > app-game-overview > app-page-container-right-nav > div > div.d-flex.mb-4 > div.flex-grow-1 > div.card.mt-4 > div > div > div.col-lg-7 > div.mt-4 > app-game-scores-display > div > div > div:nth-child(2) > app-score-orb > div > div.inner-orb').text.strip()

    num_list = list(db.nums.find({}, {'_id': False}))
    count = len(num_list) + 1
    doc_num = {
        'num': count
    }
    db.nums.insert_one(doc_num)

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_id = payload["user_id"]

        doc = {'title': title,
               'image': image,
               'maker': maker,
               'star': star_receive,
               'comment': comment_receive,
               'date': date,
               'platform': platform,
               # 삭제 기존 price 정보에 평가점수가 입력됨.
               # 'price': price_receive,
               'price': critic,
               'num': count,
               'url': url_receive,
               'user_id': user_id
               }
        db.games.insert_one(doc)

        return jsonify({'msg': '작성완료!'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return jsonify({'msg': '로그인 하지 않은 사용자는 리뷰를 작성할 수 없습니다.'})


@app.route("/game", methods=["GET"])
def game_get():
    games_list = list(db.games.find({}, {'_id': False}))
    return jsonify({'list': games_list})


# @app.route("/game/change", methods=["POST"])
# def game_change():
#     comment_receive = request.form['comment_give']
#     star_receive = request.form['star_give']
#     num_receive = request.form['num_give']
#     db.games.update_one({'name':  num_receive}, {'$set': {'comment': comment_receive}})
#     db.games.update_one({'name':  num_receive}, {'$set': {'star': star_receive}})
#     return jsonify({'msg': '변경완료'})

@app.route("/game/delete", methods=["POST"])
def game_change():
    num_receive = request.form['num_give']
    db.games.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
