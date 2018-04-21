# pylint:disable=missing-docstring, invalid-name, too-many-instance-attributes

from os import getenv
from unittest import TestCase


from api.helpers.general import digest
from api.models import (
    db, Board, Conversation, Deposit, Estate,
    Message, Payment, Role, Unit, User, Wallet)
from main import create_app


class BaseCase(TestCase):
    """
    Base class to be inherited by all other testcases.
    """

    def setUp(self):
        """
        Set up test application.
        """
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.client.headers = {'Authorization': getenv('TEST_TOKEN')}
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

        self.board1 = Board()
        self.board2 = Board()
        self.conversation1 = Conversation()
        self.conversation2 = Conversation()
        self.deposit1 = Deposit()
        self.deposit2 = Deposit()
        self.estate1 = Estate(address="Random Address 1")
        self.estate2 = Estate(address="Random Address 2")
        self.estate3 = Estate()
        self.headers = {'Authorization': getenv('TEST_TOKEN')}
        self.message1 = Message(sender=1,
                                content='Random Content')
        self.message2 = Message(sender=2,
                                content='Random Content')
        self.message3 = Message()
        self.payment1 = Payment()
        self.payment2 = Payment()
        self.role1 = Role(title='basic')
        self.role2 = Role(title='admin')
        self.role3 = Role(title='super_admin')
        self.role4 = Role()
        self.unit1 = Unit(name="Random Unit 1")
        self.unit2 = Unit(name="Random Unit 2")
        self.unit3 = Unit()
        self.user1 = User(
            name="First1 Middle1 Last1",
            phone_number="000 12 3456781",
            email="first1.last1@email.com",
            password=digest('ABC123!@#'))
        self.user2 = User(
            name="First2 Middle2 Last2",
            phone_number="000 12 3456782",
            email="first2.last2@email.com",
            password=digest('ABC123!@#')
        )
        self.user3 = User()
        self.user_new_data1 = {
            'phone_number': "000 12 3456783"}
        self.user_new_data2 = {
            'bad_field': "random"}
        self.wallet1 = Wallet()
        self.wallet2 = Wallet()
        self.board3_dict = {'members': [1, 2]}
        self.conversation3_dict = {
            "participants": [1, 2]}
        self.message4_dict = {
            "content": "New Message."}
        self.user1_dict = {
            "name": "First1 Middle1 Last1",
            "phone_number": "000 12 3456781",
            "email": "first1.last1@email.com",
            "password": "ABC123!@#"}

    def tearDown(self):
        """
        Delete database and recreate it with no data.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        # Check remote
