import cv2
import pytesseract
import numpy as np
from fuzzywuzzy import process, fuzz

def parse_receipt(processed_image):

    food_categories = ["FROZEN/DAIRY", "GROCERY", "MEAT", "DELI", "PRODUCE"]
    keywords = ["You saved", "Tax Paid", "BALANCE DUE", "FROZEN/DAIRY", "GROCERY", "MEAT", "DELI", "PRODUCE"]

    ret = pytesseract.image_to_string(processed_image, output_type=pytesseract.Output.STRING)

    # Format lines nicely
    rows = [row.split(' ') for row in ret.strip().split('\n')]
    rows = [row for row in rows if row != [''] and row != ['','']]

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    print(rows)
    # Break into groups
    groups = {}
    in_group = False
    cur_header = ""
    balance_due = -1
    tries = 0
    skip = False
    while(tries < 70):
        for row in rows:
            skip = False      
            # Check all possible keywords for every row
            whole_string = (' ').join(row)
            closest_word, similarity = process.extractOne(whole_string, keywords)
            # print(f"sim: {similarity}, closest_header: {closest_word}, orig row: {row}")
            
            # Check similarity first
            if similarity > 70 - tries:
                # Then prune based on chosen keyword
                if closest_word in food_categories and len(row) == 1: # If food category then row only has one word
                    cur_header = closest_word
                    in_group = True
                    groups[cur_header] = []
                    skip = True # Don't add row with header to group
                elif closest_word == "You saved" and len(row) == 3:
                    skip = True # Don't add row with savings to group
                elif closest_word == "Tax Paid" and len(row) == 2: # If Tax Paid header then original row has two words
                    in_group = False
                elif closest_word == "BALANCE DUE" and len(row) == 3 or len(row) == 4: # If BALANCE PAID header then original row has two or three words
                    balance_due = row[len(row)-1] # Amount due is last value of row probably
                    
            # Add row if currently in a food group header
            if in_group and skip == False:
                groups[cur_header].append(row)
                
        # Try again with lower threshold if balance due was not found
        if balance_due == -1:
            tries += 1
        else:
            break

        
    # Extract prices for each item
    # Items might have a # purchased that needs to be determined
    foods = []
    second_line = False
    for group in groups:
        print(f"\ngroup: {group}")
        # Each row may refer to the item and its cost, just the item, or the quantity and cost of the previous item
        for row in groups[group]:
            if not second_line:
                food_name = ""
                food_cost = -1
                first_word = True
                print(row)
                for i, word in enumerate(row):
                    if not is_number(word):
                        if first_word:
                            food_name += word
                            first_word = False
                        elif word != 'A' and word != 'x' and word != 'Ax':
                            food_name += ' ' + word
                    else: # word is a number
                        food_cost = float(word)
                        
                    # If removing last one or two characters of last string allows string to convert to a number then use that number
                    if i == len(row)-1 and len(word) > 2:
                        word = word[:-1]
                        if is_number(word):
                            food_cost = float(word)
                        else:
                            word = word[:-1]
                            if is_number(word):
                                food_cost = float(word)
                        
                # Check if food exists in keywords already
                # If so, iterate num_items for food_name and skip appending new food to foods
                closest_word, similarity = process.extractOne(food_name, keywords)
                # print(f"sim: {similarity}, closest_header: {closest_word}, orig name: {food_name}")
                food_entry_index = next((i for i, item in enumerate(foods) if item['name'] == closest_word), None)
                if similarity > 70 and food_entry_index != None:
                    foods[food_entry_index]['num items'] += 1
                    foods[food_entry_index]['total cost'] += food_cost
                    # print("adding")
                else:
                    # Check to see if we have to parse a second line for this food item
                    if food_cost == -1:
                        second_line = True
                    else:
                        num_items = 1
                        foods.append({"name": food_name, "num items": num_items,
                                "item_cost": food_cost/num_items, "total cost": food_cost, "food group": group})
                        # Add food name to keywords list
                        keywords.append(food_name)
                    
            else: # Parsing second line for item
                second_line = False
                # First string contains number of items purchased
                items_purchased_string = row[0]
                
                # Replace common misreads
                items_purchased_string = items_purchased_string.replace('i','1')
                items_purchased_string = items_purchased_string.replace('9','@')
                print(items_purchased_string)
                
                # Find number of item purchased
                num_purchased_str = ""
                num_items = 0
                for char in items_purchased_string:
                    if is_number(char):
                        num_purchased_str += char
                print(num_purchased_str)
                try:
                    num_items = int(num_purchased_str)
                except:
                    print("num_purchased_str could not be converted to an integer: defaulting to 1")
                    num_items = 1
                print(num_items)
                
                # Loop through remaining words
                for i, word in enumerate(row[1:]):
                    if is_number(word):
                        food_cost = float(word) # Last number is proper total cost of item
                        
                    # If removing last one or two characters of last string allows string to convert to a number then use that number
                    if i == len(row[1:])-1 and len(word) > 2:
                        word = word[:-1]
                        if is_number(word):
                            food_cost = float(word)
                        else:
                            word = word[:-1]
                            if is_number(word):
                                food_cost = float(word)
                    
                        
                foods.append({"name": food_name, "num items": num_items,
                            "item_cost": food_cost/num_items, "total cost": food_cost, "food group": group})
    
    total_read_cost = 0
    for food in foods:
        total_read_cost += food['total cost']
    if not is_number(balance_due):
        balance_due = total_read_cost
    
    return {"balance due": balance_due, "all food": foods}


# frame = cv2.imread('images/receipt_test3.jpg',0) # Preprocessed image

# receipt = parse_receipt(frame)

# print("\n\nFood: price\n")
# total_read_cost = 0
# for food in receipt['all food']:
#     total_read_cost += food['total cost']
#     print(f"{food['name']}: ${food['total cost']}, x{food['num items']}, {food['food group']}")
    
# print(f"\nbalance due: ${receipt['balance due']}, calculated cost: ${total_read_cost}, error: ${abs(float(receipt['balance due']) - total_read_cost)}")
# print("\n\n")
# print(receipt)