from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

devmongo = 'mongodb+srv://test:sparta@cluster0.stp4v.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(devmongo)
db = client.ogamemu

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/api/login", methods=["POST"])
def login():
    id_receive = request.form['user_id']
    pw_receive = request.form['user_pw']

    user = db.user.find_one({'user_id': id_receive, 'user_pw': pw_receive}, {'_id': False})

    if user is None:
        return jsonify({'msg': '유저 존재하지 않음'})

    return jsonify({'user': user})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
