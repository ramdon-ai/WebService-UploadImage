import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
app = Flask(__name__)

app_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///upload.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class gambar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_file = db.Column(db.String(80))
    gambar = db.Column(db.LargeBinary)
    waktu = db.Column(db.DateTime, default=datetime.datetime.utcnow)
db.create_all()

@app.route('/upload', methods=['POST'])
def upload():
    dataNama = request.form.get('nama_file')
    dataGambar = request.files['gambar']
    
    if 'gambar' not in request.files:
        return jsonify({'msg': 'File Tidak Boleh Kosong'})

    if dataNama and dataGambar:
        data = gambar(nama_file=dataNama, gambar=dataGambar.read())
        db.session.add(data)
        db.session.commit()
        return jsonify({'msg': 'Upload Berhasil'})
    else:
        return jsonify({'msg': 'Upload Gagal'})
    
if __name__ == "__main__":
    app.run(debug=True)