from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
from web3 import Web3
import asyncio
from moralis import evm_api

# add your blockchain connection information
infura_url = 'https://goerli.infura.io/v3/d39a866f4f6d49b9916f9269bf880110'
web3 = Web3(Web3.HTTPProvider(infura_url))
moralis_api_key = "LJ2liXqSHdL6XOad7XhWqTP30Wi0mIIqSf1RDnemTPXYwKFm5L3Ux9WeaxTFCpxB"

pair_address = None
uniswap_pair_abi = json.loads('[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

# create dict for store the users id and the task id
users_tasks = {}

# define function to handle events and print to the console


async def handle_event(event, token_address, update: Update, chat_id):
    # print(Web3.toJSON(event))
    # print()

    print("New Buy!")

    tx_hash = event['transactionHash'].hex()
    tx_to = event['args']['to']
    tx_amount0In = event['args']['amount0In']
    tx_amount1Out = event['args']['amount1Out']

    # print("tx_hash: " + tx_hash)
    # print("tx_to: " + tx_to)
    # print("tx_amount0In: " + str(tx_amount0In))
    # print("tx_amount1Out: " + str(tx_amount1Out))

    # convert tx_amount1Out to eth value
    tx_amount0InEthUnits = web3.fromWei(tx_amount0In, 'ether')
    tx_amount1OutEthUnits = web3.fromWei(tx_amount1Out, 'ether')
    # print("tx_amount0InEthUnits: " + str(tx_amount0InEthUnits))
    # print("tx_amount1OutEthUnits: " + str(tx_amount1OutEthUnits))

    token_price = "1"  # get_token_price(moralis_api_key, token_address)
    # print(token_price)

    # convert tx_amount1Out to usd value

    emoji_text = ""
    emoji_icon = "⚪️"
    emoji_value = 0.001
    emoji_count = int(float(tx_amount0InEthUnits) / emoji_value)

    # add one emoji for every 0.01 eth
    for x in range(emoji_count):
        emoji_text += emoji_icon

    message = "New Buy!\n"
    message += emoji_text + "\n"
    message += "Spend: " + \
        str(float("{:.2f}".format(float(token_price) *
            float(tx_amount1OutEthUnits)))) + " USD\n"
    message += "Receive: " + \
        str(float("{:.2f}".format(float(tx_amount1OutEthUnits)))) + " Tokens\n"
    message += "Price: " + \
        str(float("{:.8f}".format(float(token_price)))) + " USD\n"
    message += "Tx Hash: " + tx_hash + "\n"

    print(message)
    print()

    # send message to chat id
    # await update.effective_chat.send_message(message)

    # send video file to chat id
    # get video file input from local file system
    video = open('boop.mp4', 'rb')
    # send video to chat id
    await update.effective_chat.send_video(video, caption=message)
    


async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_message("Hello World!")


def get_token_price(api_key, token_address):
    params = {
        "address": token_address,
        "chain": "eth"
    }

    result = evm_api.token.get_token_price(
        api_key=api_key,
        params=params,
    )
    return result['usdPrice']

# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval


def is_valid_token_address(token_address: str) -> bool:
    """
    Check if the token address is valid.
    """
    try:
        # check if the token address is valid
        if not Web3.isAddress(token_address):
            return False

        # check if the token address is a contract
        if not web3.eth.getCode(token_address):
            return False

        return True
    except Exception as e:
        print(e)
        return False


def read_json_file(file_name):
    with open(file_name, 'r') as f:
        return json.load(f)


def get_pair_address(api_key, token_address):

    # testnet 0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6
    #  mainnet 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2

    tokens = [
        "0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6",
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # USDC
        "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT
        "0x6B175474E89094C44Da98b954EedeAC495271d0F",  # DAI
    ]

    for token in tokens:
        params = {
            "exchange": "uniswapv2",
            "token0_address": token_address,
            "token1_address": token,
            "chain": "goerli",
        }

        result = evm_api.defi.get_pair_address(
            api_key=api_key,
            params=params,
        )

        if result['pairAddress']:
            return result['pairAddress']

    return None


def get_token_info(api_key, token_address):
    params = {
        "addresses": [token_address],
        "chain": "eth",
    }

    result = evm_api.token.get_token_metadata(
        api_key=api_key,
        params=params,
    )

    return {
        "name": result[0]['name'],
        "symbol": result[0]['symbol'],
    }

# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds


async def run_buybot(contract, token_address, update: Update, chat_id):
    event_filter = contract.events.Swap.createFilter(fromBlock='latest')
    print("Starting buybot...")
    while True:
        for Swap in event_filter.get_new_entries():
            await handle_event(Swap, token_address, update, chat_id)
        await asyncio.sleep(2)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def start_buybot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # read the users_configs.json file into the users_configs variable
    users_configs = read_json_file("users_configs.json")

    user_id = None
    token_address = None
    pair_address = None
    chat_id = None

    # loop through the users_configs and find the config for the current user
    for user_config in users_configs:
        if user_config['user_id'] == update.effective_user.id:
            # extract the token address from the config
            token_address = web3.toChecksumAddress(
                user_config['token_address'])
            pair_address = web3.toChecksumAddress(user_config['pair_address'])
            user_id = user_config['user_id']
            chat_id = user_config['chat_id']

    # check if the user has a config
    if user_id == None:
        await update.message.reply_text(f'Please set the token address first.')
        return

    # check if the token address is valid
    if not is_valid_token_address(token_address):
        await update.message.reply_text(f'The token address is not valid.')
        return

    print("Token address: ", token_address)
    print("Pair address: ", pair_address)

    contract = web3.eth.contract(address=pair_address, abi=uniswap_pair_abi)

    # run the run_buybot function on a new thread
    users_tasks[update.effective_user.id] = asyncio.create_task(
        run_buybot(contract, pair_address, update, chat_id))

    await update.message.reply_text(f'Starting buybot...')


async def stop_buybot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    task = users_tasks[update.effective_user.id]

    # check if the run_buybot_task is running
    if task == None:
        await update.message.reply_text(f'Buybot is not running.')
        return

    # cancel the run_buybot_task
    task.cancel()
    await update.message.reply_text(f'Stopping buybot...')


async def buybot_config(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # extract the command arguments
    args = context.args

    # check if the user sent a parameter
    if not args:
        await update.message.reply_text("You didn't specify token address.")
        return

    # validate the token address
    if not is_valid_token_address(args[0]):
        await update.message.reply_text("Invalid token address.")
        return

    users_configs = []

    # check if the user already has a config
    for user_config in users_configs:
        if user_config["user_id"] == update.effective_user.id:
            await update.message.reply_text("You already have a config.")
            return

    # get_pair_address(moralis_api_key, args[0])
    pair_address = "0xbFa9244c2Ada020C0d197cf076e7CDC530905f14"

    # get chat id from the update
    chat_id = update.effective_chat.id

    # append the user id and token address to users_configs array
    users_configs.append({
        "user_id": update.effective_user.id,
        "token_address": web3.toChecksumAddress(args[0]),
        "pair_address": pair_address,
        "chat_id": chat_id,
    })

    # save the users_configs array to a json file
    with open('users_configs.json', 'w') as outfile:
        json.dump(users_configs, outfile)

    token_info = get_token_info(moralis_api_key, args[0])

    message = "Selected token:\n"
    message = f"Token name: {token_info['name']}\n"
    message += f"Token symbol: {token_info['symbol']}\n"
    message += f"Pair address: {pair_address}\n"

    # send the message back
    await update.message.reply_text(message)

if __name__ == "__main__":
    app = ApplicationBuilder().token(
        "5829617229:AAHHqca1eu2PG3FS-bXATVEptV2Y9ky4H-M").build()

    app.add_handler(CommandHandler("hello", send_message))
    app.add_handler(CommandHandler("buybotconfig", buybot_config))
    app.add_handler(CommandHandler("buybotstart", start_buybot))
    app.add_handler(CommandHandler("buybotstop", stop_buybot))

    app.run_polling()
