#This is the core framework for building the web application.
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file

#This extension provides integration with the SQLAlchemy ORM (Object Relational Mapper), allowing Flask to interact with databases.
from flask_sqlalchemy import SQLAlchemy

#A powerful data manipulation and analysis library.
import pandas as pd

#While not used directly in this code, it’s often included in such applications for handling file paths, environmental variables,
#or file operations. If needed, it could be used for managing file storage or paths for the exported files.
import os

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vulnerabilities.db'  # Use SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Vulnerability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    risk_score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Vulnerability {self.name}>'

# Risk calculation logic based on OWASP guidelines
def calculate_risk(likelihood, impact):
    risk = likelihood * impact
    if risk < 30:
        return "Low"
    elif 30 <= risk < 60:
        return "Medium"
    else:
        return "High"

# Mitigation suggestions based on risk level
def get_mitigation_suggestion(risk_level):
    suggestions = {
        "Low": "Monitor the vulnerability and plan for future mitigation.",
        "Medium": "Prioritize fixing the vulnerability in the next development cycle.",
        "High": "Immediate action required to fix the vulnerability."
    }
    return suggestions.get(risk_level, "No suggestion available.")

@app.route('/')
def home():
    #Renders index.html when a user visits the root URL (/), showing the main interface.
    return render_template('index.html')

@app.route('/calculate-risk', methods=['POST'])
def calculate():
    vulnerability = request.form['vulnerability']
    description = request.form['description']  # Get the description from the form
    likelihood = int(request.form['likelihood'])
    impact = int(request.form['impact'])

    # Calculate risk level
    risk_level = calculate_risk(likelihood, impact)
    mitigation = get_mitigation_suggestion(risk_level)

    # Store the vulnerability in the database
    risk_score = likelihood * impact
    new_vulnerability = Vulnerability(
        name=vulnerability,
        description=description,  # Store the description
        risk_score=risk_score
    )
    db.session.add(new_vulnerability)
    db.session.commit()

    return jsonify({
        'vulnerability': vulnerability,
        'risk_level': risk_level,
        'mitigation': mitigation
    })

# Route to List Vulnerabilities
@app.route('/vulnerabilities')
def vulnerabilities():
    vulnerabilities = Vulnerability.query.all()
    return render_template('vulnerabilities.html', vulnerabilities=vulnerabilities)

# Route to Export Vulnerabilities to Excel
@app.route('/export')
def export_vulnerabilities():
    vulnerabilities = Vulnerability.query.all()
    # Prepare data for DataFrame
    data = {
        'Vulnerability Name': [v.name for v in vulnerabilities],
        'Description': [v.description for v in vulnerabilities],
        'Risk Score': [v.risk_score for v in vulnerabilities],
    }

    df = pd.DataFrame(data)  # Create a DataFrame

    # Export to Excel
    excel_file = 'vulnerabilities.xlsx'
    df.to_excel(excel_file, index=False, engine='openpyxl')  # Save as Excel file

    return send_file(excel_file, as_attachment=True)  # Send file for download

# Route to delete all vulnerabilities
@app.route('/delete-all', methods=['POST'])
def delete_all_vulnerabilities():
    Vulnerability.query.delete()  # Delete all records in the Vulnerability table
    db.session.commit()
    return redirect(url_for('vulnerabilities'))

# Create the database tables if not exist
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True)
