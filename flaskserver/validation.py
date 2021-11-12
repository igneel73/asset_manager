from flask_restful import reqparse, abort
from flaskserver.models import Asset, Asset_Account
from flaskserver.database import db_session

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
