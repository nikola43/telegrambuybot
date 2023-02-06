import json
import os
import requests
from web3 import Web3
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from moralis import evm_api
from urllib.parse import urlparse
from telegram import Update
from functools import wraps


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except ValueError:
        return False


def extract_event_data(event, decimals):
    #tx_hash = event['transactionHash']
    tx_hash = event['transactionHash'].hex()
    to = event['args']['to']
    # tx_from = event['args']['from']
    amount1In = event['args']['amount1In']
    amount0Out = event['args']['amount0Out']
    #sender = event['args']['sender']
    address = event['address']
    amount1InEthUnits = Web3.fromWei(amount1In, 'ether')
    amount0OutEthUnits = convert_wei_to_eth(amount0Out, decimals)

    print("tx_hash: ", tx_hash)
    print("to: ", to)
    #print("amount1In: ", amount1In)
    print("amount0Out: ", amount0Out)
    #print("sender: ", sender)
    print("address: ", address)
    print("amount1InEthUnits: ", amount1InEthUnits)
    print("amount0OutEthUnits: ", amount0OutEthUnits)

    return tx_hash, to, amount0Out, address, amount1InEthUnits, amount0OutEthUnits


def get_token_info(api_key, token_address):
    params = {
        "addresses": [token_address],
        "chain": "eth",
    }

    result = evm_api.token.get_token_metadata(
        api_key=api_key,
        params=params,
    )

    print("result: ", result)

    return {
        "name": result[0]['name'],
        "symbol": result[0]['symbol'],
        "decimals": result[0]['decimals'],
    }


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


async def get_token_price_and_volume_and_mc(token_address: str):
    volume_24h = None
    token_price = None
    market_cap = None

    response = requests.get(
        "https://api.dexscreener.com/latest/dex/tokens/" + token_address)

    if response is not None:
        data = response.json()
        if data['pairs']:
            volume_24h = data['pairs'][0]['volume']['h24']
            token_price = data['pairs'][0]['priceUsd']
            market_cap = data['pairs'][0]['fdv']

    return token_price, volume_24h, market_cap


async def get_token_holders_supply_name(token_address: str):
    token_holders = None
    total_supply = None
    token_name = None

    response = requests.get(
        "https://api.ethplorer.io/getTokenInfo/" + token_address + "?apiKey=freekey")

    if response is not None:
        data = response.json()
        token_holders = data['holdersCount']
        total_supply = data['totalSupply']
        token_name = data['name']

    return token_holders, total_supply, token_name


async def get_token_dead_balance(etherscan_api_key: str, token_address: str):
    response = requests.get("https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=" +
                            token_address+"&address=0x000000000000000000000000000000000000dEaD&tag=latest&apikey=" + etherscan_api_key)

    if response is not None:
        data = response.json()
        return data['result']

    return None


async def get_token_balance(etherscan_api_key: str, token_address: str, wallet_address: str):
    response = requests.get("https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=" +
                            token_address+"&address="+wallet_address+"&tag=latest&apikey=" + etherscan_api_key)
    if response is not None:
        data = response.json()
        return data['result']

    return None


async def get_token_taxes(token_address: str):
    buy_tax = None
    sell_tax = None

    response = requests.get(
        "https://aywt3wreda.execute-api.eu-west-1.amazonaws.com/default/IsHoneypot?chain=eth&token=" + token_address)

    if response is not None:
        data = response.json()
        buy_tax = data['BuyTax']
        sell_tax = data['SellTax']

    return buy_tax, sell_tax


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


async def get_pair_addressV2(token_address):

    pair_address = None

    response = requests.get(
        "https://api.dexscreener.com/latest/dex/tokens/" + token_address)

    if response is not None:
        data = response.json()
        if data['pairs']:
            pair_address = data['pairs'][0]['pairAddress']

    return pair_address


def calc_circulating_supply(total_supply: str, dead_wallet_balance: str):
    return Web3.fromWei(
        float(total_supply) - float(dead_wallet_balance), 'ether')


def calc_market_cap(price: str, circulating_supply: str):
    return float(price) * float(circulating_supply)


def create_emoji_text(tx_amount1InEthUnits: str, emoji_char: str):
    emoji_text = ""
    emoji_icon = emoji_char
    emoji_value = 0.01
    emoji_count = int(float(tx_amount1InEthUnits) / emoji_value)

    # add one emoji for every 0.01 eth
    for x in range(emoji_count):
        emoji_text += emoji_icon
    return emoji_text


def escape_markdown(message):
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
    return message


def create_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("▫️ advertiser ▫️", callback_data="1")
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def is_valid_token_address(web3, token_address: str) -> bool:
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


def create_message(user_config, tx_hash, to, amount1InEthUnits, amount0OutEthUnits, token_price, volume_24h, token_holders, token_name, buy_tax, sell_tax, is_new_holder, market_cap):
    emoji_text = create_emoji_text(amount1InEthUnits, user_config['emoji'])

    message = ""

    message += "*" + token_name + " Buy!*\n"
    message += emoji_text + "\n\n"
    message += "💠  *" + str(float("{:,.2f}".format(float(amount1InEthUnits)))) + " ETH $" + str(
        "{:,.0f}".format(float(token_price) * float(amount0OutEthUnits))) + "*\n"

    message += "🧩  *" + \
        str("{:,.0f}".format(float(amount0OutEthUnits))) + \
        " " + token_name + "*\n"

    message += "💵 *$" + \
        str("{:,.8f}".format(float(token_price))) + "*\n"

    # if is_new_holder:
    #    message += "✅ *New Holder!*\n"
    # else:
    #    message += "❌ *Not New Holder!*\n"

    message += "📂 *[Address](https://etherscan.io/address/" + to + ")*" + \
        " | *[TX](https://etherscan.io/tx/" + tx_hash + ")*" + "\n"

    message += "\n"

    message += "🔘 *Market Cap $" + \
        str("{:,.0f}".format(float(market_cap))) + "*\n"

    message += "⭐️ *24h Volume $" + \
        str("{:,.0f}".format(float(volume_24h))) + "*\n"
    message += "🧸 *[Holders](https://etherscan.io/token/tokenholderchart/" + \
        user_config['token_address'] + ") " + str(token_holders) + "*\n"

    message += "🔪 *Taxes B/S | " + \
        str(buy_tax) + "/" + str(sell_tax) + "*\n"

    message += "\n"

    message += "*[Chart](https://www.dextools.io/app/en/ether/pair-explorer/" + user_config['pair_address'] + ")*" + " ▫️ *[Buy](https://app.uniswap.org/#/swap?outputCurrency=" + \
        user_config['token_address'] + ")*\n"

    message += "*[Website](" + user_config['websiteurl'] + ")* ▫️ *[Twitter](" + \
        user_config['twitterurl'] + \
        ")* ▫️ *[Telegram](" + user_config['telegramurl'] + ")*\n"

    # escape markdown characters
    message = escape_markdown(message)
    return message

# function for convert wei to eth with decimals


def convert_wei_to_eth(wei, decimals):
    return float(wei) / 10 ** decimals


def check_user_has_config():
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if check_user(update.effective_user.id):
                await func(update, context)
            else:
                await update.message.reply_text("You don't have a config yet. Please use /address to set your token address.")
        return wrapper
    return decorator


def check_user(user_id) -> bool:
    users_configs = read_json_file("users_configs.json")

    # loop through the users_configs and find the config for the current user
    for user_config in users_configs:
        if user_config['user_id'] == user_id:
            return True

    return False


async def is_admin(update: Update) -> bool:
    chat_member = await update.effective_chat.get_member(update.effective_user.id)
    return chat_member.status in ("administrator", "creator")


def is_bot_chat(bot_chat_id):
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if update.effective_chat.id != bot_chat_id:
                await func(update, context)
            else:
                await update.message.reply_text("You can't use this command in the bot chat. Please add the bot to your group and use the command there.")
        return wrapper
    return decorator


def admin_only():
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if await is_admin(update):
                await func(update, context)
            else:
                await update.message.reply_text("You are not an admin.")
        return wrapper
    return decorator
