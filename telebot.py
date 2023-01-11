from urllib.parse import urlparse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import json
from web3 import Web3
import asyncio
from moralis import evm_api
import requests


# add your blockchain connection information
infura_url = 'https://mainnet.infura.io/v3/d39a866f4f6d49b9916f9269bf880110'
web3 = Web3(Web3.HTTPProvider(infura_url))
moralis_api_key = "LJ2liXqSHdL6XOad7XhWqTP30Wi0mIIqSf1RDnemTPXYwKFm5L3Ux9WeaxTFCpxB"
etherscan_api_key = "UVGM9GGPHXP755SK9DKI3BED9EBA5RC16P"

pair_address = None
uniswap_pair_abi = json.loads('[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

# create dict for store the users id and the task id
users_tasks = {}

# define function to handle events and print to the console


async def handle_event(event, contract, update: Update, user_config):
    # print(Web3.toJSON(event))
    # print()

    print("New Buy!")
    router_addess = "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45"

    tx_hash = event['transactionHash']
    # tx_hash = event['transactionHash'].hex()
    tx_to = event['args']['to']
    # tx_from = event['args']['from']
    tx_amount1In = event['args']['amount1In']
    tx_amount0Out = event['args']['amount0Out']
    tx_from = event['args']['sender']

    # check if to address is the router address
    if tx_to != router_addess:
        # print("tx_hash: " + tx_hash)
        # print("tx_to: " + tx_to)
        # print("tx_amount0In: " + str(tx_amount0In))
        # print("tx_amount1Out: " + str(tx_amount1Out))

        # convert tx_amount1Out to eth value
        tx_amount1InEthUnits = web3.fromWei(tx_amount1In, 'ether')
        tx_amount0OutEthUnits = web3.fromWei(tx_amount0Out, 'ether')
        # print("tx_amount0InEthUnits: " + str(tx_amount0InEthUnits))
        # print("tx_amount1OutEthUnits: " + str(tx_amount1OutEthUnits))

        # token_price = get_token_price(moralis_api_key, token_address)
        # print(token_price)

        # convert tx_amount1Out to usd value

        emoji_text = ""
        emoji_icon = user_config['emoji']
        emoji_value = 0.01
        emoji_count = int(float(tx_amount1InEthUnits) / emoji_value)

        # add one emoji for every 0.01 eth
        for x in range(emoji_count):
            emoji_text += emoji_icon

        # get 24 hour volume from https://api.dexscreener.com/latest/dex/tokens/
        response = requests.get(
            "https://api.dexscreener.com/latest/dex/tokens/" + user_config['token_address'])
        data = response.json()
        volume_24h = data['pairs'][0]['volume']['h24']
        token_price = data['pairs'][0]['priceUsd']

        # get token holders
        response = requests.get(
            "https://api.ethplorer.io/getTokenInfo/" + user_config['token_address'] + "?apiKey=freekey")
        data = response.json()
        # print(data)
        token_holders = data['holdersCount']
        total_supply = data['totalSupply']
        token_name = data['name']

        # Get ERC20-Token Account Balance for TokenContractAddress
        response = requests.get("https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=" +
                                user_config['token_address']+"&address=0x000000000000000000000000000000000000dEaD&tag=latest&apikey=" + etherscan_api_key)
        data = response.json()
        dead_wallet_balance = data['result']

        # calc market cap. total supply - dead wallet balance
        circulating_supply = web3.fromWei(
            float(total_supply) - float(dead_wallet_balance), 'ether')

        market_cap = float(circulating_supply) * float(token_price)

        # get token buy sell taxes
        response = requests.get(
            "https://aywt3wreda.execute-api.eu-west-1.amazonaws.com/default/IsHoneypot?chain=eth&token=" + user_config['token_address'])
        data = response.json()
        buy_tax = data['BuyTax']
        sell_tax = data['SellTax']

        message = ""

        # add link to etherscan using markdown
        # add gif to message
        # set bold for token name

        message += "*" + token_name + " Buy!*\n"
        message += emoji_text + "\n\n"
        message += "💵  *" + str(float("{:,.2f}".format(float(tx_amount1InEthUnits)))) + " ETH " +\
            str(float("{:,.2f}".format(float(token_price) *
                float(tx_amount0OutEthUnits)))) + "USD*\n"

        message += "🪙  *" + \
            str("{:,.2f}".format(float(tx_amount0OutEthUnits))) + "Tokens*\n"

        message += "⚪️ *Price: " + \
            str("{:,.8f}".format(float(token_price))) + "*\n"
        message += "🔘 *Market Cap: $" + \
            str("{:,.2f}".format(float(market_cap))) + "*\n"
        message += "\n"

        message += "🛳 *Volume 24h: $" + \
            str("{:,.2f}".format(float(volume_24h))) + "*\n"
        message += "🔫 *Taxes B/S | " + \
            str(buy_tax) + "/" + str(sell_tax) + "%*\n"

        message += "🧸 *Holder count: " + str(token_holders) + "*\n"

        message += "🪪 [TX](https://etherscan.io/tx/" + tx_hash + ")" + \
            " | [Address](https://etherscan.io/address/" + tx_from + ")\n"
        message += "📊 [Explorer](https://www.dextools.io/app/en/ether/pair-explorer/" + \
            contract.address + ")\n"
        message += "🗳 [Buy](https://app.uniswap.org/#/swap?outputCurrency=" + \
            user_config['token_address'] + ")\n"
        message += "[Website](" + user_config['websiteurl'] + ")\n"
        message += "[Twitter](" + user_config['twitterurl'] + ")\n"
        message += "[Telegram](" + user_config['telegramurl'] + ")\n"

        # escape markdown characters
        message = message.replace("_", "\_")
        message = message.replace("`", "\`")
        message = message.replace(".", "\.")
        message = message.replace("%", "\%")
        message = message.replace("-", "\-")
        message = message.replace("+", "\+")
        message = message.replace("#", "\#")
        message = message.replace("=", "\=")
        message = message.replace("|", "\|")
        message = message.replace("!", "\!")

        print(message)
        print()

        # send message to chat id
        # await update.effective_chat.send_message(message)

        """Sends a message with three inline buttons attached."""
        keyboard = [
            [
                InlineKeyboardButton("▫️ YOUR AD HERE ▫️", callback_data="1"),
                InlineKeyboardButton(
                    "▫️ INSTALL BOOP BOT ▫️", callback_data="2"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # send video file to chat id
        # get video file input from local file system
        video = open('boop.mp4', 'rb')
        # send video to chat id
        await update.effective_chat.send_video(video, caption=message, parse_mode="MarkdownV2", reply_markup=reply_markup)


async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    users_configs = read_json_file("users_configs.json")

    local_user_config = None

    # loop through the users_configs and find the config for the current user
    for user_config in users_configs:
        if user_config['user_id'] == update.effective_user.id:
            local_user_config = user_config
            local_user_config['token_address'] = web3.toChecksumAddress(
                local_user_config['token_address'])
            local_user_config['pair_address'] = web3.toChecksumAddress(
                local_user_config['pair_address'])

    print(local_user_config)

    contract = web3.eth.contract(
        address=local_user_config['pair_address'], abi=uniswap_pair_abi)

    event = {"args": {"sender": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45", "to": "0x5607f96D4f0088833a10377F7f43eb19bc24B171", "amount0In": 0, "amount1In": 575000000000000000, "amount0Out": 3428621956017115909243531, "amount1Out": 0}, "event": "Swap", "logIndex": 283,
             "transactionIndex": 143, "transactionHash": "0x9505889816f9432ed314d6942804e7b5da889b9fa87139210244da68ad3074de", "address": "0x4674D4a748f787e5Cb81e73290d1B96A1a788EFC", "blockHash": "0x7f93eecb33d5e17f3577fd0917e0b929eb58ed5589a3463a7ef4f68915812d59", "blockNumber": 16378312}
    await handle_event(event, contract, update, local_user_config)

    # await update.effective_chat.send_message("[TX](https://etherscan.io/tx/" + "tx_hash" + ")\n", parse_mode="MarkdownV2")


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
        "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # USDC
        "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT
        "0x6B175474E89094C44Da98b954EedeAC495271d0F",  # DAI
    ]

    for token in tokens:
        params = {
            "exchange": "uniswapv2",
            "token0_address": token_address,
            "token1_address": token,
            "chain": "eth",
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


async def run_buybot(contract, update: Update, user_config):
    event_filter = contract.events.Swap.createFilter(fromBlock='latest')
    print("Starting buybot...")
    while True:
        for Swap in event_filter.get_new_entries():
            await handle_event(Swap, contract, update, user_config)
        await asyncio.sleep(2)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def buybot_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Descriptiom of the buybot')


async def start_buybot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # read the users_configs.json file into the users_configs variable
    users_configs = read_json_file("users_configs.json")

    local_user_config = None

    # loop through the users_configs and find the config for the current user
    for user_config in users_configs:
        if user_config['user_id'] == update.effective_user.id:
            local_user_config = user_config
            local_user_config['token_address'] = web3.toChecksumAddress(
                local_user_config['token_address'])
            local_user_config['pair_address'] = web3.toChecksumAddress(
                local_user_config['pair_address'])

    # check if the user has a config
    if local_user_config['user_id'] == None:
        await update.message.reply_text(f'Please set the token address first.')
        return

    # check if the token address is valid
    if not is_valid_token_address(local_user_config['token_address']):
        await update.message.reply_text(f'The token address is not valid.')
        return

    print("Token address: ", local_user_config['token_address'])
    print("Pair address: ", pair_address)

    contract = web3.eth.contract(address=pair_address, abi=uniswap_pair_abi)

    # run the run_buybot function on a new thread
    users_tasks[update.effective_user.id] = asyncio.create_task(
        run_buybot(contract, update, local_user_config))

    await update.message.reply_text(f'Starting buybot...')


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except ValueError:
        return False


async def buybotconfigif2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # print(update.message)

    # get file id from the message
    video = update.message.video
    # print(video)

    # download the file
    file = await context.bot.get_file(video.file_id)
    # get caption
    caption = update.message.caption
    print(caption)

    # get the file name
    file_name = video.file_name
    print(file_name)
    # save the file
    await file.download_to_drive(file_name)


async def stop_buybot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    task = users_tasks[update.effective_user.id]

    # check if the run_buybot_task is running
    if task == None:
        await update.message.reply_text(f'Buybot is not running.')
        return

    # cancel the run_buybot_task
    task.cancel()
    await update.message.reply_text(f'Stopping buybot...')


async def buybot_configtelegramurl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # extract the command arguments
    args = context.args

    # check if the user sent a parameter
    if not args:
        await update.message.reply_text("You didn't specify telegram group url.")
        return

    # check if is valid url
    if not is_valid_url(args[0]):
        await update.message.reply_text("The url is not valid.")
        return

    users_configs = read_json_file("users_configs.json")

    # check if the user already has a config
    for user_config in users_configs:
        if user_config["user_id"] == update.effective_user.id:
            # update the emoji
            user_config["telegramurl"] = args[0]
            await update.message.reply_text("Telegram url updated.")
            # write the users_configs variable to the users_configs.json file
            with open('users_configs.json', 'w') as outfile:
                json.dump(users_configs, outfile)
            return


async def buybot_configtwitterurl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # extract the command arguments
    args = context.args

    # check if the user sent a parameter
    if not args:
        await update.message.reply_text("You didn't specify twitter url.")
        return

    # check if is valid url
    if not is_valid_url(args[0]):
        await update.message.reply_text("The url is not valid.")
        return

    users_configs = read_json_file("users_configs.json")

    # check if the user already has a config
    for user_config in users_configs:
        if user_config["user_id"] == update.effective_user.id:
            # update the emoji
            user_config["twitterurl"] = args[0]
            await update.message.reply_text("Twitter url updated.")
            # write the users_configs variable to the users_configs.json file
            with open('users_configs.json', 'w') as outfile:
                json.dump(users_configs, outfile)
            return


async def buybot_configwebsiteurl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # extract the command arguments
    args = context.args

    # check if the user sent a parameter
    if not args:
        await update.message.reply_text("You didn't specify website url.")
        return

    # check if is valid url
    if not is_valid_url(args[0]):
        await update.message.reply_text("The url is not valid.")
        return

    users_configs = read_json_file("users_configs.json")

    # check if the user already has a config
    for user_config in users_configs:
        if user_config["user_id"] == update.effective_user.id:
            # update the emoji
            user_config["websiteurl"] = args[0]
            await update.message.reply_text("Website url updated.")
            # write the users_configs variable to the users_configs.json file
            with open('users_configs.json', 'w') as outfile:
                json.dump(users_configs, outfile)
            return


async def buybot_configemoji(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # extract the command arguments
    args = context.args

    # check if the user sent a parameter
    if not args:
        await update.message.reply_text("You didn't specify emoji.")
        return

    # check the emoji length
    if len(args[0]) > 1:
        await update.message.reply_text("Invalid emoji.")
        return

    users_configs = read_json_file("users_configs.json")

    # check if the user already has a config
    for user_config in users_configs:
        if user_config["user_id"] == update.effective_user.id:
            # update the emoji
            user_config["emoji"] = args[0]
            await update.message.reply_text("Emoji updated.")
            # write the users_configs variable to the users_configs.json file
            with open('users_configs.json', 'w') as outfile:
                json.dump(users_configs, outfile)
            return


async def buybot_configaddress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    pair_address = get_pair_address(moralis_api_key, args[0])

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


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await update.effective_chat.send_message(text=f"Selected option: {query.data}")
    # await query.edit_message_text(text=f"Selected option: {query.data}")

    if query.data == "2":
        # open new chat with chat id 358896373
        await context.bot.send_message(chat_id=358896373, text="/start")


if __name__ == "__main__":
    app = ApplicationBuilder().token(
        "5829617229:AAHHqca1eu2PG3FS-bXATVEptV2Y9ky4H-M").build()

    app.add_handler(CommandHandler("test", send_message))
    app.add_handler(CommandHandler(
        "address", buybot_configaddress))
    app.add_handler(CommandHandler("emoji", buybot_configemoji))
    app.add_handler(CommandHandler(
        "website", buybot_configwebsiteurl))
    app.add_handler(CommandHandler(
        "telegram", buybot_configtelegramurl))
    app.add_handler(CommandHandler(
        "twitter", buybot_configtwitterurl))
    # app.add_handler(CommandHandler("buybotconfigif", buybotconfigif))
    app.add_handler(CommandHandler("start", start_buybot))
    app.add_handler(CommandHandler("stop", stop_buybot))
    app.add_handler(MessageHandler(filters.VIDEO, buybotconfigif2))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler("description", buybot_description))

    app.run_polling()
