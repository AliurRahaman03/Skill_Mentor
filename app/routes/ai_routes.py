from flask import Blueprint, request, session, flash, redirect, url_for, render_template
from app import db
from app.models.model import Skill, User, LearningPath
from app.services.ai_service import generate_roadmap
#from openai import OpenAIError


bp = Blueprint("ai_routes", __name__)

@bp.route("/generate-roadmap", methods=["POST"])
def generate_roadmap_route():
    if "user_id" not in session:
        flash("Please log in to generate a roadmap")
        return redirect(url_for("auth_routes.login"))
        
    user_id = session["user_id"]
    user = User.query.get(user_id)
    if not user:
        flash("User not found")
        return redirect(url_for("auth_routes.logout"))
        
    target_role = request.form.get("target_role")
    if not target_role:
        flash("Please specify a target role")
        return redirect(url_for("skill_routes.get_skills"))
        
    skills = [s.skill_name for s in Skill.query.filter_by(user_id=user_id).all()]
    roadmap = generate_roadmap(user.name, skills, target_role)
    
    # Save the learning path
    learning_path = LearningPath(
        user_id=user_id,
        target_role=target_role,
        title=roadmap.get("title", "Custom Learning Path"),
        content=roadmap
    )
    db.session.add(learning_path)
    db.session.commit()
    
    return render_template("roadmap.html", roadmap=roadmap)