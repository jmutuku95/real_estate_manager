# pylint:disable=missing-docstring, invalid-name

from json import dumps, loads

from api.models import Board, Estate, Payment
from tests.base import BaseCase


class TestEstate(BaseCase):
    """
    Estate resource tests.
    """

    def test_view_estate_nonexistent(self):
        response = self.client.get(
            '/api/v1/estates/1'
        )
        self.assertEqual(404, response.status_code)
        expected = {
            'status': 'fail',
            'message': 'The estate does not exist.',
            'help': 'Ensure estate_id is of an existent estate.'
        }
        actual = loads(response.data)
        self.assertEqual(expected, actual)

    def test_view_estate(self):
        self.estate1.save()
        self.board1.save()
        self.payment1.save()
        estate1 = Estate.get(id=1)
        estate1.insert('payment', Payment.get(id=1))
        estate1.insert('board', Board.get(id=1))
        response = self.client.get(
            '/api/v1/estates/1'
        )
        self.assertEqual(200, response.status_code)
        expected = {
            'status': 'success',
            'data': {
                'estate': {
                    'id': 1, 'address': 'Random Address 1', 'board_id': 1,
                    'board': {'id': 1, 'members': []},
                    'payment': {'id': 1, 'required': 0.0, 'balance': 0.0},
                    'units': []}}}
        actual = loads(response.data)
        self.assertDictEqual(expected, actual)
