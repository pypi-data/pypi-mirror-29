import random
import unittest
from datetime import datetime
from functools import wraps

from pynYNAB.ClientFactory import clientfromkwargs
from pynYNAB.scripts.__main__ import parser

from pynYNAB import KeyGenerator
from pynYNAB.schema.Entity import AccountTypes
from pynYNAB.schema.budget import Account
from pynYNAB.scripts.helpers import merge_config


def util_add_account(client, account_name=None):
    if account_name is None:
        account_name = str(KeyGenerator.generateuuid())
    account = Account(
        account_type=random.choice(list(AccountTypes)),
        account_name=account_name
    )

    client.add_account(account, balance=random.randint(-10, 10), balance_date=datetime.now())
    return account


def needs_account(account_name=None):
    def decorator(fn):
        @wraps(fn)
        def wrapped(self, *args, **kwargs):
            for account in self.client.budget.accounts:
                if account_name is None or account.account_name == account_name:
                    self.account = account
                    fn(self, *args, **kwargs)
                    return
            self.account = util_add_account(self.client, account_name)
            fn(self, *args, **kwargs)
            return

        return wrapped

    return decorator


class CommonLive(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(CommonLive, self).__init__(*args, **kwargs)
        self.account = None
        self.budget = None
        self.transaction = None
        self.client = None

    def reload(self):
        config = merge_config()
        self.client = clientfromkwargs(**config)

    def setUp(self):
        self.reload()


