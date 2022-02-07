from flask import Flask, render_template,request,jsonify
import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
app = Flask(__name__)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r', encoding='utf-8') as json_data:
    intents = json.load(json_data)  
FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "TDTU_CHATBOT"

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.5:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])  
    return "Tôi Không Hiểu"

#XU LY API
@app.route("/", methods = ["GET"])
def home():
    return render_template("index.html")

@app.route("/reply", methods=["POST"])
def reply():
    text = request.get_json().get("message")

    res = get_response(text)

    msg = {"response":res}
    return jsonify(msg)

if __name__ =="__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)