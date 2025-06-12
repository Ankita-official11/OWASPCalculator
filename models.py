from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object
db = SQLAlchemy()

# Define the Vulnerability model
class Vulnerability(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each vulnerability
    name = db.Column(db.String(100), nullable=False)  # Name of the vulnerability
    description = db.Column(db.String(500), nullable=False)  # Description of the vulnerability
    risk_score = db.Column(db.Integer, nullable=False)  # Calculated risk score based on likelihood and impact

    def __repr__(self):
        return f'<Vulnerability {self.name}>'
