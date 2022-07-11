from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.2qnmgye.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/game", methods=["POST"])
def game_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    price_receive = request.form['price_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')


    image = soup.select_one('body > app-root > div > app-game-overview > div > div.header-image-container > picture > source:nth-child(2)')['srcset']
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
    game_list =  list(db.games.find({}, {'_id': False}))
    count = len(game_list) +1

    doc = { 'title': title,
            'image':image,
            'maker': maker,
            'star': star_receive,
            'comment': comment_receive,
            'date' : date,
            'platform' : platform,
            'price' : price_receive,
            'num': count
    }
    db.games.insert_one(doc)

    return jsonify({'msg':'작성완료!'})

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