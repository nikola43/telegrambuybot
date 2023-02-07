
import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import json
from web3 import Web3
import asyncio
import requests
from utils import admin_only, check_user_has_config, extract_event_data, get_token_price_and_volume_and_mc, get_token_holders_supply_name, get_token_dead_balance, get_token_balance, get_token_taxes, calc_circulating_supply, calc_market_cap, create_emoji_text, create_message, create_keyboard, is_bot_chat, is_valid_token_address, read_json_file, get_pair_addressV2, get_token_info, is_valid_url
from revChatGPT.ChatGPT import Chatbot
from gtts import gTTS
from functools import wraps
from dotenv import load_dotenv

# Replace YOUR_API_KEY with your OpenAI API key
moralis_api_key = None
etherscan_api_key = None
infura_api_key = None
chatGPT_token = None
telegram_token = None

# add your blockchain connection information
infura_url = None
web3 = None

bot_chat_id = 358896373

# add your uniswap router address
routerV2_addess = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
routerV3_addess = "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45"
uniswap_pair_abi = json.loads('[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
uniswap_router_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_factoryV2","type":"address"},{"internalType":"address","name":"factoryV3","type":"address"},{"internalType":"address","name":"_positionManager","type":"address"},{"internalType":"address","name":"_WETH9","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH9","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"approveMax","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"approveMaxMinusOne","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"approveZeroThenMax","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"approveZeroThenMaxMinusOne","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes","name":"data","type":"bytes"}],"name":"callPositionManager","outputs":[{"internalType":"bytes","name":"result","type":"bytes"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"paths","type":"bytes[]"},{"internalType":"uint128[]","name":"amounts","type":"uint128[]"},{"internalType":"uint24","name":"maximumTickDivergence","type":"uint24"},{"internalType":"uint32","name":"secondsAgo","type":"uint32"}],"name":"checkOracleSlippage","outputs":[],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"uint24","name":"maximumTickDivergence","type":"uint24"},{"internalType":"uint32","name":"secondsAgo","type":"uint32"}],"name":"checkOracleSlippage","outputs":[],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"}],"internalType":"struct IV3SwapRouter.ExactInputParams","name":"params","type":"tuple"}],"name":"exactInput","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"internalType":"struct IV3SwapRouter.ExactInputSingleParams","name":"params","type":"tuple"}],"name":"exactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMaximum","type":"uint256"}],"internalType":"struct IV3SwapRouter.ExactOutputParams","name":"params","type":"tuple"}],"name":"exactOutput","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMaximum","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"internalType":"struct IV3SwapRouter.ExactOutputSingleParams","name":"params","type":"tuple"}],"name":"exactOutputSingle","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"factoryV2","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getApprovalType","outputs":[{"internalType":"enum IApproveAndCall.ApprovalType","name":"","type":"uint8"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"amount0Min","type":"uint256"},{"internalType":"uint256","name":"amount1Min","type":"uint256"}],"internalType":"struct IApproveAndCall.IncreaseLiquidityParams","name":"params","type":"tuple"}],"name":"increaseLiquidity","outputs":[{"internalType":"bytes","name":"result","type":"bytes"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickLower","type":"int24"},{"internalType":"int24","name":"tickUpper","type":"int24"},{"internalType":"uint256","name":"amount0Min","type":"uint256"},{"internalType":"uint256","name":"amount1Min","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"internalType":"struct IApproveAndCall.MintParams","name":"params","type":"tuple"}],"name":"mint","outputs":[{"internalType":"bytes","name":"result","type":"bytes"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"previousBlockhash","type":"bytes32"},{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"","type":"bytes[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"","type":"bytes[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"results","type":"bytes[]"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"positionManager","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"pull","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"refundETH","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowed","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowedIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"sweepToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"}],"name":"sweepToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"sweepTokenWithFee","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"sweepTokenWithFee","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"int256","name":"amount0Delta","type":"int256"},{"internalType":"int256","name":"amount1Delta","type":"int256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"uniswapV3SwapCallback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"unwrapWETH9","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"}],"name":"unwrapWETH9","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"unwrapWETH9WithFee","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"unwrapWETH9WithFee","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"}],"name":"wrapETH","outputs":[],"stateMutability":"payable","type":"function"},{"stateMutability":"payable","type":"receive"}]')

# create dict for store the users id and the task id
users_tasks = {}

# init the chatbot
# chatbot = Chatbot({
#   "session_token": chatGPT_token
# }, conversation_id=None, parent_id=None)  # You can start a custom conversation


async def handle_event(event, update: Update, user_config):
    print(Web3.toJSON(event))

    # extract event data
    tx_hash, to, amount1In, amount0Out, sender, address, amount1InEthUnits, amount0OutEthUnits = extract_event_data(
        event, user_config['decimals'])

    # check if to address is the router address
    is_buy_tx = to != routerV3_addess and to != routerV2_addess and address == user_config[
        'pair_address'] and amount1InEthUnits > 0.0 and amount0OutEthUnits > 0.0

    if is_buy_tx:
        print("New Buy!")

        # get 24 hour volume from https://api.dexscreener.com/latest/dex/tokens/
        token_price, volume_24h, market_cap = await get_token_price_and_volume_and_mc(
            user_config['token_address'])

        # get token holders
        token_holders, total_supply, token_name = await get_token_holders_supply_name(
            user_config['token_address'])

        # Get Token balance for wallet
        wallet_token_balance = await get_token_balance(
            etherscan_api_key,
            user_config['token_address'], to)

        # check if wallet_token_balance is equal to amount0Out
        is_new_holder = str(wallet_token_balance) == str(amount0Out)

        # get token buy sell taxes
        buy_tax, sell_tax = await get_token_taxes(user_config['token_address'])

        message = create_message(user_config, tx_hash, to, amount1InEthUnits, amount0OutEthUnits, token_price,
                                 volume_24h, token_holders, token_name, buy_tax, sell_tax, is_new_holder, str(market_cap))

        keyboard = [
            [
                InlineKeyboardButton("▫️ advertiser ▫️", callback_data="1")
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        print(message)
        print()

        # get video file input from local file system
        # send video to chat id
        video = open(user_config['gif'], 'rb')
        await update.effective_chat.send_video(video, caption=message, parse_mode="MarkdownV2", reply_markup=reply_markup)


async def setgif(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_chat.send_message("Please send me the gif you want to use for the buybot.")


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

    event = {"args": {"sender": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D", "to": "0xCc33Db5fEc8cb1393adD7318Ca99cb916547E1B5", "amount0In": 0, "amount1In": 753066405440747595, "amount0Out": 7147773969820848, "amount1Out": 0}, "event": "Swap", "logIndex": 42,
             "transactionIndex": 7, "transactionHash": "0x59eb920fc08c2cab52a4258be864e4989513f9be8bebf325187c12277fa385eb", "address": "0x5C9f4Eb96D4c111B5e667c0F0B63922CF91b8796", "blockHash": "0x6155bb1592b514ea1eda41053b699dd40fcde527cc919817e9a9951fa4641ed4", "blockNumber": 16576283}
    await handle_event(event, update, local_user_config)


async def run_buybot(contract, update: Update, user_config):
    event_filter = contract.events.Swap.createFilter(fromBlock='latest')
    print("Starting buybot...")
    while True:
        for Swap in event_filter.get_new_entries():
            await handle_event(Swap, update, user_config)
        await asyncio.sleep(2)


async def buybot_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    print("chat_id: " + str(chat_id))

    # create description of the buybot
    text = "\n◽️ Welcome to ai bot. ◽️" + "\n"
    text += "This is a list of all the things I'm capable of at the moment. " + "\n\n"
    text += "Please add me to your group first before using any of my commands." + "\n\n"
    text += "- Type /ai(TEXT) | to chat with ai chatbot" + "\n\n"
    text += "- Type /aivoice(TEXT) | to chat with ai chatbot and reply you with voice audio" + "\n\n"
    text += "- Type /price(CONTRACT ADDRESS) | to see token price and info" + "\n\n"
    text += "- Type /address(CONTRACT ADDRESS) | to track your coin" + "\n\n"
    text += "- Type /emoji(EMOJI) | to set a custom emoji" + "\n\n"
    text += "- Type /website(WEBSITE) | to set a custom website url" + "\n\n"
    text += "- Type /telegram(TELEGRAM) | to set a custom telegram url" + "\n\n"
    text += "- Type /twitter(TWITTER) | to set a custom twitter url" + "\n\n"
    text += "- Type /gif | while you send your mp4 file to set a custom gif" + "\n\n"
    text += "- Type /start | to start the bot" + "\n\n"
    text += "- Type /stop | to stop the bot" + "\n\n"
    text += "- Type /help | to show all commands" + "\n\n"
    text += "Click here for a tutorial on how to set me up"

    await update.message.reply_text(text)


async def call_get_price_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # extract the command arguments
    args = context.args

    # check if the user sent a parameter
    if not args:
        await update.message.reply_text("You didn't specify token address.")
        return

    # validate the token address
    if not is_valid_token_address(web3, Web3.toChecksumAddress(args[0])):
        await update.message.reply_text("Invalid token address.")
        return

    response = requests.get(
        "https://api.dexscreener.com/latest/dex/tokens/" + args[0])
    data = response.json()
    token_info = {
        "name": data['pairs'][0]['baseToken']['name'],
        "symbol": data['pairs'][0]['baseToken']['symbol'],
        "price": data['pairs'][0]['priceUsd'],
        "price_1h": data['pairs'][0]['priceChange']['h1'],
        "price_24h": data['pairs'][0]['priceChange']['h24'],
        "volume_24h": data['pairs'][0]['volume']['h24'],
        "fdv_market_cap": data['pairs'][0]['fdv'],
        "liquidity": data['pairs'][0]['liquidity']['usd'],
    }

    # send the message
    message = ""
    # message += "⚡ Net️work: Ethereum" + "\n"
    message += f"Token name: {token_info['name']}\n"
    message += f"Token symbol: {token_info['symbol']}\n"
    message += "💰 Price: $" + str(token_info['price']) + "\n"
    price1h_emoji = "📈" if token_info['price_1h'] > 0 else "📉"
    price24h_emoji = "📈" if token_info['price_24h'] > 0 else "📉"
    message += price1h_emoji + " 1h: " + \
        str(token_info['price_1h']) + "%" + "\n"
    message += price24h_emoji + " 24h: " + \
        str(token_info['price_24h']) + "%" + "\n"
    message += "📊 Volume: $" + str(token_info['volume_24h']) + "\n"
    message += "💦 Liquidity: $" + str(token_info['liquidity']) + "\n"
    message += "💎 Market Cap (FDV): $" + \
        str(token_info['fdv_market_cap']) + "\n"

    print(message)
    await update.effective_chat.send_message(message)


@is_bot_chat(bot_chat_id)
@admin_only()
@check_user_has_config()
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
    if not is_valid_token_address(web3, local_user_config['token_address']):
        await update.message.reply_text(f'The token address is not valid.')
        return

    print("Token address: ", local_user_config['token_address'])
    print("Pair address: ", local_user_config['pair_address'])

    contract = web3.eth.contract(
        address=local_user_config['pair_address'], abi=uniswap_pair_abi)

    print("local_user_config: ", local_user_config)

    # check if bot is already running
    if update.effective_user.id in users_tasks:
        await update.message.reply_text(f'Buybot is already running.')
        return

    # run the run_buybot function on a new thread
    users_tasks[update.effective_user.id] = asyncio.create_task(
        run_buybot(contract, update, local_user_config))

    await update.message.reply_text(f'Buybot started.')


@is_bot_chat(bot_chat_id)
@admin_only()
@check_user_has_config()
async def buybotconfigvideo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # print(update.message)

    # get file id from the message
    video = update.message.video
    print(update.message)

    # download the file
    file = await context.bot.get_file(video.file_id)
    # get caption
    caption = update.message.caption
    print(caption)

    if (caption == "/gif"):
        # get the file name
        file_name = video.file_name
        print(file_name)
        # save the file
        await file.download_to_drive(file_name)

        users_configs = read_json_file("users_configs.json")

        # check if the user already has a config
        for user_config in users_configs:
            if user_config["user_id"] == update.effective_user.id:
                # update the emoji
                user_config["gif"] = file_name
                await update.message.reply_text("Gif updated.")
                # write the users_configs variable to the users_configs.json file
                with open('users_configs.json', 'w') as outfile:
                    json.dump(users_configs, outfile)
                return


@is_bot_chat(bot_chat_id)
@admin_only()
@check_user_has_config()
async def stop_buybot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # check if the user has a task running
    if update.effective_user.id not in users_tasks:
        await update.message.reply_text(f'Buybot is not running.')
        return

    task = users_tasks[update.effective_user.id]

    # check if the run_buybot_task is running
    if task == None:
        await update.message.reply_text(f'Buybot is not running.')
        return

    # cancel the run_buybot_task
    task.cancel()

    # delete the task from the users_tasks dictionary
    del users_tasks[update.effective_user.id]

    await update.message.reply_text(f'Buybot stopped.')


@is_bot_chat(bot_chat_id)
@admin_only()
@check_user_has_config()
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
            user_config["telegramurl"] = args[0]
            await update.message.reply_text("Telegram url updated.")
            # write the users_configs variable to the users_configs.json file
            with open('users_configs.json', 'w') as outfile:
                json.dump(users_configs, outfile)
            return


@is_bot_chat(bot_chat_id)
@admin_only()
@check_user_has_config()
async def advertiser_fn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # extract the command arguments
    args = context.args

    # check if the user sent a parameter
    if not args:
        await update.message.reply_text("You didn't specify advertiser url.")
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
            user_config["advertiser"] = args[0]
            await update.message.reply_text("Telegram url updated.")
            # write the users_configs variable to the users_configs.json file
            with open('users_configs.json', 'w') as outfile:
                json.dump(users_configs, outfile)
            return


@is_bot_chat(bot_chat_id)
@admin_only()
@check_user_has_config()
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


@is_bot_chat(bot_chat_id)
@admin_only()
@check_user_has_config()
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


@is_bot_chat(bot_chat_id)
@admin_only()
@check_user_has_config()
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


@is_bot_chat(bot_chat_id)
@admin_only()
async def buybot_configaddress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # extract the command arguments
    args = context.args

    # check if the user sent a parameter
    if not args:
        await update.message.reply_text("You didn't specify token address.")
        return

    # validate the token address
    is_valid = is_valid_token_address(web3, Web3.toChecksumAddress(args[0]))
    if not is_valid:
        await update.message.reply_text("Invalid token address.")
        return

    pair_address = await get_pair_addressV2(Web3.toChecksumAddress(args[0]))

    token_info = get_token_info(
        moralis_api_key, web3.toChecksumAddress(args[0]))

    # get chat id from the update
    chat_id = update.effective_chat.id

    users_configs = read_json_file("users_configs.json")
    local_user_config = None

    # check if the user already has a config
    for user_config in users_configs:
        if user_config["user_id"] == update.effective_user.id:
            local_user_config = user_config
            local_user_config["token_address"] = web3.toChecksumAddress(
                args[0])
            local_user_config["pair_address"] = pair_address
            local_user_config["chat_id"] = chat_id
            local_user_config["decimals"] = int(token_info["decimals"])
            # replace the user config in the users_configs array
            users_configs[users_configs.index(user_config)] = local_user_config
            await update.message.reply_text("Token address updated.")
            break

    if local_user_config is None:
        # append the user id and token address to users_configs array
        users_configs.append({
            "user_id": update.effective_user.id,
            "token_address": web3.toChecksumAddress(args[0]),
            "pair_address": pair_address,
            "decimals": int(token_info["decimals"]),
            "chat_id": chat_id,
            "emoji": "⚪️",
            "telegramurl": "https://t.me/",
            "advertiser": "https://google.com/",
            "twitterurl": "https://twitter.com/",
            "websiteurl": "https://google.com/",
            "gif": "video.mp4"
        })

    # save the users_configs array to a json file
    with open('users_configs.json', 'w') as outfile:
        json.dump(users_configs, outfile)

    message = "Selected token:\n"
    message = f"Token name: {token_info['name']}\n"
    message += f"Token symbol: {token_info['symbol']}\n"
    message += f"Pair address: {pair_address}\n"

    # send the message back
    await update.message.reply_text(message)


async def ask_chat_gpt_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # extract the command arguments
    args = context.args

    # check if the user sent a parameter
    if not args:
        await update.message.reply_text("You didn't specify a prompt.")
        return

    question = ""

    for i in range(len(args)):
        question += args[i]
        if i < len(args) - 1:
            question += " "
    print(question)

    # set bot typing status
    await update.effective_chat.send_chat_action("typing")

    # You can specify custom conversation and parent ids. Otherwise it uses the saved conversation (yes. conversations are automatically saved)
    response = chatbot.ask(question, conversation_id=None, parent_id=None)

    # text to speech response
    tts = gTTS(response['message'], lang='en', tld='co.uk', slow=False)
    # get user id from the update
    user_id = update.effective_user.id
    # gen filename
    filename = f"{user_id}.mp3"
    # save the mp3 file
    tts.save(filename)

    await update.effective_chat.send_voice(filename)

    # remove the mp3 file
    os.remove(filename)


async def ask_chat_gpt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # extract the command arguments
    args = context.args

    # check if the user sent a parameter
    if not args:
        await update.message.reply_text("You didn't specify a prompt.")
        return

    question = ""

    for i in range(len(args)):
        question += args[i]
        if i < len(args) - 1:
            question += " "
    print(question)

    # set bot typing status
    await update.effective_chat.send_chat_action("typing")

    # You can specify custom conversation and parent ids. Otherwise it uses the saved conversation (yes. conversations are automatically saved)
    response = chatbot.ask(question, conversation_id=None, parent_id=None)

    await update.effective_chat.send_message(response['message'])


def get_env_file_variables():
    moralis_api_key = os.getenv('moralis_api_key')
    etherscan_api_key = os.getenv('etherscan_api_key')
    infura_api_key = os.getenv('infura_api_key')
    chatGPT_token = os.getenv('chatGPT_token')
    telegram_token = os.getenv('telegram_token')

    return moralis_api_key, etherscan_api_key, infura_api_key, chatGPT_token, telegram_token


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    # link
    link = "https://t.me/+NxL2xoRkFIY1MTU0"

    # create markdown link
    markdown_link = "[Group]("+link + ")"

    # await update.effective_chat.send_message(text=f"Selected option: {query.data}")
    await update.effective_chat.send_message(markdown_link, parse_mode="MarkdownV2")


if __name__ == "__main__":
    load_dotenv()

    moralis_api_key, etherscan_api_key, infura_api_key, chatGPT_token, telegram_token = get_env_file_variables()

    # add your blockchain connection information
    infura_url = 'https://mainnet.infura.io/v3/' + infura_api_key
    web3 = Web3(Web3.HTTPProvider(infura_url))

    app = ApplicationBuilder().token(telegram_token).build()
    # app.add_handler(CommandHandler("ai", ask_chat_gpt))
    # app.add_handler(CommandHandler("aivoice", ask_chat_gpt_voice))
    app.add_handler(CommandHandler("price", call_get_price_bot))
    app.add_handler(CommandHandler("address", buybot_configaddress))
    app.add_handler(CommandHandler("emoji", buybot_configemoji))
    app.add_handler(CommandHandler("website", buybot_configwebsiteurl))
    app.add_handler(CommandHandler("telegram", buybot_configtelegramurl))
    app.add_handler(CommandHandler("twitter", buybot_configtwitterurl))
    app.add_handler(CommandHandler("advertiser", advertiser_fn))
    app.add_handler(CommandHandler("startbuybot", start_buybot))
    app.add_handler(CommandHandler("stopbuybot", stop_buybot))
    app.add_handler(CommandHandler("help", buybot_help))
    app.add_handler(MessageHandler(filters.VIDEO, buybotconfigvideo))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler("test", send_message))
    # app.add_handler(CommandHandler("gif", set_gif))
    # create message handler for .gif files
    # app.add_handler(MessageHandler(filters.Document, buybotconfiggif))
    # app.add_handler(CommandHandler("buybotconfigif", buybotconfigif))

    app.run_polling()
