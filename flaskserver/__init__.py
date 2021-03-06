"""
api setup and route definitions
"""
import flaskserver.models
from flaskserver.database import init_db, db_session
from flask import Flask
from flask_restful import Api
from flaskserver.models import Asset_Account

from flaskserver.resource import Account

# setup
app = Flask(__name__)
api = Api(app)

# initialize dummy database
init_db()
if Asset_Account.query.all() == []:
    account_1 = Asset_Account()
    account_2 = Asset_Account()
    account_3 = Asset_Account()
    db_session.add(account_1)
    db_session.add(account_2)
    db_session.add(account_3)
    db_session.commit()

# Routing

"""
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
"""
api.add_resource(Account,
                 '/account',
                 '/account/<acc_no>',
                 '/account/<acc_no>/<string:asset_type>',
                 '/account/<acc_no>/<string:asset_type>/<string:start_time>/<string:end_time>',
                 '/account/<acc_no>/<string:start_time>/<string:end_time>',
                 endpoint='account')
