####################################################
#       顔の属性を推定したい画像を読み込み表示        #
####################################################
from PIL import Image

####################################################
#            顔画像の検出と感情分析                  #
####################################################
## 
import cv2 # OpenCV ライブラリ
import numpy as np
import random
from mtcnn.mtcnn import MTCNN # MTCNN（Multi-task Cascaded Convolutional Networks）を使用して顔検出を行います
from deepface import DeepFace # DeepFaceライブラリを使用して顔の属性分析を行います
# from google.colab import files # ファイルのアップロードに使用します
####from IPython.display import Image #  画像の表示に使用します
from PIL import Image #0802 追加
## global_emotion = ''

def detect_faces(image):
    detector = MTCNN() # MTCNNオブジェクトを作成し、
    #detect_facesメソッドを使用して顔の位置情報を取得します
    # 顔の位置情報はリスト形式で返されます
    face_locations = detector.detect_faces(image)
    print(face_locations)
    return face_locations

# 画像と顔の位置情報を受け取り、指定された顔領域を切り取って個々の顔の属性を分析します
# 顔の位置情報から顔領域を切り取り、DeepFace.analyzeメソッドを使用して顔の属性を分析します
# 分析結果は辞書形式で返されます。

# 'analyze_face(image, face_location)'は、
#  画像と顔の位置情報（face_location）を引数として受け取ります
# x, y, w, hには、face_locationから顔の位置情報を取り出してそれぞれ代入しています
# ここでは、xとyは矩形の左上隅の座標、wは矩形の幅、hは矩形の高さを表します
def analyze_face(image, face_location):
    x, y, w, h = face_location['box']
    ###############################################
    #detected_face = image[y:y+h, x:x+w] # 0802 コメントアウト
    #result = DeepFace.analyze(detected_face, actions=['age', 'gender', 'emotion'],\ 
    #                          enforce_detection=False) # 0802 コメントアウト
    # 
    detected_face = Image.fromarray(image[y:y+h, x:x+w]) #0802 以下の3行を追加
    detected_face = np.array(detected_face.convert('RGB'))
    result = DeepFace.analyze(detected_face, actions=['age', 'gender', 'emotion'],\
                              enforce_detection=False)
    ###############################################
#    print(type(result))
#    print(result)
    return result

# main関数
# 与えられた画像のパスを引数として受け取ります
# 画像を読み込み、顔を検出します
# 検出された顔の数と位置情報を表示します
# 各顔に対して、analyze_face関数を呼び出して属性を分析し、結果(辞書型)を表示します

def main(image):
#    image = cv2.imread(image) #0802 コメントアウト
#    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #0802 コメントアウト
    image = np.array(image) #0802 追加
    face_locations = detect_faces(image)
# 画像の中にFaceが有るか？いくつ有るか？
    print("Found {} face(s) in the image.".format(len(face_locations)))
    print()

    for index, face_location in enumerate(face_locations):
        print("\nFace {}: {}".format(index+1, face_location['box']))
        results = analyze_face(image, face_location)

        for result in results:
          age = result['age']
#         gender = result['gender'] # Man, Woman を確率で表示する場合
#         dominant とすると、確率的な表現でなくなる
          gender = result['dominant_gender']
          emotion = result['dominant_emotion']
#         print('\n') # 改行
#         print(emotion) # emotion のみprint
          print("\n Age: {}".format(age))
          print(" Gender: {}".format(gender))
          print(" Emotion: {}".format(emotion))
          return(emotion, age, gender) # 追加(emotion のみを返す)

## IPython.display.Imageを使用して、input_pathで指定された画像を表示します
# display(Image(input_path)) # 画像を表示しない場合はコメントアウト
# main(input_path)
#main(input_path)

#####################################################
# コメントの例文集
# 出力するコメントは、以下より編集します
#####################################################
#
def comment(global_emotion):
## happy
  if global_emotion == 'happy':
    random_no = random.randint(1, 3)
    if random_no == 1:
      # コメントをコメント変数に格納する
      output_comment = 'いい笑顔！良いことあった？'
      print(output_comment) # 文例をランダムに発生させたい？➡ChatGPT

    elif random_no == 2:
      # コメントをコメント変数に格納する
      output_comment = '今日は良いこと有りそう？'
      print(output_comment)
    elif random_no == 3:
      # コメントをコメント変数に格納する
      output_comment = '素敵な笑顔！'
      print(output_comment)

## angery
  elif global_emotion == 'angry':
    random_no = random.randint(1,3)
    if random_no == 1:
      # コメントをコメント変数に格納する
      output_comment = 'ここは、少し落ち着いて'
      print(output_comment)
    elif random_no == 2:
      # コメントをコメント変数に格納する
      output_comment = '穏便にね'
      print(output_comment)
    elif random_no == 3:
      # コメントをコメント変数に格納する
      output_comment = 'おちついて！'
      print(output_comment)

## sad
  elif global_emotion == 'sad':
    random_no = random.randint(1,3)
    if random_no == 1:
      # コメントをコメント変数に格納する
      output_comment = 'Never Mind!'
      print(output_comment)
    elif random_no == 2:
      # コメントをコメント変数に格納する
      output_comment = '明日は明日の風が吹く'
      print(output_comment)
    elif random_no == 3:
      # コメントをコメント変数に格納する
      output_comment = '元気だしなよ'
      print(output_comment)

    elif global_emotion == 'neutral':
      # コメントをコメント変数に格納する
      output_comment = 'なにか良いこと有る? Good & New?  '
      print(output_comment)

## surprise
  elif global_emotion == 'surprise':
    random_no = random.randint(1,3)
    if random_no == 1:
      # コメントをコメント変数に格納する
      output_comment = 'ああ、びっくりした'
      print(output_comment)
    elif random_no == 2:
      # コメントをコメント変数に格納する
      output_comment = 'おどろいた！！！'
      print(output_comment)
    elif random_no == 3:
      # コメントをコメント変数に格納する
      output_comment = '！びっくり！'
      print(output_comment)

## fear
  elif global_emotion == 'fear':
    random_no = random.randint(1,3)
    if random_no == 1:
      # コメントをコメント変数に格納する
      output_comment = '怖い！'
      print(output_comment)
    elif random_no == 2:
      # コメントをコメント変数に格納する
      output_comment = 'ちょっと怖いかも…'
      print(output_comment)
    elif random_no == 3:
      # コメントをコメント変数に格納する
      output_comment = '！びっくり！'
      print(output_comment)

## disgust
  elif global_emotion == 'disgust':
    random_no = random.randint(1,3)
    if random_no == 1:
      # コメントをコメント変数に格納する
      output_comment = 'ここは、少し落ち着いて'
      print(output_comment)
    elif random_no == 2:
      # コメントをコメント変数に格納する
      output_comment = '穏便にね'
      print(output_comment)
    elif random_no == 3:
      # コメントをコメント変数に格納する
      output_comment = 'おちついて！'
      print(output_comment)


## neutral
  elif global_emotion == 'neutral':
    random_no = random.randint(1,3)
    if random_no == 1:
      # コメントをコメント変数に格納する
      output_comment = '今日の気分は！'
      print(output_comment)
    elif random_no == 2:
      # コメントをコメント変数に格納する
      output_comment = '表情硬いよ！笑って…'
      print(output_comment)
    elif random_no == 3:
      # コメントをコメント変数に格納する
      output_comment = '！今日も一日元気で行こう！'
      print(output_comment)

  return(output_comment)