from flask import Blueprint, redirect, render_template, url_for, session
from ..ext import db, login_required, current_user


from ..forms.profile import BioForm, StatusForm

from ..models.user import User, Profile

profile = Blueprint("profile",__name__)


# /profile/bio - Updates the logged in users bio
@profile.post("/bio")
@login_required
def update_bio():
    form = BioForm()
    if form.is_submitted():
        # We simply update the property
        #current_user.profile().bio = update_bio.bio.data
        profile = Profile.query.filter_by(id=current_user.id).first()
        if profile:
            profile.bio = form.bio.data
        # And save the changes.
        db.session.commit()
        
    # Always redirect to the dashboard
    return redirect(url_for('main.dashboard'))

@profile.post("/status")
@login_required
def update_status():
    form = StatusForm()
    if form.is_submitted():
        # Again we just update the status
        current_user.profile().status = form.status.data
        # Save the changes
        db.session.commit()
    
    # Always redirect
    return redirect(url_for('main.dashboard'))
