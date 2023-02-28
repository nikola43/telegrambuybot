from web3 import Web3
from web3.middleware import geth_poa_middleware
from uniswapv3sdk import UniswapV3SDK
from uniswapv3sdk.utils import token_to_id

# Initialize Web3
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/d39a866f4f6d49b9916f9269bf880110'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Set the UniswapV3Pool pair address and token addresses
pair_address = '0x1f98431c8ad98523631ae4a59f267346ea31f984' # Example pair address for ETH/USDC
token0_address = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2' # Example token 0 address for ETH
token1_address = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48' # Example token 1 address for USDC

# Create UniswapV3SDK instance
sdk = UniswapV3SDK(pair_address, token0_address, token1_address, w3)

# Set the tick spacing and tick range
tick_spacing = sdk.get_tick_spacing()
tick_lower = sdk.get_tick_lower(-3*tick_spacing)
tick_upper = sdk.get_tick_upper(3*tick_spacing)

# Subscribe to the UniswapV3Pool events
pool_contract = w3.eth.contract(pair_address, abi=sdk.pool_abi)
event_filter = pool_contract.events.Swap.createFilter(fromBlock='latest')
while True:
    events = event_filter.get_new_entries()
    for event in events:
        # Check if the event is a buy or a sell
        if event.args.amount0In > 0:
            # Buy event
            amount_in = event.args.amount0In
            amount_out = event.args.amount1Out
            token_in = sdk.token0
            token_out = sdk.token1
        elif event.args.amount1In > 0:
            # Sell event
            amount_in = event.args.amount1In
            amount_out = event.args.amount0Out
            token_in = sdk.token1
            token_out = sdk.token0
        else:
            # Not a buy or a sell event
            continue

        # Convert the token amounts to token prices in ETH
        price_in_eth = sdk.get_price(token_in, token_out, amount_in, amount_out, tick_lower, tick_upper)

        # Print the buy or sell event and the token price in ETH
        if amount_in > 0 and amount_out > 0:
            print(f'{token_in.symbol} bought {token_out.symbol}: {amount_in} {token_in.symbol} for {amount_out} {token_out.symbol} at {price_in_eth:.8f} ETH/{token_out.symbol}')

