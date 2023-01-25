import requests
from web3 import Web3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

etherscan_api_key = "UVGM9GGPHXP755SK9DKI3BED9EBA5RC16P"


def extract_event_data(event):
    tx_hash = event['transactionHash']
    # tx_hash = event['transactionHash'].hex()
    to = event['args']['to']
    # tx_from = event['args']['from']
    amount1In = event['args']['amount1In']
    amount0Out = event['args']['amount0Out']
    sender = event['args']['sender']
    address = event['address']

    amount1InEthUnits = Web3.fromWei(amount1In, 'ether')
    amount0OutEthUnits = Web3.fromWei(amount0Out, 'ether')

    return tx_hash, to, amount1In, amount0Out, sender, address, amount1InEthUnits, amount0OutEthUnits


def get_token_price_and_volume(token_address: str):
    response = requests.get(
        "https://api.dexscreener.com/latest/dex/tokens/" + token_address)
    data = response.json()
    volume_24h = 0
    token_price = 0

    if data['pairs']:
        volume_24h = data['pairs'][0]['volume']['h24']
        token_price = data['pairs'][0]['priceUsd']

    return token_price, volume_24h


def get_token_holders_supply_name(token_address: str):
    response = requests.get(
        "https://api.ethplorer.io/getTokenInfo/" + token_address + "?apiKey=freekey")
    data = response.json()
    # print(data)
    token_holders = data['holdersCount']
    total_supply = data['totalSupply']
    token_name = data['name']

    return token_holders, total_supply, token_name


def get_token_dead_balance(token_address: str):
    response = requests.get("https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=" +
                            token_address+"&address=0x000000000000000000000000000000000000dEaD&tag=latest&apikey=" + etherscan_api_key)
    data = response.json()

    return data['result']


def get_token_balance(token_address: str, wallet_address: str):
    response = requests.get("https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=" +
                            token_address+"&address="+wallet_address+"&tag=latest&apikey=" + etherscan_api_key)
    data = response.json()
    return data['result']


def get_token_taxes(token_address: str):
    response = requests.get(
        "https://aywt3wreda.execute-api.eu-west-1.amazonaws.com/default/IsHoneypot?chain=eth&token=" + token_address)
    data = response.json()
    buy_tax = data['BuyTax']
    sell_tax = data['SellTax']

    return buy_tax, sell_tax


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
            InlineKeyboardButton("▫️ UR AD HERE ▫️", callback_data="1"),
            InlineKeyboardButton(
                "▫️ GET BOOP ▫️", callback_data="2"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


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

    if is_new_holder:
        message += "✅ *New Holder!*\n"
    else:
        message += "❌ *Not New Holder!*\n"

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
