"""
helper function definitions
"""
from flaskserver.database import db_session
from flaskserver.models import Asset_Transaction, Asset
from flaskserver.validation import abort_if_insufficient_bal, abort_if_invalid_account


def deposit_to_account(acc_no, asset_type, amt):
    """
    Deposit given amount of asset type into given account
    """
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
    """
    Withdraw given amount of asset type from given account
    """
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
