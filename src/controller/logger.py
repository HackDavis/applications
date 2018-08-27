from flask import Blueprint
import logging

logger = Blueprint('logger', __name__)


@logger.errorhandler(500)
def catch_500_errors(e):
    """Log 500 errors"""
    logging.exception("Error occurred while serving request")
