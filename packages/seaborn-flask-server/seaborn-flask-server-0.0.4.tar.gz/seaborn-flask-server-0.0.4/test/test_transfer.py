import os
import sys

flask_folder = os.path.abspath(__file__).replace('\\', '/').rsplit(
    '/flask_app', 1)[0]
sys.path.append(flask_folder)
from test.base import *
from test.test_account import AccountTest


class TransferTest(AccountTest):
    def test_account_deposit_transfer(self, username="Demo-User",
                                      account_name="demo_account",
                                      amount=100.00,
                                      receipt='receipt placeholder'):
        user, account = self.test_create_account(username, account_name)
        transfer = user.account.transfer.deposit.put(account['account_id'],
                                                     amount, receipt=receipt)

        self.assertEqual(amount, transfer['amount'])
        self.assertEqual(user.user_id, transfer['user_id'])
        self.assertEqual(account['account_id'], transfer['deposit_account_id'])
        self.assertEqual(receipt, transfer['receipt'])

        account2 = user.account.get(account['account_id'])
        self.assertEqual(account['funds'] + amount, account2['funds'])
        return user, account2, transfer

    def test_account_to_account_transfer(self, amount=50.0):
        user1, account1, transfer = self.test_account_deposit_transfer()
        user2, account2 = self.test_create_account("Demo-User2",
                                                   "demo_account2")

        transfer = user1.account.transfer.put(account1['account_id'],
                                              account2['account_id'], amount)
        self.assertEqual(amount, transfer['amount'])
        self.assertEqual(user1.user_id, transfer['user_id'])
        self.assertEqual(account1['account_id'],
                         transfer['withdraw_account_id'])
        self.assertEqual(account2['account_id'],
                         transfer['deposit_account_id'])

        account1_ = user1.account.get(account1['account_id'])
        self.assertEqual(account1['funds'] - amount, account1_['funds'])

        account2_ = user2.account.get(account2['account_id'])
        self.assertEqual(account2['funds'] + amount, account2_['funds'])
        return user1, account2, user2, account2, transfer

    def test_account_withdraw_transfer(self):
        user1, account1, user2, account2, transfer = \
            self.test_account_to_account_transfer()
        transfer = user2.account.transfer.withdraw.put(
            account2['account_id'], 50.0)
        self.assertEqual(50.0, transfer['amount'])
        self.assertEqual(user2.user_id, transfer['user_id'])
        self.assertEqual(account2['account_id'],
                         transfer['withdraw_account_id'])

        account2_ = user2.account.get(account2['account_id'])
        self.assertEqual(account2_['funds'], 0)
        return transfer

    def test_get_transfer(self):
        user, account, transfer1 = self.test_account_deposit_transfer()
        transfer2 = user.account.transfer.get(transfer1['transfer_id'])
        self.assertEqual(transfer1, transfer2)

    def test_get_transfers(self):
        user1, account1, user2, account2, transfer = \
            self.test_account_to_account_transfer()

        transfers = user2.account.transfer.array.get(account2['account_id'],
                                                     withdraws_only=True)
        self.assertNotIn(transfer, transfers)
