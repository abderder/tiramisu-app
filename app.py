# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///commandes.db'
db = SQLAlchemy(app)

class Commande(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    date_commande = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Commande {self.nom}>'

@app.route('/')
def formulaire():
    return render_template('formulaire.html')

@app.route('/commander', methods=['POST'])
def commander():
    nom = request.form['nom']
    telephone = request.form['telephone']
    adresse = request.form['adresse']
    nouvelle_commande = Commande(nom=nom, telephone=telephone, adresse=adresse)
    db.session.add(nouvelle_commande)
    db.session.commit()
    return redirect(url_for('formulaire'))

@app.route('/dashboard')
def dashboard():
    tri = request.args.get('tri', 'date')
    if tri == 'nom':
        commandes = Commande.query.order_by(Commande.nom).all()
    elif tri == 'adresse':
        commandes = Commande.query.order_by(Commande.adresse).all()
    else:
        commandes = Commande.query.order_by(Commande.date_commande.desc()).all()
    return render_template('dashboard.html', commandes=commandes)

@app.route('/map')
def carte():
    commandes = Commande.query.all()
    return render_template('dashboard_map.html', commandes=commandes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

