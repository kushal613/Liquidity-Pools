import math
# For an automated market maker in which the deposited token pair must be of equal value, and the quantities of the two tokenmust always multiply to the same constant (xy=k)

# Some basic information about the liquidity pool given a few arguments
def calculate_pool(deposit_ETH, initial_ETH_quantity, initial_DAI_quantity):
    initial_ETH_price = initial_DAI_quantity / initial_ETH_quantity
    deposit_DAI = deposit_ETH * initial_ETH_price
    k = initial_ETH_quantity * initial_DAI_quantity
    print(f"Based on the ETH to DAI price ratio, if you want to deposit {deposit_ETH} ETH to this liquidity pool, you must also supply {deposit_DAI} DAI. The constant for this CPMM is {k}, so the amount of each token must always multiply to this value.", flush=True)
# calculate_pool(1, 10, 1000)

#Since the price of ETH is less in the pool and more in the market, arbitrageurs will buy ETH from the pool and sell it on the market.
def arbitrage_once(initial_ETH_quantity, initial_DAI_quantity, new_ETH_price, remove_ETH_increment=1, remove_DAI_increment=100):
    k = initial_ETH_quantity * initial_DAI_quantity
    initial_ETH_price = initial_DAI_quantity / initial_ETH_quantity
    if new_ETH_price > initial_ETH_price:
        new_DAI_quantity = k / (initial_ETH_quantity - remove_ETH_increment)
        supply_DAI_once = new_DAI_quantity - initial_DAI_quantity # how much DAI must be deposited to get 'remove_ETH_increment' ETH
        # The closer remove_ETH_increment gets to initial_ETH_quantity, the greater the amount of DAI will have to be supplied.
        
        profit_once_in_DAI = (new_ETH_price * remove_ETH_increment) - supply_DAI_once # This is when the remove_ETH_increment is specified in the arbitrage_once argument
        profit_once_in_ETH = profit_once_in_DAI / new_ETH_price
        new_ETH_quantity = initial_ETH_quantity - remove_ETH_increment

        # print(f"To buy {remove_ETH_increment} ETH from the pool, the arbitrager must supply {supply_DAI_once} DAI. Then, by selling this one ETH on the market for the new ETH price of ${new_ETH_price}, the one-time profit for the arbitrager is ${profit_once_in_DAI}. The new supply of DAI in the pool is {new_DAI_quantity}, and the new ETH supply in the pool is {new_ETH_quantity}. Not surprisingly, these numbers still multiply to {new_ETH_quantity * new_DAI_quantity}")

        print(f"z {profit_once_in_DAI}")
        return profit_once_in_DAI

    elif new_ETH_price < initial_ETH_price: # new_ETH_price < initial_ETH_price, meaning value of ETH dropped --> arbitrageurs will buy DAI from the pool and sell it for more ETH.
        # print("Thew market ETH price is less than the price of ETH in the pool, so arbitrageurs will buy DAI from the pool and sell it for more ETH.")
        new_ETH_quantity = k / (initial_DAI_quantity - remove_DAI_increment)
        supply_ETH_once = new_ETH_quantity - initial_ETH_quantity # how much ETH must be deposited to get 'remove_DAI_increment' DAI
        # The closer remove_DAI_increment gets to initial_DAI_quantity, the greater the amount of ETH will have to be supplied.

        profit_once_in_ETH = (remove_DAI_increment / new_ETH_price) - supply_ETH_once
        profit_once_in_DAI = profit_once_in_ETH * new_ETH_price
        new_DAI_quantity = initial_DAI_quantity - remove_DAI_increment

        # print(f"Buying {remove_DAI_increment} DAI will yield a profit of {profit_once_in_DAI} DAI.")
        print(f"r {profit_once_in_DAI}")
        return profit_once_in_DAI
    else:
        print("(Further) one-way arbitrage not possible.")
        return -1
# arbitrage_once(10, 1000, 400, 6, 1)

def arbitrage_once_max(initial_ETH_quantity, initial_DAI_quantity, new_ETH_price):
    k = initial_ETH_quantity * initial_DAI_quantity
    initial_ETH_price = initial_DAI_quantity / initial_ETH_quantity  
    if new_ETH_price > initial_ETH_price:
        remove_ETH_increment_to_max_profit = ((new_ETH_price * initial_ETH_quantity) - math.sqrt(k* new_ETH_price)) / new_ETH_price
        max_profit = (new_ETH_price * remove_ETH_increment_to_max_profit) - ((k / (initial_ETH_quantity - remove_ETH_increment_to_max_profit)) - initial_DAI_quantity)
        print(f"To maximize profit, buy {remove_ETH_increment_to_max_profit} ETH, for a maximum profit of {max_profit} DAI.")

        global remove_ETH_increment_for_zero_profit
        remove_ETH_increment_for_zero_profit = (new_ETH_price * initial_ETH_quantity - initial_DAI_quantity + math.sqrt((initial_DAI_quantity - new_ETH_price * initial_ETH_quantity)**2 - 4*new_ETH_price*(k - initial_DAI_quantity * initial_ETH_quantity))) / (2 * new_ETH_price)
        zero_profit = (new_ETH_price * remove_ETH_increment_for_zero_profit) - ((k / (initial_ETH_quantity - remove_ETH_increment_for_zero_profit)) - initial_DAI_quantity)
        print(f"To get {zero_profit} profit, buy {remove_ETH_increment_for_zero_profit} ETH.")

    else: # new_ETH_price < initial_ETH_price, meaning value of ETH dropped --> arbitrageurs will buy DAI from the pool and sell it for more ETH.
        remove_DAI_increment_to_max_profit = initial_DAI_quantity - math.sqrt(new_ETH_price * k)
        max_profit = initial_DAI_quantity + new_ETH_price * initial_ETH_quantity - 2 * math.sqrt(new_ETH_price * k)
        print(f"To maximize profit, buy {remove_DAI_increment_to_max_profit} DAI, for a maximum profit of {max_profit} DAI.")

        global remove_DAI_increment_for_zero_profit
        remove_DAI_increment_for_zero_profit = (initial_DAI_quantity - new_ETH_price * initial_ETH_quantity - (new_ETH_price * initial_ETH_quantity - initial_DAI_quantity)) / 2
        zero_profit = (initial_DAI_quantity - new_ETH_price * initial_ETH_quantity + (new_ETH_price * initial_ETH_quantity - initial_DAI_quantity)) / 2
        print(f"To get {zero_profit} profit, buy {remove_DAI_increment_for_zero_profit} DAI.")
# arbitrage_once_max(1000, 1000, 6)

# The arbitrage will continue until the price ratio in the pool equals the market price ratio. Beyond this point, it is not profitable for arbitrageurs to continue the arbitrage process.
def arbitrage_max_one_way_incremental(initial_ETH_quantity, initial_DAI_quantity, new_ETH_price, remove_ETH_increment, remove_DAI_increment):
    """
    Given a few parameters, this function does the following:
    1. Lists the incremental change in ETH and DAI in the liquidity pool given the specified remove increments, for max. arbitrage
    2. Gives the profit for the arbitrageur.
    3. Tells if further one-way arbitrage given the remove increments is not possible.
    """
    initial_ETH_price = initial_DAI_quantity / initial_ETH_quantity
    k = initial_ETH_quantity * initial_DAI_quantity
    global change_in_ETH_by_arbitrage_max
    change_in_ETH_by_arbitrage_max = [initial_ETH_quantity]
    global change_in_DAI_by_arbitrage_max
    change_in_DAI_by_arbitrage_max = [initial_DAI_quantity]
    profit_from_each_arbitrage = []
    if new_ETH_price != initial_ETH_price and remove_ETH_increment < initial_ETH_quantity and remove_DAI_increment < initial_DAI_quantity:
        while new_ETH_price > initial_ETH_price and arbitrage_once(initial_ETH_quantity, initial_DAI_quantity, new_ETH_price, remove_ETH_increment, remove_DAI_increment) > 0:
            initial_DAI_quantity = k / (initial_ETH_quantity - remove_ETH_increment)
            initial_ETH_quantity = initial_ETH_quantity - remove_ETH_increment
            change_in_ETH_by_arbitrage_max.append(initial_ETH_quantity)
            change_in_DAI_by_arbitrage_max.append(initial_DAI_quantity)
            initial_ETH_price = initial_DAI_quantity / initial_ETH_quantity

        if len(change_in_DAI_by_arbitrage_max) >= 2:
            for i in range(len(change_in_DAI_by_arbitrage_max)):
                if i == 0:
                    pass
                else:
                    profit_from_each_arbitrage.append(new_ETH_price * remove_ETH_increment - (change_in_DAI_by_arbitrage_max[i] - change_in_DAI_by_arbitrage_max[i-1]))

            total_profit_for_arbitrageur = sum(profit_from_each_arbitrage)    
            print(f"Incremental change in DAI in liquidity pool: {change_in_DAI_by_arbitrage_max}")
            print(f"Incremental change in ETH in liquidity pool: {change_in_ETH_by_arbitrage_max}")
            print(profit_from_each_arbitrage)
            print(f"Total one-way arbitrage profit: ${total_profit_for_arbitrageur}")

            return total_profit_for_arbitrageur

        while new_ETH_price < initial_ETH_price and arbitrage_once(initial_ETH_quantity, initial_DAI_quantity, new_ETH_price, remove_ETH_increment, remove_DAI_increment) > 0:
            initial_ETH_quantity = k / (initial_DAI_quantity - remove_DAI_increment)
            initial_DAI_quantity = initial_DAI_quantity - remove_DAI_increment
            change_in_ETH_by_arbitrage_max.append(initial_ETH_quantity)
            change_in_DAI_by_arbitrage_max.append(initial_DAI_quantity)
            initial_ETH_price = initial_DAI_quantity / initial_ETH_quantity

        if len(change_in_ETH_by_arbitrage_max) >= 2:
            for i in range(len(change_in_ETH_by_arbitrage_max)):
                if i == 0:
                    pass
                else:
                    profit_from_each_arbitrage.append(((remove_DAI_increment / new_ETH_price) - (change_in_ETH_by_arbitrage_max[i] - change_in_ETH_by_arbitrage_max[i-1])) * new_ETH_price)
            
            total_profit_for_arbitrageur = sum(profit_from_each_arbitrage)
            print(f"Incremental change in DAI in liquidity pool: {change_in_DAI_by_arbitrage_max}")
            print(f"Incremental change in ETH in liquidity pool: {change_in_ETH_by_arbitrage_max}")
            print(profit_from_each_arbitrage)
            print(f"Total one-way arbitrage profit: ${total_profit_for_arbitrageur}")

            return total_profit_for_arbitrageur

    else:
        print("(Further) one-way arbitrage not possible.")
        return None

# arbitrage_max_one_way_incremental(10, 1000, 50, 1, 100)

def arbitrage_max_two_way_incremental(initial_ETH_quantity, initial_DAI_quantity, new_ETH_price, remove_ETH_increment, remove_DAI_increment):
    """
    Given the remove_ETH_increment and remove_DAI_increment, this function determines the maximum arbitrage profit (two-way).
    If the new_ETH_price is initially greater than the initial_ETH_price, then after a certain level of arbirage either:
    a) the two prices will be equal, or b) the new_ETH_price will be less than the ETH price in the pool
    In the first case, no further arbitrage is possible. In the second case, the reverse arbitrage procedure happens until
    the new_ETH_price equals the price of ETH in the pool.
    """

    initial_ETH_price = initial_DAI_quantity / initial_ETH_quantity
    k = initial_ETH_quantity * initial_DAI_quantity
    global change_in_ETH_by_arbitrage_max
    change_in_ETH_by_arbitrage_max = [initial_ETH_quantity]
    global change_in_DAI_by_arbitrage_max
    change_in_DAI_by_arbitrage_max = [initial_DAI_quantity]
    while new_ETH_price != initial_ETH_price and remove_ETH_increment < initial_ETH_quantity and remove_DAI_increment < initial_DAI_quantity:
        while new_ETH_price > initial_ETH_price and arbitrage_once(initial_ETH_quantity, initial_DAI_quantity, new_ETH_price, remove_ETH_increment, remove_DAI_increment) > 0:

            initial_DAI_quantity = k / (initial_ETH_quantity - remove_ETH_increment)
            initial_ETH_quantity = initial_ETH_quantity - remove_ETH_increment
            change_in_ETH_by_arbitrage_max.append(initial_ETH_quantity)
            change_in_DAI_by_arbitrage_max.append(initial_DAI_quantity)
            initial_ETH_price = initial_DAI_quantity / initial_ETH_quantity
            print(f"x {initial_ETH_price}")

        while new_ETH_price < initial_ETH_price and arbitrage_once(initial_ETH_quantity, initial_DAI_quantity, new_ETH_price, remove_ETH_increment, remove_DAI_increment) > 0:
            initial_ETH_quantity = k / (initial_DAI_quantity - remove_DAI_increment)
            initial_DAI_quantity = initial_DAI_quantity - remove_DAI_increment
            change_in_ETH_by_arbitrage_max.append(initial_ETH_quantity)
            change_in_DAI_by_arbitrage_max.append(initial_DAI_quantity)
            initial_ETH_price = initial_DAI_quantity / initial_ETH_quantity
            print(f"y {initial_ETH_price}")

# arbitrage_max_two_way_incremental(10, 1000, 400, 1, 100)

# To calculate impermanent loss, we need to find the difference in profit between holding the assets and using them to provide liquidity
# The below two functions give the same result, but in different ways.
# This assumes that the total liquidity in the pool remains constant.
def impermanent_loss_calc(deposit_ETH, initial_ETH_quantity, initial_DAI_quantity, new_ETH_price):
    percentage = deposit_ETH / initial_ETH_quantity
    initial_ETH_price = initial_DAI_quantity / initial_ETH_quantity
    arbitrage_max_one_way_incremental(initial_ETH_quantity, initial_DAI_quantity, new_ETH_price, 1, 1)
    # print(f"The LP has {percentage*100} percent of the liquidity of the pool")
    profit_from_LP_in_DAI = ((percentage * change_in_ETH_by_arbitrage_max[-1]) * new_ETH_price) + (percentage * change_in_DAI_by_arbitrage_max[-1])
    print(profit_from_LP_in_DAI)
    # print(f"Profit from providing liquidity (in DAI): {profit_from_LP_in_DAI} DAI")
    profit_from_holding = (deposit_ETH * new_ETH_price) + (deposit_ETH * initial_ETH_price)
    print(profit_from_holding)
    # print(f"Profit from holding the deposited assets: {profit_from_holding} DAI")
    impermanent_loss = profit_from_holding - profit_from_LP_in_DAI
    print(f"Impermanent loss: {impermanent_loss} DAI")
    return impermanent_loss

# impermanent_loss_calc(5000, 100, 100, 6)

# eth_liquidity_pool * token_liquidity_pool = constant_product
# eth_price = token_liquidity_pool / eth_liquidity_pool
# eth_liquidity_pool = sqrt(constant_product / eth_price)
# token_liquidity_pool = sqrt(constant_product * eth_price)

def impermanent_loss_formula(deposit_ETH, initial_ETH_quantity, initial_DAI_quantity, new_ETH_price):
    initial_ETH_price = initial_DAI_quantity / initial_ETH_quantity
    r = new_ETH_price / initial_ETH_price
    impermanent_loss_percentage = ((2 * math.sqrt(r)) / (1 + r)) - 1
    profit_from_holding = (deposit_ETH * new_ETH_price) + (deposit_ETH * initial_ETH_price)
    impermanent_loss_actual = impermanent_loss_percentage * profit_from_holding
    print(f"Impermanent loss: {abs(impermanent_loss_actual)} DAI")
    return impermanent_loss_actual

# impermanent_loss_formula(5000, 1000, 1000, 6)

# Weighted Reserves

def swap_weighted(weight_a, initial_a, initial_b, withdraw_b):
    weight_b = 1 - weight_a
    mean = (initial_a)**(weight_a) * (initial_b)**(weight_b)
    deposit_a = [mean / (initial_b - withdraw_b)**weight_b]**(1 / weight_a) - initial_a
    print(f"Amount of token a to deposit: {deposit_a}")

swap_weighted(1/3, 10, 10, 0.466)