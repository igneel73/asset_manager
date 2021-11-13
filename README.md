# Asset Manager

#### Description

REST web service to manage assets in a crypto account
with functionality for

1. Getting Balance
2. Depositing assets
3. Withdrawing assets
4. Exchanging assets within or between accounts

#### Installation & Running

###### Requires

1. python 3..8.x
2. pipenv

To install dependencies execute the following on the command line

    pipenv shell
    pipenv install

To run the server execute the following on the command line
python run.py

#### Routes

    GET account/acc_no -> get account asset balances
    GET account/acc_no/asset_type -> get specific asset balance
    GET account/acc_no/start_time/end_time -> get balances for time interval
    GET account/acc_no/asset_type/start_time/end_time -> get
    balance for asset_type in time interval

    Returns:
    {
        assets : [
            asset : asset type
            amount : asset amount
        ]
    }

###### DEPOSIT ROUTE

    POST account/acc_no -> deposit asset into account
    args -> deposit_amt : amount to deposit
    asset_type : asset to deposit

    Returns:
    if success
    {
        account_no : account credited to
        deposit_amt : deposited amount
        asset_type : asset type
    }

###### WITHDRAWAL ROUTE

    PUT account/acc_no -> withdraw asset from account
    args -> withdrawal_amt : amount to withdraw
    asset_type : asset to withdraw

    Returns:
    if success
    {
        account_no : debited account
        withdrawal_amt : debited amount
        asset_type : asset type
    }

###### EXCHANGE ROUTE

    PATCH account/ -> transfer asset from one account to another
    args -> src_acc_no : source account
    dest_acc_no : destination account
    src_asset_type : source asset
    dest_asset_type : destination asset
    transfer_amt : amount to be transferred

    Returns:
        {
            'src_account_no': src_acc_no,
            'dest_asset_type':  dest_asset_type,
            'transfer_amt': transfer_amt,
            'src_asset_type': src_asset_type,
            'dest_asset_type': src_asset_type,
            'exchange_amt': exchange_amt
        }

#### Errors

#### Future Work

What to work on given more time

1. mechanism to cache exchange rates for faster computation
2. Unit test coverage
3. private routes with authentication
4. More comprehensive validations
