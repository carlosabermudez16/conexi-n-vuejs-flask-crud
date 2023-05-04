from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)

Cors = CORS(app)
CORS(app, resources = {r'/api/*': {'origins': 'http://localhost:8080',
                                   "allow_headers":"Access-Control-Allow-Origin"}}, 
     CORS_SUPPORTS_CREDENTIALS = True)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SQLALCHEMY_DATABASE_URI']= f'mysql+mysqlconnector://admin:123456@localhost:3306/integrationdb_flask_vue_crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
print ('conexión establecida')

db = SQLAlchemy(app)
class User(db.Model):
    def __init__(self,company,designation,review):
        self.company = company
        self.designation = designation
        self.review = review
    id = db.Column(db.Integer, primary_key = True)
    company = db.Column(db.String(15))
    designation = db.Column(db.String(15))
    review = db.Column(db.String(60))
    
db.create_all()

@app.route('/api/dataentry', methods = ['GET', 'POST'])
def submit_data():
    response_object = {'status':'success'}
    if request.method == "POST" or request.method == "OPTIONS":

        post_data = request.get_json()
        company = post_data.get('company')
        designation = post_data.get('designation')
        review = post_data.get('review')
        
        
        data = User(company=company, designation=designation, review=review)

        db.session.add(data)
        db.session.commit()
        
        response_object['message'] ='Data added!'
    return jsonify(response_object)

@app.route('/api/view', methods = ['GET','POST'])
def view_data():
    usuario = User.query.all()
    data = []
    for i in usuario:
        dic = {}
        dic['_id'] = i.id
        dic['company'] = i.company
        dic['designation'] = i.designation
        dic['review'] = i.review
        data.append(dic)
    return jsonify(data)

@app.route('/api/dataview/<dataid>', methods = ['DELETE'])
def delete_data(dataid):
    if request.method == "DELETE":
        _id = int(dataid)
        db.session.delete(User.query.get(_id))
        db.session.commit()

        response_object = {'status': 'success'}
        
    return jsonify(response_object)

@app.route('/api/dataview/<dataid>', methods = ['PUT'])
def modify_data(dataid):
    if request.method == 'PUT':
        post_data = request.get_json()
        _id = int(dataid)
        usuario  = User.query.get(_id)
        usuario.company = post_data.get('company')
        usuario.designation = post_data.get('designation')
        usuario.review = post_data.get('review')
        db.session.commit()

        response_object = {'status': 'success'}
        
    return response_object

if __name__ == '__main__':
    app.run(debug=True)