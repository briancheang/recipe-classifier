import pickle
import flask
from flask import Flask, request, render_template, jsonify


model = pickle.load(open("LogReg_v5.sav","rb"))
vectorizer = pickle.load(open("vectorizer.sav","rb"))

dic_arr = []
# with open('features.txt') as feature_file:
#     for line in feature_file:
#         dic_arr.append(line.rstrip())

app = flask.Flask(__name__)

prediction = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
prediction2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
ingredients = set([])
dictionary = set(vectorizer.get_feature_names());
data = "";
valid = "false";
exists = "false";

@app.route('/', methods=['GET'])
def home():
    return render_template('mainpage.html', prediction=prediction, prediction2=prediction2, valid=valid, data=data, exists=exists)

@app.route('/update', methods=['POST', 'DELETE'])
def update():
    global valid
    global exists
    global ingredients
    data = request.form.get('ingredient').lower().strip()
    if data in ingredients:
        exists = "true"
    else:
        exists = "false"
    if request.method == 'POST':
        if data in dictionary:
            ingredients.add(data)
            valid = "true"
        else:
            valid = "false"
    else:
        if data in ingredients:
            ingredients.remove(data)
            valid = "false"
    if(len(ingredients) == 0):
        prediction = ["0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1"]
    else:
        prediction = model.predict_proba([' '.join(ingredients)]).tolist()
        prediction = [rearrange_predict(prediction[0])]

    map = {
            'prediction': prediction,
            'data': data,
            'valid': valid,
            'exists': exists,
        }
    return (jsonify(map));

@app.route('/update2', methods=['POST'])
def update2():
    data = request.form.get('recipe').lower().strip()
    defined = get_recipe_features(data)
    if(len(defined) == 0):
        prediction2 = ["0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1"]
    else:
        prediction2 = model.predict_proba([data]).tolist()
        prediction2 = [rearrange_predict(prediction2[0])]
    map = {
        'prediction2': prediction2,
        'defined': defined
    }
    return jsonify(map)

@app.route('/reset', methods=['DELETE'])
def reset():
    global ingredients
    prediction = ["0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1"]
    ingredients = set([])
    prediction = [prediction]
    map = {
            'prediction': prediction,
        }
    return jsonify(map)

def get_recipe_features(data):
    words = data.split(" ");
    defined = []
    for word in words:
        if word in dictionary:
            defined.append(word);
    return defined

def rearrange_predict(data):
    new_predict = []
    new_predict.append(data[1])
    new_predict.append(data[8])
    new_predict.append(data[15])
    new_predict.append(data[16])
    new_predict.append(data[5])
    new_predict.append(data[6])
    new_predict.append(data[9])
    new_predict.append(data[17])
    new_predict.append(data[7])
    new_predict.append(data[14])
    new_predict.append(data[0])
    new_predict.append(data[2])
    new_predict.append(data[4])
    new_predict.append(data[10])
    new_predict.append(data[13])
    new_predict.append(data[3])
    new_predict.append(data[11])
    new_predict.append(data[12])
    new_predict.append(data[18])
    new_predict.append(data[19])
    return new_predict


if __name__ == '__main__':
    app.run()
