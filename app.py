from flask import Flask
from flask_restful import Api, Resource
from database import init_db


# setup
app = Flask(__name__)
api = Api(app)
init_db()

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
        pass

    '''
    Deposit asset into account.  Parameters:
    Account number
    Asset type
    Asset amount to deposit
    '''

    def post(self, acc_no):
        pass

    '''
    Withdraw assets from account.  Parameters:
    Account number
    Asset type
    Asset amount to withdraw
    '''

    def put(self, acc_no):
        pass

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
        pass


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
