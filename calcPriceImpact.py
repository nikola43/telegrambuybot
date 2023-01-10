
"""     
    This calculation uses the constant product formula used on Uniswap to determine how much of one asset should be swapped for another asset.
    Some exchanges may have a slightly more complex formula to combat price impact or impermanent loss.
    But this is the most common and easiest to calculate.

    Constant product formula: token_a_pool_size * token_b_pool_size = constant_product
    constant_product will be the same number before and after a trade occurs.

    A couple of examples to show price impact calculation:

    Starting pool for both examples

    Initial pool info

    wMATIC = 3024
    LUCHA = 4318
    Constant Product = 13,057,632
    Lucha Market Price = 0,700322422 wMATIC
    First example : 100 wMATIC for LUCHA

    After swap

    wMATIC = 3124 (we added 100 wMATIC to the pool)
    Constant Product = 13,057,632 (stays the same)
    LUCHA = 4179,77977 (constant product / new wMATIC amount)
    LUCHA received = 138,22023 (old LUCHA amount — new LUCHA amount)
    Price paid per LUCHA= 0,72334830965 wMATIC
    Price impact =1- (Market price / Price paid) = 3,18%  """

def main():
    reserves = [105400002905146747094744708, 15243964198084823781]
    pair_a_reserve = reserves[0]
    pair_b_reserve = reserves[1]
    tx_amount1In = 10000000000000000

    constant_product = pair_a_reserve * pair_b_reserve
    print("Constant product: ", constant_product)

    pair_a_per_pair_b_price = pair_a_reserve / pair_b_reserve
    print("Pair A per pair B price: ", pair_a_per_pair_b_price)

    # calculate price impact based on the constant product formula
    pair_a_reserve_after_swap = pair_a_reserve + tx_amount1In
    print("Pair A reserve after swap: ", pair_a_reserve_after_swap)

    pair_b_reserve_after_swap = constant_product / pair_a_reserve_after_swap
    print("Pair B reserve after swap: ", pair_b_reserve_after_swap)

    pair_b_received = pair_b_reserve - pair_b_reserve_after_swap
    print("Pair B received: ", pair_b_received)

    pair_b_price_paid_per_pair_a = pair_a_reserve / pair_b_reserve_after_swap
    print("Pair B price paid per pair A: ", pair_b_price_paid_per_pair_a)

    price_impact = 1 - (pair_a_per_pair_b_price / pair_b_price_paid_per_pair_a)
    #price_impact = price_impact * 100

    print("Price impact: ", price_impact, "%")

if __name__ == "__main__":
    main()
