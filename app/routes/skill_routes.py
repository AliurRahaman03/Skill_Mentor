from flask import Blueprint, request, jsonify, session,flash,redirect,url_for, render_template
from app.models.model import Skill
from app import db

bp = Blueprint("skill_routes", __name__)

@bp.route("/view-skills", methods=["GET"])
def get_skills():
    if "user_id" not in session:
        flash("Please log in to view your skills")
        return redirect(url_for("auth_routes.login"))
        
    user_id = session["user_id"]
    skills = Skill.query.filter_by(user_id=user_id).all()
    return render_template("skill.html", skills=skills)
    

@bp.route("/add", methods=["POST"])
def add_skills():
    if "user_id" not in session:
        flash("You must be logged in to add a skill")
        return redirect(url_for("auth_routes.login"))
    
    skill_name = request.form.get("skill_name")
    if not skill_name:
        flash("Skill name is required")
        return redirect(url_for("skill_routes.get_skills"))
    
    # Get the selected level from radio buttons
    level = request.form.get("level")
    if not level:
        flash("Please select a skill level")
        return redirect(url_for("skill_routes.get_skills"))
        
    user_id = session["user_id"]
    
    new_skill = Skill(user_id=user_id, skill_name=skill_name, level=level)
    db.session.add(new_skill)
    db.session.commit()
    
    flash("New skill added!")
    return redirect(url_for("skill_routes.get_skills"))

@bp.route("/remove/<int:id>", methods=["POST"])
def remove(id):
    # Ensure user is logged in
    if "user_id" not in session:
        flash("You must be logged in to delete a skill")
        return redirect(url_for("auth_routes.login"))

    skill = Skill.query.get_or_404(id)

    # Only allow owners to delete their skills
    if skill.user_id != session.get("user_id"):
        flash("Unauthorized to delete this skill")
        return redirect(url_for("auth_routes.user"))

    db.session.delete(skill)
    db.session.commit()
    flash("Skill deleted successfully!")
    # Redirect back to the skills listing
    return redirect(url_for("skill_routes.get_skills"))
