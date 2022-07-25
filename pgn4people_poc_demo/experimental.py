"""
Module to hold experimental routes and their supporting code
"""

from flask import Blueprint
from flask import render_template

blueprint = Blueprint('experimental', __name__)
@blueprint.route('/experimental')
def test():
    return render_template("/experimental.html")