ASCII_LOWER_A = 97

def get_list():
    my_list = []
    for i in range(5):
        num = input(f'Enter {chr(ASCII_LOWER_A + i)}: ')
        if not num:
            continue

        my_list.append(int(num))
    return my_list

def product_list(numbers):
    product_sum = 1
    for num in numbers:
        product_sum *= num
    return product_sum


if __name__ == '__main__':
    my_list = get_list()

    my_min = min(my_list)
    print("Minimum: " + str(my_min))

    print("Product of first 4 numbers: ")
    product = product_list(my_list[:4])
    print(f"  {product}")

    print("Product of last 4 numbers")
    product = product_list(my_list[-4:])
    print(f"  {product}")