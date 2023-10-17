from flask import Flask
app = Flask(__name__)
app.secret_key = "Keep this a secret!"
app.config['upload_folder']='/Users/User/Documents/coding_dojo/projects_algos/Projects/nostalgic_toys/Nostalgic-Toys/flask_app/static/images/'