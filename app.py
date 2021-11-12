import requests
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from database import init_db, db_session
from models import Asset, Asset_Account, Asset_Transaction


# setup
app = Flask(__name__)
api = Api(app)
init_db()

# argument parsing, and validations
parser = reqparse.RequestParser()
parser.add_argument('asset_type')
parser.add_argument('deposit_amt', type=float)
parser.add_argument('withdrawal_amt', type=float)
parser.add_argument('src_acc_no', type=int)
parser.add_argument('dest_acc_no', type=int)
parser.add_argument('src_asset_type')
parser.add_argument('dest_asset_type')
parser.add_argument('transfer_amt', type=float)


def abort_if_insufficient_bal(acc_no, asset_type, amt):
    asset = Asset.query.filter(
        Asset.owner_account == acc_no, Asset.asset == asset_type).first()
    if asset == None or asset.amount < amt:
        abort(401, message=f'account {acc_no} has insufficient balance')


def abort_if_invalid_account(acc_no):
    account = db_session.get(Asset_Account, acc_no)
    if account == None:
        abort(401, message=f'account {acc_no} does not exist')

# helper function


def deposit_to_account(acc_no, asset_type, amt):

    abort_if_invalid_account(acc_no)
    # store account transaction
    new_transaction = Asset_Transaction(
        asset=asset_type, amount=amt, owner_account=acc_no)
    db_session.add(new_transaction)

    # credit asset to account
    # create asset row if it doesn't exist
    asset_to_credit = Asset.query.filter(
        Asset.owner_account == acc_no, Asset.asset == asset_type).first()
    if asset_to_credit == None:
        asset_to_credit = Asset(
            owner_account=acc_no, asset=asset_type, amount=amt)
        db_session.add(asset_to_credit)
    else:
        asset_to_credit.amount += amt
        db_session.flush()


def withdraw_from_account(acc_no, asset_type, amt):
    # check for sufficient balance
    abort_if_invalid_account(acc_no)
    abort_if_insufficient_bal(acc_no, asset_type, amt)

    # store transaction
    new_transaction = Asset_Transaction(
        asset=asset_type, amount=(-amt), owner_account=acc_no)
    db_session.add(new_transaction)

    # debit asset from account
    asset_to_debit = Asset.query.filter(
        Asset.owner_account == acc_no, Asset.asset == asset_type).first()
    asset_to_debit.amount -= amt
    db_session.flush()


# Resource


class Account(Resource):

    '''
    Show account balances.  Parameters:
    Account number
    Optional start time
    Optional end time
    Optional asset types
    '''

    def get(self, acc_no, start_time=None, end_time=None, asset_type=None):
        # check account
        abort_if_invalid_account(acc_no)
        ret_balance = 0
        account = db_session.get(Asset_Account, acc_no)
        assets = account.assets

        # compute balance based on time

        # return specific asset
        if asset_type != None:
            for asset in assets:
                if asset.asset == asset_type:
                    ret_balance = {'asset': asset.asset,
                                   'amount': asset.amount}
        # return all assets
        else:
            ret_balance = {'assets': []}
            for asset in assets:
                ret_balance['assets'].append(
                    {'asset': asset.asset, 'amount': asset.amount})

        return ret_balance, 201

    '''
    Deposit asset into account.  Parameters:
    Account number
    Asset type
    Asset amount to deposit
    '''

    def post(self, acc_no):
        # parse args
        args = parser.parse_args()
        asset_type = args['asset_type']
        deposit_amt = args['deposit_amt']

        deposit_to_account(acc_no, asset_type, deposit_amt)

        db_session.commit()
        return acc_no, 201

    '''
    Withdraw assets from account.  Parameters:
    Account number
    Asset type
    Asset amount to withdraw
    '''

    def put(self, acc_no):
        # parse arguments
        args = parser.parse_args()
        asset_type = args['asset_type']
        withdrawal_amt = args['withdrawal_amt']

        withdraw_from_account(acc_no, asset_type, withdrawal_amt)

        db_session.commit()
        return acc_no, 201

    '''
    Exchange assets within an account, or between different accounts. 
    Parameters:
    From:
    Account number
    Asset type
    Amount
    To:
    Account number
    Asset type
    (the backend should compute the resulting target 
    amount using some reasonable mechanism, or describe
    how that computation would be done)
    '''

    def patch(self):
        # parse arguments
        args = parser.parse_args()
        src_acc_no = args['src_acc_no']
        dest_acc_no = args['dest_acc_no']
        src_asset_type = args['src_asset_type']
        dest_asset_type = args['dest_asset_type']
        transfer_amt = args['transfer_amt']
        exchange_amt = 0

        # find exchange rate
        if src_asset_type != dest_asset_type:
            request_url = f'https://api.crosstower.com/api/3/public/price/rate?from={src_asset_type}&to={dest_asset_type}'
            exchange_response = requests.get(url=request_url).json()
            exchange_amt = transfer_amt * \
                float(exchange_response[src_asset_type]['price'])
        else:
            exchange_amt = transfer_amt

        # call deposit and withdrawal
        withdraw_from_account(src_acc_no, src_asset_type, transfer_amt)
        deposit_to_account(dest_acc_no, dest_asset_type, exchange_amt)

        db_session.commit()
        return src_acc_no, 201


# Routing

'''
    BALANCE ROUTES
    GET account/acc_no -> get account asset balances
    GET account/acc_no/asset_type -> get specific asset balance
    GET account/acc_no/start_time/end_time -> get balances for time interval
    GET account/acc_no/asset_type/start_time/end_time -> get balance for asset_type in time interval

    DEPOSIT ROUTE
    POST account/acc_no -> deposit asset into account
        args -> deposit_amt : amount to deposit
                asset_type : asset to deposit

    WITHDRAWAL ROUTE
    PUT account/acc_no -> withdraw asset from account
        args -> withdrawal_amt : amount to withdraw
                asset_type : asset to withdraw
    
    EXCHANGE ROUTE
    PATCH account/ -> transfer asset from one account to another
        args -> src_acc_no : source account
                dest_acc_no : destination account
                src_asset_type : source asset
                dest_asset_type : destination asset
                transfer_amt : amount to be transferred
'''
api.add_resource(Account,
                 '/account',
                 '/account/<acc_no>',
                 '/account/<acc_no>/<string:asset_type>',
                 '/account/<acc_no>/<string:asset_type>/<int:start_time>/<int:end_time>',
                 '/account/<acc_no>/<int:start_time>/<int:end_time>',
                 endpoint='account')


# execution
if __name__ == '__main__':
    app.run(debug=True)
