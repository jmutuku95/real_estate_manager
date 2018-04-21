"""
Models and their methods.
"""

from operator import itemgetter
from time import time

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.collections import InstrumentedList

from api.helpers.general import is_substring

# pylint:disable=no-member, invalid-name, broad-except, no-else-return

db = SQLAlchemy()


class BaseModel(db.Model):
    """
    Base model with all main requirements of a model.
    """

    __abstract__ = True

    def delete(self):
        """
        Delete an object from the database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return {
                "message": "Database encountered an error upon deletion.",
                "help": "Ensure the database is running properly.",
                "exception": e
            }

    def insert(self, field, values):
        """
        Insert values into a relationship field.
        If inserting one-to-one or reverse one-to-many, values is an object.
        For example(model.insert('field', object))
        If inserting many-to-many or one-to-many, values are a list of objects.
        For example(model.insert('field', [object1, ...]))
        If only one object, (model.insert('field', [object1]))
        """
        try:
            current_values = getattr(self, field)
        except AttributeError:
            return {
                "message": "Ensure the  field passed is valid.",
                "help": "The field should be an attribute of the object."
            }
        if isinstance(current_values, InstrumentedList):
            if not isinstance(values, list):
                return {
                    "message": "Ensure objects passed are as a list.",
                    "help": "This eases updating of (one)many-to-many fields"
                }
            try:
                current_values.extend(values)
            except Exception as e:
                return {
                    "message": "Ensure the values you're inserting are valid.",
                    "help": "The objects should relate to the inserted field.",
                    "exception": e
                }
            try:
                db.session.add(self)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                return {
                    "message": "Ensure the object you're saving is valid",
                    "help": "Has all fields and doesn't repeat unique values.",
                    "exception": e
                }
        try:
            setattr(self, field, values)
        except Exception as e:
            return {
                "message": "Ensure the values you're inserting are valid.",
                "help": "The objects should relate to the inserted field.",
                "exception": e
            }
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return {
                "message": "Ensure the object you're saving is valid",
                "help": "Has all fields and doesn't repeat unique values.",
                "exception": e
            }

    def remove(self, field, **kwargs):
        """
        Remove values from a relationship field.
        This replaces the value with None or an empty list.
        Pass in the field and unique argument to isolate object for removal.
        """
        try:
            current_values = getattr(self, field)
        except AttributeError:
            return {
                "message": "Ensure the  field passed is valid.",
                "help": "The field should be an attribute of the object."
            }
        if isinstance(current_values, InstrumentedList):
            if kwargs:
                key = [i for i in kwargs][0]
                try:
                    item_index = current_values.index([
                        i for i in current_values
                        if getattr(i, key) == kwargs[key]
                    ][0])
                    current_values.pop(item_index)
                except Exception as e:
                    return {
                        "message": "Ensure the arguments passed are valid.",
                        "help": "Should be of an existent object and unique.",
                        "exception": e
                    }
            else:
                setattr(self, field, InstrumentedList([]))
        else:
            setattr(self, field, None)
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return {
                "message": "Ensure the object saved after deletion is valid",
                "help": "Has all fields and doesn't repeat unique values.",
                "exception": e
            }

    def save(self):
        """
        Save an object in the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except Exception as e:
            db.session.rollback()
            return {
                "message": "Ensure the object you're saving is valid",
                "help": "Has all fields and doesn't repeat unique values.",
                "exception": e
            }

    def serialize(self):
        """
        Convert sqlalchemy object to dictionary.
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def update(self, new_data):
        """
        Update an object with new information.
        """
        all_keys = [key for key in self.__dict__]
        keys = [key for key in new_data]
        for key in keys:
            if key in all_keys:
                setattr(self, key, new_data[key])
            else:
                return {
                    "message": "Error encountered when setting attributes.",
                    "help": "Ensure all fields you're updating are valid."
                }
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return {
                "message": "Database encountered error upon updating.",
                "help": "Ensure the database is running properly.",
                "exception": e
            }

    @classmethod
    def check_exists(cls, **kwargs):
        """
        Check whether an object exists in the database.
        """
        return bool(cls.query.filter_by(**kwargs).first())

    @classmethod
    def drop(cls):
        """
        Delete all objects of a table.
        """
        for i in cls.get_all():
            i.delete()
        return True

    @classmethod
    def get(cls, **kwargs):
        """
        Get a specific object from the database.
        """
        result = cls.query.filter_by(**kwargs).first()
        if not result:
            return {
                "message": "The object does not exist",
                "help": "Ensure arguments are of existent objects and unique."
            }
        return result

    @classmethod
    def get_all(cls):
        """
        Get all objects of a specific table.
        """
        result = cls.query.all()
        if not result:
            return {
                "message": "The class of objects do not exist",
                "help": "Ensure the class required has objects."
            }
        return result

    @classmethod
    def search(cls, **kwargs):
        """
        Search through values of string fields.
        If searched value is a substring of a field, return the field's object.
        """
        key = [key for key in kwargs][0]
        objects = cls.get_all()
        if isinstance(objects, dict):
            return objects
        results = []
        for i in objects:
            if is_substring(kwargs[key], getattr(i, key)):
                results.append(i)
        if not results:
            return {
                "message": "No objects match the searched value.",
                "help": "Ensure arguments are of existent objects."
            }
        return results


user_conversations = db.Table(
    'user_conversations',
    db.Column(
        'user_id',
        db.Integer(),
        db.ForeignKey('user.id'),
        nullable=False),
    db.Column(
        'conversation_id',
        db.Integer(),
        db.ForeignKey('conversation.id'),
        nullable=False))

user_boards = db.Table(
    'user_boards',
    db.Column(
        'user_id',
        db.Integer(),
        db.ForeignKey('user.id'),
        nullable=False),
    db.Column(
        'board_id',
        db.Integer(),
        db.ForeignKey('board.id'),
        nullable=False))

user_roles = db.Table(
    'user_roles',
    db.Column(
        'user_id',
        db.Integer(),
        db.ForeignKey('user.id'),
        nullable=False),
    db.Column(
        'role_id',
        db.Integer(),
        db.ForeignKey('role.id'),
        nullable=False))


class User(BaseModel):
    """
    User's model.
    """
    id = db.Column(db.Integer(),
                   primary_key=True)
    email = db.Column(db.String(),
                      unique=True)
    name = db.Column(db.String(),
                     nullable=False)
    password = db.Column(db.String(),
                         nullable=False)
    phone_number = db.Column(db.String(),
                             nullable=False,
                             unique=True)
    boards = db.relationship('Board',
                             secondary='user_boards',
                             backref=db.backref('members',
                                                lazy=True,
                                                uselist=True))
    conversations = db.relationship('Conversation',
                                    secondary='user_conversations',
                                    backref=db.backref('participants',
                                                       lazy=True,
                                                       uselist=True))
    roles = db.relationship('Role',
                            secondary='user_roles',
                            backref=db.backref('users',
                                               lazy=True,
                                               uselist=True))
    units = db.relationship('Unit',
                            backref='resident',
                            lazy=True,
                            uselist=True)
    wallet = db.relationship('Wallet',
                             backref='owner',
                             lazy=True,
                             uselist=False,
                             cascade="all,delete")

    def view_public(self):
        """
        Public view of a user's profile.
        """
        user = self.serialize()
        del user['password']
        return user

    def view_private(self):
        """
        Private view of a user's profile.
        """
        roles = [role.serialize() for role in self.roles]
        wallet = self.wallet.serialize()
        boards = [board.serialize() for board in self.boards]
        conversations = self.conversations
        messages = [conversation.messages for conversation in conversations]
        conversations = [conversation.serialize()
                         for conversation in conversations]
        for conversation in conversations:
            conversation.update(
                {
                    'messages': [
                        message.serialize()
                        for message in messages[
                            conversations.index(conversation)]]
                }
            )
        user = self.serialize()
        user.update({'roles': roles, 'wallet': wallet,
                     'conversations': conversations, 'boards': boards})
        del user['password']
        return user


class Board(BaseModel):
    """
    Board model.
    """
    id = db.Column(db.Integer(),
                   primary_key=True)
    estates_owned = db.relationship('Estate',
                                    backref='board',
                                    lazy=True,
                                    uselist=True)
    units_owned = db.relationship('Unit',
                                  backref='board',
                                  lazy=True,
                                  uselist=True)
    conversation = db.relationship('Conversation',
                                   backref='board',
                                   lazy=True,
                                   uselist=False,
                                   cascade="all,delete")

    def __repr__(self):
        return {
            'id': self.id,
            'members': [i.view_public() for i in self.members]
        }

    def view(self):
        board = self.serialize()
        board.update({'members': [i.view_public() for i in self.members]})
        board.update({'estates_owned': [i.__repr__()
                                        for i in self.estates_owned]})
        board.update({'units_owned': [i.__repr__() for i in self.units_owned]})
        return board


class Estate(BaseModel):
    """
    Estate model.
    """
    id = db.Column(db.Integer(),
                   primary_key=True)
    address = db.Column(db.String(),
                        nullable=False)
    estate_units = db.relationship('Unit',
                                   backref='estate',
                                   lazy=True,
                                   uselist=True)
    payment = db.relationship('Payment',
                              backref='estate',
                              lazy=True,
                              uselist=False)
    board_id = db.Column(db.Integer(),
                         db.ForeignKey('board.id'),
                         nullable=True)

    def __repr__(self):
        return {'id': self.id, 'address': self.address}

    def view(self):
        estate = self.serialize()
        estate.update({'board': self.board.__repr__()})
        estate.update({'payment': self.payment.__repr__()})
        estate.update({'units': [unit.view() for unit in self.estate_units]})
        return estate


class Unit(BaseModel):
    """
    Unit model.
    """
    id = db.Column(db.Integer(),
                   primary_key=True)
    name = db.Column(db.String(),
                     nullable=False)
    payment = db.relationship('Payment',
                              backref='unit',
                              lazy=True,
                              uselist=False)
    board_id = db.Column(db.Integer(),
                         db.ForeignKey('board.id'),
                         nullable=True)
    estate_id = db.Column(db.Integer(),
                          db.ForeignKey('estate.id'),
                          nullable=True)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('user.id'),
                        nullable=True)

    def __repr__(self):
        return {'id': self.id, 'name': self.name,
                'estate': self.estate.__repr__()}

    def view(self):
        unit = self.serialize()
        unit.update({'estate': self.estate.__repr__()})
        unit.update({'payment': self.payment.__repr__()})
        unit.update({'board': self.board.__repr__()})


class Wallet(BaseModel):
    """
    Wallet model.
    """
    id = db.Column(db.Integer(),
                   primary_key=True)
    balance = db.Column(db.Float(),
                        default=0.0)
    payments = db.relationship('Payment',
                               backref='wallet',
                               lazy=True,
                               uselist=True)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('user.id'),
                        nullable=True)

    def __repr__(self):
        {
            'id': self.id,
            'balance': self.balance
        }

    def view(self):
        wallet = self.serialize()
        payments = [i.view() for i in self.payments]
        wallet.update({'payments': payments})
        return wallet


class Payment(BaseModel):
    """
    Payment model.
    """
    id = db.Column(db.Integer(),
                   primary_key=True)
    balance = db.Column(db.Float(),
                        default=0.0)
    required = db.Column(db.Float(),
                         default=0.0)
    deposits = db.relationship('Deposit',
                               backref='payment',
                               lazy=True,
                               uselist=True,
                               cascade="all,delete")
    estate_id = db.Column(db.Integer(),
                          db.ForeignKey('estate.id'),
                          nullable=True)
    unit_id = db.Column(db.Integer(),
                        db.ForeignKey('unit.id'),
                        nullable=True)
    wallet_id = db.Column(db.Integer(),
                          db.ForeignKey('wallet.id'),
                          nullable=True)

    def __repr__(self):
        return {
            'id': self.id,
            'required': self.required,
            'balance': self.balance
        }

    def view(self):
        payment = self.serialize()
        deposits = [i.view() for i in self.deposits]
        payment.update({'deposits': deposits})
        return payment


class Deposit(BaseModel):
    """
    Deposit model.
    """
    id = db.Column(db.Integer(),
                   primary_key=True)
    amount = db.Column(db.Float(),
                       default=0.0)
    period_end = db.Column(db.Float(),
                           default=time())
    period_start = db.Column(db.Float(),
                             default=time())
    timestamp = db.Column(db.Float(),
                          default=time())
    payment_id = db.Column(db.Integer(),
                           db.ForeignKey('payment.id'),
                           nullable=True)

    def view(self):
        return self.serialize()


class Conversation(BaseModel):
    """
    Conversation model.
    """
    id = db.Column(db.Integer(),
                   primary_key=True)
    timestamp = db.Column(db.Float(),
                          default=time())
    messages = db.relationship('Message',
                               backref='conversation',
                               lazy=True,
                               uselist=True,
                               cascade="all,delete")
    board_id = db.Column(db.Integer(),
                         db.ForeignKey('board.id'),
                         nullable=True)

    def view(self):
        conversation = self.serialize()
        conversation.update({'participants': [i.view_public()
                                              for i in self.participants]})
        conversation.update(
            {'messages': sorted(
                [i.serialize() for i in self.messages],
                key=itemgetter('timestamp'))})
        return conversation


class Message(BaseModel):
    """
    Message model.
    """
    id = db.Column(db.Integer(),
                   primary_key=True)
    content = db.Column(db.String(),
                        nullable=True)
    sender = db.Column(db.Integer(),
                       nullable=False)
    timestamp = db.Column(db.Float(),
                          default=time())
    conversation_id = db.Column(db.Integer(),
                                db.ForeignKey('conversation.id'),
                                nullable=True)

    def view(self):
        return self.serialize()


class Role(BaseModel):
    """
    Role model.
    """
    id = db.Column(db.Integer(),
                   primary_key=True)
    title = db.Column(db.String(),
                      nullable=False)

    def view(self):
        return self.serialize()
