"""
L10 Assignment - receipt.py - Soren Reber
"""
import csv
from datetime import date, datetime
TAX_RATE = .06

def main():
    product_file = "products.csv"
    request_file = 'request.csv'
    subtotal = 0
    current_time = datetime.now()
    item_count = 0
    discount_codes = ['cheap20', 'discount20', 'irefusetopay', 'isthisarealcode']
    discount = ''

    try:
        products = read_products(product_file)
        have_code = input('Do you have a discount code? [Y/N]: ')
        if have_code.lower() == 'y':
            have_code = True
            discount = input('Please enter the discount code with or without spaces: ')
            discount = discount.replace(' ', '').replace('?', '').lower()
        else:
            have_code = False
        print('\nReal Phoods, Inc.\n')

        with open(request_file, "rt") as csv_file:

            reader = csv.reader(csv_file)

            next(reader)
            for row in reader:
                product_id = row[0]
                quantity = row[1]
                item_count += int(quantity)
                for _ in products:
                    product = products[product_id]
                    name = product[0]
                    price = product[1]
                subtotal += int(quantity) * float(price)
                print(f'{name}: {quantity} @ {price}')
        discount_amount = calc_discount(discount_codes, discount, subtotal, have_code)
        subtotal -= discount_amount
        tax_amount = subtotal * TAX_RATE
        total = subtotal + tax_amount        
        print_receipt(item_count, subtotal, total, tax_amount, current_time, discount, discount_amount)
        
    except (FileNotFoundError, PermissionError) as file_err:
        print(f'Error: Unable to find file. {file_err}')
    except KeyError as key_err:
        print(f'Error: {key_err}')

def read_products(filename):
    dictionary = {}

    
    with open(filename, "rt") as csv_file:

        reader = csv.reader(csv_file)

        next(reader)

        for row in reader:
            key = row[0]
            row[2] = float(row[2])
            dictionary[key] = row[1:]
    return dictionary

def print_receipt(item_count, sub, total, tax, current_time, discount_code, discount_amount):
        print(f'\nNumber of items: {item_count}')
        if discount_amount > 0:
            print(f'Discount code: {discount_code}')
            print(f'Amount saved with discount: {discount_amount:.2f}')
        print(f'Subtotal: {sub:.2f}')
        print(f'Sales Tax: {tax:.2f}')
        print(f'Total: {total:.2f}')
        print('\nThank you for shopping at Real Phoods, Inc.')
        print(f'{current_time:%a %b %d %H:%M:%S %Y}\n')

def calc_discount(code_list, discount_code, subtotal, have_code= False):
    discount_percent = .2
    if have_code == True:
        if discount_code in code_list:
            discount_amount = subtotal * discount_percent
            return discount_amount
    else:
        return 0

if __name__ == '__main__':
    main()    
