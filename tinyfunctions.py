# %%
from iroha import Iroha, IrohaCrypto, IrohaGrpc
from iroha.primitive_pb2 import *
import ed25519


net = IrohaGrpc('localhost:50051')
admin = Iroha("admin@test")


def get_keypair(account_id):
    signing_key = open(f"{account_id}.prib","rb").read()
    verifying_key = open(f"{account_id}.pub","rb").read()
    return signing_key, verifying_key
ADMIN_KEY = "f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70"


# %%
def create_domain(domain):
    if domain == None:
        return None
    cmds = [
        admin.command("CreateDomain", domain_id=domain, default_role="admin")
    ]

    tx = admin.transaction(cmds,creator_account="admin@test")
    IrohaCrypto.sign_transaction(tx, "f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70")
    net.send_tx(tx)
    for status in net.tx_status_stream(tx):
        print(status)
        print("\n")
    return tx

# %%
def create_asset(asset):
    if asset == None:
        return None
    cmds = [
        admin.command("CreateAsset", asset_name=asset, domain_id="chain", precision=0)
    ]

    tx = admin.transaction(cmds)
    IrohaCrypto.sign_transaction(tx, "f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70")
    net.send_tx(tx)
    for status in net.tx_status_stream(tx):
        print(status)
        print("\n")
    return tx

# %%
def add_asset_quantity(asset_name,amount):
    cmds = [
        admin.command("AddAssetQuantity", asset_id=f"{asset_name}#chain", amount=f"{amount}")
    ]

    tx = admin.transaction(cmds)
    IrohaCrypto.sign_transaction(tx, "f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70")
    net.send_tx(tx)
    for status in net.tx_status_stream(tx):
        print(status)
        print("\n")
    return tx

# %%
def account_assets(account_id):
    query = admin.query('GetAccountAssets', account_id=account_id)
    IrohaCrypto.sign_query(query, "f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70")

    response = net.send_query(query)
    data = response.account_assets_response.account_assets
    for asset in data:
        print('Asset id = {}, balance = {}'.format(
            asset.asset_id, asset.balance))
        print("\n")

# %%
def create_account(account_name):
# Creating a key pair
   signing_key, verifying_key = ed25519.create_keypair()

   # Save the created key pair
   open("iroha@test.prib","wb").write(signing_key.to_ascii(encoding="hex"))
   open("iroha@test.pub","wb").write(verifying_key.to_ascii(encoding="hex"))

   # Convert from binary to hexadecimal
   vkey_hex = verifying_key.to_ascii(encoding="hex")

   # Creating a Transaction
   transfer_tx = admin.transaction(
   [admin.command(
      'CreateAccount',
      account_name = account_name,
      domain_id = 'test',
      public_key = vkey_hex
   )]
   )

   # Transaction signature
   IrohaCrypto.sign_transaction(transfer_tx,ADMIN_KEY)

   # Send Transaction
   net.send_tx(transfer_tx)

   # Check the result
   for status in net.tx_status_stream(transfer_tx):
      print(status)
      print("\n")

# %%
def transfer_assets(account_id, dest_account_id, asset_id, amount):
    cmds = [
        admin.command('TransferAsset', src_account_id=account_id, dest_account_id=dest_account_id, asset_id=asset_id, amount=amount)
    ]

    tx = admin.transaction(cmds)
    IrohaCrypto.sign_transaction(tx, "f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70")
    net.send_tx(tx)
    for status in net.tx_status_stream(tx):
        print(status)
        print("\n")
    return tx

# %%
def GetSignatories(account_id):
    query = admin.query('GetSignatories', account_id=account_id)
    IrohaCrypto.sign_query(query, "f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70")
    response = net.send_query(query)
    print(f'Account Signatories\n{response}')

# %%



