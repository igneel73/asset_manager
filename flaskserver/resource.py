'''
Api Resource definitons
'''

import requests
from flask_restful import Resource
from flaskserver.validation import abort_if_invalid_account
from flaskserver.database import db_session
from flaskserver.validation import parser
from flaskserver.helper import deposit_to_account, withdraw_from_account
from flaskserver.models import Asset_Account, Asset_Transaction
from sqlalchemy import select, func

'''
Asset Account that handles
 - computing and showing balances
 - depositing into account
 - withdrawing from account
 - exchanging between accounts
'''


class Account(Resource):

    '''
    Show account balances.  
    Parameters:
        acc_no - query arg - Account number
        start_time - query arg - Optional start time
        end_time - query arg - Optional end time 
        asset_type - query arg - Optional asset types to return
    Returns:
        {
            assets : [
                asset : asset type
                amount : asset amount
            ]
        }
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
    Deposit asset into account.  
    Parameters:
        acc_no - query arg - Account number
        Asset type - parsed arg - Asset type
        deposit_amt - parsed arg - Asset amount to deposit 
    Returns:
        if success
        {
            account_no : account credited to
            deposit_amt : deposited amount
            asset_type : asset type
        }
    '''

    def post(self, acc_no):
        # parse args
        args = parser.parse_args()
        asset_type = args['asset_type']
        deposit_amt = args['deposit_amt']

        deposit_to_account(acc_no, asset_type, deposit_amt)

        db_session.commit()
        ret_res = {
            'account_no': acc_no,
            'deposit_amt': deposit_amt,
            'asset_type': asset_type
        }
        return ret_res, 201

    '''
    Withdraw assets from account.  
    Parameters:
        acc_no - query arg - Account number
        Asset type - parsed arg - Asset type
        withdrawal_amt - parsed arg - Asset amount to withdraw
    Returns:
        if success
        {
            account_no : debited account
            withdrawal_amt : debited amount
            asset_type : asset type
        }
    '''

    def put(self, acc_no):
        # parse arguments
        args = parser.parse_args()
        asset_type = args['asset_type']
        withdrawal_amt = args['withdrawal_amt']

        withdraw_from_account(acc_no, asset_type, withdrawal_amt)

        db_session.commit()
        ret_res = {
            'account_no': acc_no,
            'withdrawal_amt': withdrawal_amt,
            'asset_type': asset_type
        }
        return ret_res, 201

    '''
    Exchange assets within an account, or between different accounts. 
    uses the crosstower api to grab the current exchange price
    in case of different src and dest asset types
    Parameters:
        src_acc_no - parsed arg - source account
        dest_acc_no - parsed arg - destination account
        src_asset_type - parsed arg - source asset
        dest_asset_type - parsed arg - destination asset
        transfer_amt - parsed arg - amount to be transfered from source
    Returns:
        {
            'src_account_no': src_acc_no,
            'dest_asset_type':  dest_asset_type,
            'transfer_amt': transfer_amt,
            'src_asset_type': src_asset_type,
            'dest_asset_type': src_asset_type,
            'exchange_amt': exchange_amt
        }
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
        ret_res = {
            'src_account_no': src_acc_no,
            'dest_asset_type':  dest_asset_type,
            'transfer_amt': transfer_amt,
            'src_asset_type': src_asset_type,
            'dest_asset_type': src_asset_type,
            'exchange_amt': exchange_amt
        }
        return ret_res, 201
