stock = {}
prices = {}
queue = []

while True:
    cmd = input('Action: ').split()
    action = cmd.pop(0)
    if action == 'order':
        item, quantity = cmd[0], int(cmd[1])
        if item in stock and quantity <= stock[item]:
            cost = prices[item] * quantity
            print(f'Your order will cost ${cost}, would you like to proceed? (y/n) ')
            answer = input('> ').lower()
            if answer == 'y':
                stock[item] -= quantity
                print(f'You have successfully ordered {quantity}kg of {item}.')
            else:
                print('Your order has been cancelled.')
        else:
            print('Sorry, we do not currently have your request in stock.')
            cost = prices[item] * quantity
            print(f'Would you like to add your order for {quantity}kg of {item} costing ${cost} to the queue? (y/n) ')
            answer = input('> ').lower()
            if answer  == 'y':
                queue.append((item, quantity))
                print(f'Your order for {quantity}kg of {item} is currently in position {len(queue)}.')
            else:
                print('Your order has been cancelled.')
    elif action == 'deliver':
        item, quantity = cmd[0], int(cmd[1])

        if item in stock:
            stock[item] += quantity
        else:
            stock[item] = quantity
            print(f'What is the price per kg for this item?')
            price = float(input('> $'))
            prices[item] = price

        orders = [order for order in queue if order[0] in stock and order[1] <= stock[order[0]]]
        for order in orders:
            item, quantity = order
            stock[item] -= quantity
            print(f'The order for {quantity}kg of {item} has been processed.')
            queue.remove(order)
    else:
        print('That is not a valid command.')
    print()
