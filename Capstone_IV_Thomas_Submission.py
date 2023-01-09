"""
SE T32 - Capstone Project IV - OOP
Thomas Siu - TS22110004677
"""

#========Import modules========
from tabulate import tabulate
import re
import pandas

#========The beginning of the class========
class Shoe:

    #Initialise with attributes
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
    
    #Method to return cost of product
    def get_cost(self):
        return int(self.cost)
    
    #Method to return quantity of product
    def get_quantity(self):
        return int(self.quantity)

    #Method to provide string representation of the object
    def __str__(self):
        return self.country,self.code,self.product,self.cost,self.quantity

#========Shoe list========
#The list will be used to store a list of objects of shoes.
shoe_list = []

#========Functions outside the class========

#Function to open the 'inventory.txt' file, loop through the file and create shoe objects, store into the shoe_list
def read_shoes_data(shoe_list):

    #Open the 'inventory.txt' file in read mode
    with open('inventory.txt', 'r') as inv_file:
        
        #Skip the first line of the file as it contains the header
        next(inv_file)

        #for each line in the file, create a shoe object and add to the shoe_list
        for inventory in inv_file:
            try:
                country, code, product, cost, quantity = inventory.split(',')
                quantity = quantity.strip()
                new_shoe = Shoe(country,code,product,cost,quantity)
                shoe_list.append(new_shoe)
            except Exception as error:
                print(error)
    

#Function to allow a user to capture data about a shoe
#Use this data to create a shoe object and append to the shoe_list
def capture_shoes(shoe_list):
    
    print('Provide the product information to add to the inventory list: ')
    country = input('Please enter the country: ')
    code = input('Please enter the inventory code: ')
    product = input('Please enter the product name: ')
    cost = input('Please enter the inventory cost: ')
    quantity = input('Please enter the inventory quantity: ')

    #Create a shoe object based on the data and append to the shoe_list
    new_shoe = Shoe(country,code,product,cost,quantity)
    shoe_list.append(new_shoe)
    
    #Also add the new shoe info to the 'inventory.txt' file
    with open('inventory.txt', 'a') as inv_file:
        inv_file.write(f'\n{country}, {code}, {product}, {cost}, {quantity}')


#Function to iterate over the shoe list and print info in user friendly table
def view_all(shoe_list):
    table = []
    for shoe in shoe_list:
        table.append(shoe.__str__())
    print(tabulate(table, headers=['country','code','product','cost','quantity'], tablefmt="outline"))
    

#Function to find the shoe object with the lowest quantity
#Ask user if they want to add quantity to this shoe; if so, update the 'inventory.txt' file and shoe list
def re_stock(shoe_list):

    #Loop through shoe list and find lowest quantity item, mark the lowest stock item with 'min_flag'
    quantity = None
    for index, shoe in enumerate(shoe_list):
        if quantity is None or shoe.get_quantity() < quantity:
            quantity = shoe.get_quantity()
            min_flag = index
    print('\nThe following item has the lowest quantity in inventory.')
    print(tabulate([shoe_list[min_flag].__str__()],headers=['country','code','product','scost','quantity'], tablefmt="outline"))
    
    #Ask user if they want to restock this product
    while True:
        #Note that input is transform to lowercases
        rs_decision = str(input('Do you want to restock this product? (Enter Yes or No) ')).lower()
        print(rs_decision)
        #if user input yes, ask how many they want to add to inventory
        if rs_decision == 'yes':
            try:
                add_quantity = int(input(f'How many units of {shoe_list[min_flag].code} do you want to add? '))
                #Number to update will be the sum of existing stock plus amount to add
                rs_quantity = add_quantity + quantity
            except Exception:
                print('Incorrect entry, try again.')
                break
            
            #Update shoe list and 'inventory.txt'
            shoe_list[min_flag].quantity = rs_quantity
            #Note that min_flag is 1 less than the line index in 'inventory.txt'
            #This is because we skipped a line when creating the shoe list
            with open('inventory.txt','r') as inv_file:
                i_data = inv_file.readlines()
                index = min_flag + 1    
                a, b, c, d, e = i_data[index].split(',')
            with open('inventory.txt', 'w') as inv_file:
                i_data[index] = i_data[index].replace(f'{e}',f'{str(rs_quantity)}\n')
                inv_file.writelines(i_data)
            break
        elif rs_decision == 'no':
            break
        else:
            print('Please enter either Yes or No')
   

#Function to search for a shoe fusing a shoe code provided by user
def search_shoe(shoe_list):

    search_code = str(input('Please enter the shoe code for seaching: '))
    search_result = None
    for shoe in shoe_list:
        if shoe.code == search_code:
            #Store result if the user code matches a product
            search_result = [shoe.__str__()]
    
    #Only print result if there is a result
    if search_result is not None:
        print(tabulate(search_result,headers=['country','code','product','scost','quantity'], tablefmt="outline"))
    else:
        print('No product is found based on the code entered. Please try again.')


#Function to calculate the total value for each item in inventory
# value = cost * quantity ; display result on screen for all shoes
def value_per_item(shoe_list):

    table_s = []
    table_v = []
    #Loop through each shoe in list to calculate value
    for shoe in shoe_list:
        value = shoe.get_cost() * shoe.get_quantity()
        #Store information in table: shoe info (table_s) and calculated values (table_v)
        table_s.append(shoe.__str__())
        table_v.append(value)
    #transform table_s into dataframe and merge table_v
    table_m = pandas.DataFrame(table_s)
    table_m[''] = table_v
    #Display info on screen, 'value' being the last column
    print(tabulate(table_m, headers=['country','code','product','cost','quantity','value'], tablefmt="outline", showindex=False))


#Function to determine the product with the highest quantity and print it as being for sale
def highest_qty(shoe_list):

    #Loop through shoe list and find highest quantity item, mark the highest stock item with 'max_flag'
    quantity = None
    for index, shoe in enumerate(shoe_list):
        if quantity is None or shoe.get_quantity() > quantity:
            quantity = shoe.get_quantity()
            max_flag = index
    print('\nThe following item has the highest quantity in inventory. This item could be marked for sale.')
    print(tabulate([shoe_list[max_flag].__str__()],headers=['country','code','product','scost','quantity'], tablefmt="outline"))


#==========Main Program=============

#Begin by reading in shoes information from 'inventory.txt'
read_shoes_data(shoe_list)

#A menu that allow the user to execute each function
while True:
    #presenting the menu to the user and
    #making sure that the user input is coneverted to lower case
    menu = input('''Select one of the following Options below:
1 - View all inventory
2 - Add a new product onto the inventory list
3 - Search for a product using product code
4 - Find the product with the lowest quantity and restock
5 - Find the product with the highest quantity (potential sale)
6 - Display all product values
7 - Exit
: ''').lower()

    if menu == '1':
        view_all(shoe_list)

    elif menu == '2':
        capture_shoes(shoe_list)

    elif menu == '3':
        search_shoe(shoe_list)

    elif menu == '4':
        re_stock(shoe_list)

    elif menu == '5':
        highest_qty(shoe_list)

    elif menu == '6':
        value_per_item(shoe_list)

    #Exit or else user to select again
    elif menu == '7':
        print('Goodbye!')
        exit()

    else:
        print("Incorrect entry, please try again")