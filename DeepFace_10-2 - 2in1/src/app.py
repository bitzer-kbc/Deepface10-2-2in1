# ※事前準備※　
# ターミナルより、以下のパッケージをインストール
#
# ・顔検出のパッケージ: mtcnn（MITライセンス）
# ・顔の属性を推定するパッケージ: deepface（MITライセンス）
#     conda install mtcnn ()
#     conda install deepface
#     conda install -c conda-forge opencv
#     conda install pillow

#   Anaconda の環境ではcpmmand prompt 上で以上のコマンドを実行してください。
#　　（他の仮想環境では実施していません）
#　　
#     pip install mtcnn
#     pip install deepface
#     pip install -c conda-forge opencv
#     pip install pillow
#
###################################################
# 必要なモジュールのインポート
# import torch
# from animal import transform, Net # animal.py から前処理とネットワークの定義を読み込み
###################################################################################
from deepface_1 import detect_faces, analyze_face, main, comment ## deepface_1 より

from flask import Flask, request, render_template, redirect, url_for
#from werkzeug.utils import secure.filename #とりあえず追加
import os
import io
from PIL import Image
import base64


# Flask のインスタンスを作成
app = Flask(__name__)

# アップロードされる拡張子の制限
UPLOAD_FOLDER = './uploads' # 0802 追加
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'jpeg'])

# ディレクトリがなければ作成
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #0802 追加

#　拡張子が適切かどうかをチェック
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

############################################################
#  ### URL にアクセスがあった場合の挙動の設定 ###
############################################################
# ルートディレクトリにアクセスがあった場合に、
# 下に書かれている def から始まる関数の中の処理を実行します
#
########## 0803 追加　########################################
age = ""  # POSTリクエストがない場合でも空の値を設定
gender = ""  # POSTリクエストがない場合でも空の値を設定
emotion = ""  # POSTリクエストがない場合でも空の値を設定
output_comment = ""  # POSTリクエストがない場合でも空の値を設定
base64_img = ""  # POSTリクエストがない場合でも空の値を設定
#############################################################

@app.route('/', methods = ['GET', 'POST'])
def predicts():
    # グローバル変数を使うために追加（不要かも）
    global age, gender, emotion, output_comment, base64_img
    # リクエストがポストかどうかの判別
    if request.method == 'POST': # 画像がアップロードされてボタンが押された場合
        # ファイルがなかった場合の処理
        if 'file' not in request.files:
            return redirect(request.url)
        # データの取り出し
        file = request.files['file'] ##修正 filename -> file 0802
        # ファイルのチェック
        if file and allowed_file(file.filename):

###############################################################################
            #　画像ファイルに対する処理
            #　画像書き込み用バッファを確保
            ##buf = io.BytesIO() ##0802
            ##image = Image.open(file).convert('RGB') ##0802
            #　画像データをバッファに書き込む
            ##image.save(buf, 'png') ##0802
##############################################################################
#            filename = secure_filename(file.filename)
#            filename = file.filename # 0802追加
#            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#            return redirect(url_for('uploaded_file', filename=filename))
############# 0802 上記の4行を以下の通り 再度、修正する 0802 ####################
# 画像の保存
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            # 画像の読み込み
            image = Image.open(file_path).convert('RGB')
            image_up = image ################################# 仮0804 -> 不要
#
########################
            #　バイナリデータを base64 でエンコードして utf-8 でデコード
            ##base64_str = base64.b64encode(buf.getvalue()).decode('utf-8') ##0802
            #　HTML 側の src  の記述に合わせるために付帯情報付与する
            ##base64_data = 'data:image/png;base64,{}'.format(base64_str) ##0802
########################
# 画像データをバイト列に変換し、そのバイト列をbase64でエンコードしてからデコードする
        #    buffered = io.BytesIO()
        #    image.save(buffered, format="PNG")
        #    img_str = base64.b64encode(buffered.getvalue())
        #    base64_data = "data:image/png;base64," + img_str.decode('utf-8')
########################
# image をbase64に変換(0803 修正)
            buf = io.BytesIO()            
            ################################################################
            # 以下の "base64_data" の形式でないと、ブラウザで表示できないみたい
            # result.html に送る画像(base64_data)を用意する 
            ################################################################
            buf_up = io.BytesIO()
            image_up = Image.open(file).convert('RGB')
            #　画像データをバッファに書き込む
            image.save(buf_up, 'png')
            #　バイナリデータを base64 でエンコードして utf-8 でデコード
            # （画像データを直接 HTML に埋め込むため）
            base64_str = base64.b64encode(buf_up.getvalue()).decode('utf-8')
            #　HTML 側の src の記述に合わせるために付帯情報付与する
            base64_data = 'data:image_up/png;base64,{}'.format(base64_str)
            # buf_up.close() # とりあえず、コメントアウトしておく
            ##################################################################
            # 
            image.save(buf, format='PNG')
            image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()             

###############################################
##  入力された画像に対してコメント文書を生成     ##
###############################################
            result_ = main(image)
            emotion = result_[0]
            age = result_[1]
            gender = result_[2]
#            face_locations = detect_faces(image)
#            result = analyze_face(image, face_locations)
            global_emotion = emotion
            output_comment = comment(global_emotion)

            ############# 確認のため、以下のコードを挿入 #################
            #print(global_emotion)  
            #print(emotion)
            #print(output_comment)  
            ############# 確認　ここまで　###############################
###########                      
            return render_template('result.html', age=age, gender=gender, emotion=emotion, 
                                   output_comment=output_comment, image_base64=base64_data) 
###########
        return redirect(request.url)
##  result.htm に結果を送る・・・
#################################################################################

    # GET メソッドの定義
    elif request.method == 'GET':
        return render_template('index.html')
    return render_template('result.html', age=age, gender=gender,
                           emotion=emotion, output_comment=output_comment, 
                           image_base64=base64_data)

# アプリケーションの実行の定義
if __name__ == '__main__':
    app.run(debug=True)
