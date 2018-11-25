from flask import Flask, jsonify, request
from database import db_session, Produto, Tag
from os import getenv

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')


@app.route('/find')
def find():
    from clarifai.rest import ClarifaiApp

    url = request.args['imageUrl']
    app = ClarifaiApp(api_key=getenv('CLARIFAI_KEY'))

    model = app.models.get(model_id='produtos')
    response = model.predict_by_url(url=url)
    concept = response['outputs'][0]['data']['concepts']
    concept = concept[0]

    if concept['value'] < 0.4:
        return jsonify({
            "redirect_to_blocks": ["return"]
        })

    obj = db_session.query(Produto).filter_by(clarifai_id=concept['name']).first()
    resp = {
        "messages": obj.message
    }
    return jsonify(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
