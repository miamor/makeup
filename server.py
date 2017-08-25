from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_jwt_extended import get_jti
from sqlalchemy.orm import relationship, backref, validates
import jwt
import uuid
import datetime
from datetime import timedelta, datetime, date
import time
from functools import wraps

import os
from demos.classifier import infer

fileDir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hellokitty'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/makeup'

db = SQLAlchemy(app)

"""
class User(db.Model):
    __tablename__ = 'User'
    ID = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(80))
    phone = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(80))
    sex = db.Column(db.String(20))
    birthday = db.Column(db.String(20))
    group = db.Column(db.String(20), db.ForeignKey('GroupUser.ID'))
    trips = db.relationship("Trip", cascade="save-update, merge, delete")
"""


@app.errorhandler(404)
def error404(error):
    return jsonify({'message': 'Page not found!!!'}), 404

# detect face shape
@app.route('/detect_face_shape/<image_name>/', methods=['GET'])
def detect_face_shape(image_name):
    image_path = './data/upload/%s.jpg' % image_name
    results = infer(image_path)
    #print results
    return jsonify({'status': results[0], 'predict': results[1], 'confidence': results[2]})


# LOGIN
@app.route('/login')
def login_taxi():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    taxi = Taxi.query.filter_by(username=auth.username).first()
#    import pdb; pdb.set_trace()
    if not taxi:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if taxi.dayTo.day == 9 and taxi.dayTo.month == 9 and taxi.dayTo.year == 1990:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if taxi.status == False:
        a = time.strftime("%Y/%m/%d")
        a = datetime.strptime(a, "%Y/%m/%d")
        b = str(taxi.dayTo.year)+"/"+str(taxi.dayTo.month)+"/"+str(taxi.dayTo.day)
        b = datetime.strptime(b, "%Y/%m/%d")
        delta = a - b
        if int(delta.days) >=0:
            taxi.status = True
            taxi.dayTo = '2000/10/10'
            db.session.commit()
        else:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(taxi.password, auth.password):
        uid = str(uuid.uuid4())
        token = jwt.encode({'ID': taxi.ID, 'exp': datetime.utcnow() + timedelta(minutes=120), 'jti': uid}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


if __name__ == '__main__':
    app.run(debug=True)
