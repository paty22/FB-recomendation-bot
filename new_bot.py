from flask import Flask, request
import requests
import xlrd
import pandas as pd
import nltk

app = Flask(__name__)

ACCESS_TOKEN = "EAACHgzqJfXkBAJZBasmC3St3iWBz6my5WAjNeYoj9aTC6pV06OP1P8eITlFmBOhWzsZAbwQZAnKNcNepTOH20P7kr84rIk8pp1RZAeuhXZAQlcS8KdKDmQ3Y1BfWH1JrXu5qFdUlY3DJNKnK0ZAck2wjep3EEpwJOtYp7aVhFdx9gfBGPG5PnW"
VERIFY_TOKEN = "testbot_verify_token"
PAGE_ID ="159992937960089"

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


@app.route('/', methods=['GET'])
def handle_verification():
    if request.args['hub.verify_token'] == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return "Invalid verification token"
@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    output = ml_train(message)
    reply(sender, output)
    return "ok"

def ml_train(message):
    ml_array =[]
    nltk.download('punkt')
    df=pd.read_csv('witty.csv')
    df.replace('?',-9999,inplace=True)
    b_word = message
    b_word.lower()
    word_list = b_word.split(' ')
    print(word_list)
    n =  len(word_list)
    output_link=''
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    filtered_sentence = [w for w in word_list if not w in stop_words]
    print(filtered_sentence)
    workbook = xlrd.open_workbook('witty.xls')
    worksheet = workbook.sheet_by_name('witty')
    df.drop(['status_id'],1,inplace=True)
    for i in range (0, 2200):
        title_string = worksheet.cell(i, 2).value
        title_string = title_string.lower()
        for j in range (0, n):
            if word_list[j] in title_string:
                output_link = worksheet.cell(i, 5).value
                return output_link
                break

if __name__ == '__main__':
    app.run(debug=True)