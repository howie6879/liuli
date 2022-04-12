#!/usr/bin/env python
"""
    Created by howie.hu at 2022/4/12.
    Description：
    Changelog: all notable changes to this file will be documented
"""

from flask import Blueprint

from .bp_user import bp_user
from .bp_utils import bp_utils

bp_api_v1 = Blueprint("api_v1", __name__, url_prefix="/v1")
bp_api_v1.register_blueprint(bp_user)
bp_api_v1.register_blueprint(bp_utils)
