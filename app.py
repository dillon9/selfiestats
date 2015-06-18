import json
import os
from flask import Flask, redirect, url_for, render_template, request
from werkzeug import secure_filename
import indicoio


app = Flask(__name__)
ALLOWED_EXTENSIONS = set(["png","jpg","jpeg"])
app.config["UPLOAD_FOLDER"] = "pictures/"

foo = ""

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit(".",1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
  global foo
  if request.method == 'POST':
      file = request.files['file']
      if file and allowed_file(file.filename):
          filename = secure_filename(file.filename)
          foo = request.form['name']
          path = os.path.dirname(os.path.abspath(__file__)) + "/pictures/" + foo
          if not os.path.exists(path):          
              os.makedirs(path)
          app.config["UPLOAD_FOLDER"] = path
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  else:
      return render_template("upload.html")
  return render_template("index.html")

@app.route('/crunch', methods=['POST'])
def send_to_indico():

  global foo
  path = os.path.dirname(os.path.abspath(__file__)) + "/pictures/" + foo
  emotion_list = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
  c = 0
  for x in emotion_list:
      x = x.split(".")[1]
      if x == "db":
          del emotion_list[c]
      c+=1


  #angry,sad,happy,afraid,neutral,surprise = 0,0,0,0,0,0
  emotion = []
  n = 0

  for i in emotion_list:
    emotion_list[n] = path + "/" + emotion_list[n]
    n += 1 

  print emotion_list
  emotion_scores = indicoio.batch_fer(emotion_list, api_key="0f73d0a7c698469192cbd74886b48615")
  for i in emotion_scores:
      emotion.append(i["Happy"])
  #    angry += i["Angry"]
  #    sad += i["Sad"]
  #    afraid += i["Fear"]
  #    happy += i["Happy"]
  #    neutral += i["Neutral"]
  #    surprise += i["Surprise"]
  #    n += 1
  
  print emotion
  return json.dumps({'scores': emotion, 'tweets': emotion_list})


   #tweets_csv_string = request.form.get('tweets')
   #csv_list = tweets_csv_string.replace('\r', '').splitlines()

   #if len(csv_list) > 40:
   #    csv_list = csv_list[:40]

   #tweet_list = []
   #for csv_tweet in csv_list:
   #    tweet_only = csv_tweet.split(',')[2:]
   #    tweet_list.append(','.join(tweet_only))

   #tweet_list = tweet_list[::-1]
   #tweet_scores = indicoio.batch_sentiment(tweet_list, api_key="0f73d0a7c698469192cbd74886b48615")
   #return json.dumps({'scores': tweet_scores, 'tweets': tweet_list})  # dumps converts res to a JSON object



if __name__ == '__main__':
    app.run(debug=True)