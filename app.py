from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///package.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Package(db.Model):
    __table_arges__ = {'sqlite_autoincrement':True}
    id = db.Column(db.Integer,primary_key=True)
    city = db.Column(db.String(50))
    days =db.Column(db.Integer)
    price =db.Column(db.Integer)

    def __repr__(self):
        return '<Package %s>'% self.city

class PackageSchema(ma.Schema):
    class Meta:
        fields = ("id","city","days","price")

package_schema = PackageSchema()
packages_schema = PackageSchema(many=True)

@app.route('/') 
def hello_world(): 
	return 'Hello World'

@app.route('/viewAllPackages',methods=['GET'])
def get_allpackages():
    packages = Package.query.all()
    return jsonify(packages_schema.dump(packages))

@app.route('/addPackage',methods=['POST'])
def add_package():
    new_package = Package(city=request.json['city'],days=request.json['days'],price=request.json['price'])
    db.session.add(new_package)
    db.session.commit()
    id = new_package.id
    return 'Package with id='+str(id)+' created'

@app.route('/viewPackageById/<int:id>',methods=['GET'])
def get_package(id):
    package = Package.query.get(id)
    if package == None:
        return "No package with the given id found"
    return package_schema.dump(package)

@app.route('/viewPackageByCity/<string:city>',methods=['GET'])
def get_package_c(city):
    packages = Package.query.filter_by(city=city).all()
    if packages == []:
        return "No package found for given city"
    return jsonify(packages_schema.dump(packages))

@app.route('/updatePackage/<int:id>',methods=['PUT'])
def update_package(id):
    package = Package.query.get(id)

    if package == None:
        return "Updation failed due to invalid id"

    if 'city' in request.json:
        package.city = request.json['city']
    if 'days' in request.json:
        package.days = request.json['days']
    if 'price' in request.json:
        package.price = request.json['price']
    db.session.commit()
    return 'Package with id='+str(id)+' updated sucessfully'

@app.route('/deletePackage/<int:id>',methods=['DELETE'])
def delete_package(id):
    package = Package.query.get(id)
    if package == None:
        return "Deletion failed due to invalid id"
    db.session.delete(package)
    db.session.commit()
    return 'Package with id='+str(id)+' deleted sucessfully'

if __name__ == '__main__': 
	app.run() 
