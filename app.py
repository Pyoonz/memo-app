#from flask import Flask
 #Flask　ライブラリから　Flask を読み込みしている
#app = Flask(__name__)
 #Flask アプリのインスタンス（実体）を作成。　
 #__name__　は今実行されているファイルの名前が入る
#@app.route("/")
 #デコレータ
 #今ある関数に追加の機能を付け加えたい時に使う
#def hello():
 #/ にアクセスした時に使う関数
#    return "Hello, World!"
 #ブラウザに返すレスポンスの内容。関数名の名前は自由
#if __name__ == "__main__":
 #このファイルが直接実行されたときだけ以下の処理を行う
 #pythonでよく使われる
#    app.run(debug=True)
 #Flaskのサーバーを起動する
 #debug = True　のメリット　・コードを変更すると自動でサーバーが起動する。
 #                   ・　えらーが起きたときブラウザに詳しいエラー情報が表示される

from flask import Flask, jsonify, request, send_from_directory
from database import init_db, get_all_memos,get_memo,create_memo,update_memo,delete_memo
#from collections import OrderedDict

app = Flask(__name__)
#app.json.ensure_ascii = False

#アプリ起動時にDBを初期化
init_db()

@app.route("/")
def index():
    """HTMLページを配信する"""
    return send_from_directory("static", "index.html")



@app.route("/api/memos", methods=["GET"])
def api_get_memos():
    """全てのメモを取得する"""
    memos = get_all_memos()
    #ordered_memos_for_json = []
    #for memo_item in memos:
        #ordered_memo_item = OrderedDict([
            #("id", memo_item["id"]),
            #("title", memo_item["title"]),
            #("body", memo_item["body"]),
            #("created_at", memo_item["created_at"]),
            #("updated_at", memo_item["updated_at"])
        #])
        #ordered_memos_for_json.append(ordered_memo_item)

    #return jsonify(ordered_memos_for_json)
    return jsonify(memos)


@app.route("/api/memos", methods=["POST"])
def api_create_memo():
    """新しいメモを作成!"""
    data = request.get_json()

    #バリデーション（入力チェック）
    if not data:
        return jsonify({"error":"リクエストボディが空です"}),400

    title = data.get("title")
    body = data.get("body")

    if not title or not body:
        return jsonify({"error": "　title　と　body　は必須です"}),400

    memo_id = create_memo(title, body)
    memo = get_memo(memo_id)
    return jsonify(memo), 201

@app.route("/api/memos/<int:id>", methods=["GET"])
def api_get_memo(id):
    """指定されたIDのメモを取得する"""
    memo = get_memo(id)
    
    if not memo:
        return jsonify({"error": "メモが見つかりません"}),404
    
    return jsonify(memo)


@app.route("/api/memos/<int:id>", methods=["PUT"])
def api_update_memo(id):
    """指定されたIDのメモを更新する"""
    #更新対象が存在するか確認
    memo = get_memo(id)
    if not memo:
        return jsonify({"error": "メモが見つかりません"}), 404
    
    data = request.get_json()

    if not data:
        return jsonify({"error": "リクエストボディが空です"}), 400

    title = data.get("title")
    body = data.get("body")

    if not title or not body:
        return jsonify({"error": "title と body は必須です"}), 400
    
    #メモを更新
    update_memo(id, title, body)
    #更新後のメモを返す
    updated_memo = get_memo(id)
    return jsonify(updated_memo)


@app.route("/api/memos/<int:id>", methods=["DELETE"])
def api_delete_memo(id):
    """指定されたIDのメモを削除する"""
    memo = get_memo(id)
    if not memo:
        return jsonify({"error": "メモが見つかりません"}), 404
    
    delete_memo(id)
    return jsonify({"message": f"メモ (ID:{id}) を削除しました"})


if __name__ == "__main__":
    app.run(debug=True, port = 5000)
    

