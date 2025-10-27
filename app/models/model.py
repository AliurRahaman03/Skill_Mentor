from app import db


class User(db.Model):
    __tablename__ = "users"
    # primary key must be declared with primary_key=True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    # Add relationships
    skills = db.relationship('Skill', backref='user', lazy=True)
    learning_paths = db.relationship('LearningPath', backref='user', lazy=True)

class Skill(db.Model):
    __tablename__ = "skills"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_name = db.Column(db.String(80), nullable=False)
    level = db.Column(db.String(20), nullable=False)

class LearningPath(db.Model):
    __tablename__ = "learning_paths"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_role = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(200))
    content = db.Column(db.JSON)
    