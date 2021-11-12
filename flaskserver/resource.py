import requests
from flask_restful import Resource
from flaskserver.validation import abort_if_invalid_account
from flaskserver.database import db_session
from flaskserver.validation import parser
from flaskserver.helper import deposit_to_account, withdraw_from_account
from flaskserver.models import Asset_Account, Asset_Transaction
from sqlalchemy import select, func

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
        if start_time != None:
            assets = db_session.execute(
                select(Asset_Transaction.asset,
                       func.sum(Asset_Transaction.amount).label("amount")).
                group_by(
                    Asset_Transaction.asset
                ).
                having(
                    Asset_Transaction.owner_account == acc_no,
                    Asset_Transaction.timestamp >= start_time,
                    Asset_Transaction.timestamp <= end_time
                )
            ).all()
            ret_balance = {'assets': []}

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
