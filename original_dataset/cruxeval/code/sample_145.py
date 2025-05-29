def f(price, product):
    inventory = ['olives', 'key', 'orange']
    if product not in inventory:
        return price
    else:
        price *= 0.85
        inventory.remove(product)
    return price