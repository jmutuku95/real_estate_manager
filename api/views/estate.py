"""
Estate manipulation functionality.
"""

from flask import request
from flask_restful import Resource

from api.models import Estate


class EstateResource(Resource):
    """
    View functions for estates.
    """

    def get(self, estate_id):
        """
        View an estate.
        """
        estate = Estate.get(id=estate_id)
        if isinstance(estate, dict):
            return {
                'status': 'fail',
                'message': 'The estate does not exist.',
                'help': 'Ensure estate_id is of an existent estate.'
            }, 404
        else:
            return {
                'status': 'success',
                'data': {
                    'estate': estate.view()
                }
            }, 200
