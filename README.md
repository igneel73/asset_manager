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

    Examples:
    http://127.0.0.1:5000/account/1
    http://127.0.0.1:5000/account/1/BTC
    http://127.0.0.1:5000/account/1/2021-11-13%2014:08:18.431806/2021-11-13%2014:11:22.550878
    http://127.0.0.1:5000/account/1/BTC/2021-11-13%2014:08:18.431806/2021-11-13%2014:11:22.550878

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

    Example:
    curl http://127.0.0.1:5000/account/1 -d "deposit_amt=2.3401" -d "asset_type=USD" -X POST

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

    Example:
    curl http://127.0.0.1:5000/account/1 -d "withdrawal_amt=2.3401" -d "asset_type=USD" -X PUT

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

    Example:
    curl http://127.0.0.1:5000/account -d "src_acc_no=1" -d "dest_acc_no=2" -d "src_asset_type=USD" -d "dest_asset_type=BTC" -d "transfer_amt=200" -X PATCH

#### Errors

    401 - if provided acc_no doesn't exist
    401 - if provided acc_no doesn't have sufficient balance

#### Future Work

What to work on given more time

1. mechanism to cache exchange rates for faster computation
2. Unit test coverage
3. private routes with authentication
4. More comprehensive validations - valid asset types
