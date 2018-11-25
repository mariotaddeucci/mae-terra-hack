from flask import Flask, jsonify, request
from database import db_session, Produto, Tag

app = Flask(__name__)
app.config['SECRET_KEY'] = "key"
app.config['DEBUG'] = True


@app.teardown_appcontext
def cleanup(resp_or_exc):
    db_session.remove()


@app.before_request
def mock_data_base():
    db_session.add_all([
        Produto(clarifai_id='Mãe Terra - Mini Tribos Azeite e Ervas', message='Mãe Terra - Mini Tribos Azeite e Ervas esse é o de ervas e a mensagem criada', tags=[
            Tag(tag='SNACK'),
            Tag(tag='Vegetarian Food'),
            Tag(tag='Breakfast Cereal'),
            Tag(tag='Cracker'),
        ]),
        Produto(clarifai_id='Mãe Terra - Mini Tribos Chilli', message='Ed Jo1221nes', tags=[
            Tag(tag='SNACK'),
            Tag(tag='Vegetarian Food'),
            Tag(tag='Breakfast Cereal'),
            Tag(tag='Cracker'),
        ]),
    ])
    db_session.commit()


@app.route('/find')
def find():
    from clarifai.rest import ClarifaiApp
    from os import getenv

    url = request.args['q']

    app = ClarifaiApp(api_key=getenv('CLARIFAI_KEY'))

    model = app.models.get(model_id='produtos')
    response = model.predict_by_url(url=url)
    concept = response['outputs'][0]['data']['concepts']
    concept = concept[0]

    if concept['value'] < 0.4:
        return jsonify({
            "messages": [
                {"text": "Daqui a pouco vou uma alternativa para "},
                {"text": "What are you up to?"}
            ]
        })
    obj = db_session.query(Produto).filter_by(clarifai_id=concept['name']).first()
    resp = {
        "messages":
            {"text": obj.message}
    }
    return jsonify(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
