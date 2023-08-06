from .resource import Get, Post, Resource, Create
from .schemas import PermataVASchema, BCAVASchema, MandiriBillSchema, CIMBClicksSchema, BNIVASchema


class Transaction(Get):
    path = ""

    def get_status(self):
        return self.get('status')


class BankTransferTransaction(Transaction, Post, Create):
    path = ""

    def charge(self):
        return self.create('charge')

    def execute(self, attributes):
        return self.post('execute', attributes, self)


class PermataVATransaction(BankTransferTransaction):
    def __init__(self, attributes=None, api=None):
        BankTransferTransaction.__init__(self, attributes, api)
        _, errors = PermataVASchema().load(attributes)
        if errors:
            raise Exception(errors)


class BCAVATransaction(BankTransferTransaction):
    def __init__(self, attributes=None, api=None):
        BankTransferTransaction.__init__(self, attributes, api)
        _, errors = BCAVASchema().load(attributes)
        if errors:
            raise Exception(errors)


class BNIVATransaction(BankTransferTransaction):
    def __init__(self, attributes=None, api=None):
        BankTransferTransaction.__init__(self, attributes, api)
        _, errors = BNIVASchema().load(attributes)
        if errors:
            raise Exception(errors)


class MandiriBillTransaction(BankTransferTransaction):
    def __init__(self, attributes=None, api=None):
        BankTransferTransaction.__init__(self, attributes, api)
        _, errors = MandiriBillSchema().load(attributes)
        if errors:
            raise Exception(errors)


class CIMBClicksTransaction(BankTransferTransaction):
    def __init__(self, attributes=None, api=None):
        BankTransferTransaction.__init__(self, attributes, api)
        _, errors = CIMBClicksSchema().load(attributes)
        if errors:
            raise Exception(errors)
