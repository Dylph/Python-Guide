# Input the number of people and the total discount
num_people = int(input("Enter the number of people: "))
total_discount = float(input("Enter the total discount (%): "))
extra_fees = float(input("Enter any extra fees: "))

# Initialize empty lists to store the price and total cost of items for each person
total_cost_list = []

# Loop through each person and input their price and total cost of items
for i in range(num_people):
    total_cost = float(input("Enter the total cost of items ordered by person {}: ".format(i+1)))
    total_cost_list.append(total_cost)

# Calculate the total cost of all items ordered and the discounted total
total_cost_all = sum(total_cost_list)
discounted_total = total_cost_all * (1 - total_discount/100)

# Calculate the amount each person needs to pay based on the percentage of the total cost of the items they ordered
amount_list = []
for i in range(num_people):
    amount = (total_cost_list[i] / total_cost_all) * discounted_total + (extra_fees / num_people)
    amount_list.append(amount)

# Print the amount each person needs to pay
for i in range(num_people):
    print("Person {}: Order total = ${:.2f}, Amount owed = ${:.2f}".format(i+1, total_cost_list[i], amount_list[i]))

# Calculate and print the total amount owed by all people
total_amount_owed = sum(amount_list)
print("Total amount owed by all people = ${:.2f}".format(total_amount_owed))
