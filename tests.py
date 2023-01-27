import unittest

from utils import extract_event_data, get_token_price_and_volume, get_token_holders_supply_name, get_token_dead_balance, get_token_balance, get_token_taxes, calc_circulating_supply, calc_market_cap, create_emoji_text, create_message, create_keyboard


# test for get token price and volume
class TestGetTokenPriceAndVolume(unittest.TestCase):

    async def test_get_token_price_and_volume(self):
        price, volume = await get_token_price_and_volume(
            "0xEf27252B567F6B3fe35b34A85bE322917abE524A")
        self.assertIsNotNone(price)
        self.assertIsNotNone(volume)
        print(price, volume)


if __name__ == '__main__':
    unittest.main()
