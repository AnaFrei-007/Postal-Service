#NAME: ANA FERRAZ DE FREITAS
#STUDENT ID: 012225342

import csv
import datetime
from package import *
from hashmap import *
from driver import *
from truck import *

# Load all data from CSV files
def load_data():
    # Load distances
    with open("distances.csv") as csvfile:
        CSV_Distance = csv.reader(csvfile)
        CSV_Distance = list(CSV_Distance)

    # Load addresses
    with open("addresses.csv") as csvfile1:
        CSV_Address = csv.reader(csvfile1)
        CSV_Address = list(CSV_Address)

    # Load package information
    with open("packages.csv") as csvfile2:
        CSV_Package = csv.reader(csvfile2)
        CSV_Package = list(CSV_Package)

    return CSV_Distance, CSV_Address, CSV_Package


# Distance calculation between two locations
def calculate_distance(x, y, CSV_Distance):
    dist = CSV_Distance[x][y]
    if dist == '':
        dist = CSV_Distance[y][x]
    return float(dist)


# Retrieve address ID from the address string
def get_address(address, CSV_Address):
    for row in CSV_Address:
        if address in row[2]:
            return int(row[0])


# Load package data into hash table
def load_package_data(filename):
    packages = HashMap()
    with open(filename) as file:
        reader = csv.reader(file)
        for row in reader:
            package_id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zipcode = row[4]
            deadline = row[5]
            weight = row[6]
            status = "At Hub"

            package = Package(package_id, address, city, state, zipcode, deadline, weight, status)
            packages.insert(package_id, package)
    return packages


# Calculate the total weight of packages for a truck
def calculate_weight(package_list, packages):
    total_weight = 0
    for package_id in package_list:
        package = packages.lookup(package_id)
        total_weight += package.get_weight()
    return total_weight


# Update Package #9
def check_and_update_package_9(available_trucks, packages_hash, current_time):
    # Loop through all the packages in the hash map
    target_time = datetime.timedelta(hours=10, minutes=20)
    if current_time >= target_time:
        for truck in available_trucks:
            if truck.departure_time >= target_time:  # Check each entry in the bucket
                package_9 = packages_hash.lookup(9)  # Lookup package 9
                if package_9:
                    package_9.update_address("410 S State St","Salt Lake City","UT","84111")


# Nearest Neighbor Algorithm for delivering packages
def delivering_packages(truck, packages, CSV_Distance, CSV_Address):
    not_delivered = [packages.lookup(package_id) for package_id in truck.package_list]
    truck.package_list.clear()

    while len(not_delivered) > 0:
        next_address = float('inf')
        next_package = None

        for package in not_delivered:
            dist = calculate_distance(get_address(truck.address, CSV_Address), get_address(package.address, CSV_Address), CSV_Distance)
            if dist < next_address:
                next_address = dist
                next_package = package

        truck.package_list.append(next_package.package_id)
        not_delivered.remove(next_package)
        truck.total_mileage += next_address  # Update total mileage
        truck.address = next_package.address
        truck.time_of_departure += datetime.timedelta(hours=next_address / 18)  # Update the time
        next_package.delivery_time = truck.time_of_departure
        next_package.departure_time = truck.departure_time
        next_package.status = "Delivered"

        next_package.set_delivered_by(truck.get_truck_id())

    truck.return_to_hub(CSV_Distance, CSV_Address)


# Method to get user input for time
def get_user_time():
    user_input = input("Please enter the time (HH:MM): ") # Military Time
    # Split the time input into hours and minutes
    try:
        hours, minutes = map(int, user_input.split(":"))
        # Convert the input time into a timedelta object
        time = datetime.timedelta(hours=hours, minutes=minutes)
        return time
    except ValueError:
        print("Invalid time format. Please enter time in HH:MM format.")
        return None


# Method to check and print package status
def print_package_status(package_obj, user_time):
    # Check the status of the package at the given time
    if package_obj.delivery_time <= user_time:
        package_obj.status = "Delivered"
    elif package_obj.departure_time <= user_time:
        package_obj.status = "En route"
    else:
        package_obj.status = "At Hub"

    # Print package status
    if package_obj.status == "Delivered":
        print(f"[Package ID: {package_obj.package_id}] Status: {package_obj.status} at "
              f"{package_obj.delivery_time} || Address: {package_obj.address} || "
              f"City: {package_obj.city} || Zip: {package_obj.zipcode} || Weight: {package_obj.weight} || "
              f"Deadline: {package_obj.deadline} || Delivered By {package_obj.delivered_by}")
    elif package_obj.status == "En route":
        print(f"[Package ID: {package_obj.package_id}] Status: {package_obj.status} || "
              f"Estimated Arrival Time: {package_obj.delivery_time} || Address: {package_obj.address} || "
              f"City: {package_obj.city} || Zip: {package_obj.zipcode} || Weight: {package_obj.weight} || "
              f"Deadline: {package_obj.deadline} || Being Delivered By {package_obj.delivered_by}")
    else:
        print(f"[Package ID: {package_obj.package_id}] Status: {package_obj.status} || "
              f"Departure Time: {package_obj.departure_time} || Address: {package_obj.address} || "
              f"City: {package_obj.city} || Zip: {package_obj.zipcode} || Weight: {package_obj.weight} || "
              f"Deadline: {package_obj.deadline} || To Be Delivered By {package_obj.delivered_by}")


# Method to get a general report at the given time
def general_report(packages, user_time):
    # Loop through all the packages in the hash map
    for package in packages.table:
        for entry in package:  # Check each entry in the bucket
            package_obj = entry[1]
            # Print status
            print_package_status(package_obj, user_time)


# Method to get a report of a specific package at a given time #LOOKUP FUNCTION!!!!
def package_query(packages_hash, inpt, user_time):
    try:
        # Convert the input to integer
        package_id = int(inpt)
        # Lookup package by ID in the hash map
        package_obj = packages_hash.lookup(package_id)
        # Print status
        print_package_status(package_obj, user_time)
    except ValueError:
        print("Please enter a valid numeric package ID.")


# Get the mileage driven at given time
def truck_mileage(truck, user_time):
    # Check if the truck has already departed
    if truck.departure_time <= user_time:
        # Calculate the elapsed time since departure
        elapsed_time = user_time - truck.departure_time
        # Calculate the mileage at this specific time
        # Truck speed is 18 miles per hour
        mileage_at_time = (elapsed_time.total_seconds() / 3600) * 18
        # Ensure that we don't exceed the total mileage
        mileage_at_time = min(mileage_at_time, truck.total_mileage)
        return mileage_at_time
    else:
        # If the truck hasn't left the hub:
        return 0.0


# Method to get the total mileage of all trucks at the given time
def total_mileage_at_time(trucks, user_time):
    total_mileage = 0.0
    for truck in trucks:
        total_mileage += truck_mileage(truck, user_time)
    return total_mileage


# Main Menu UI
def main_menu_option():
    print("------------------------------------------------")
    print("| WESTERN GOVERNORS UNIVERSITY PARCEL SERVICES |")
    print("------------------------------------------------")
    print("Please select a menu option:")
    print("1. General Report")
    print("2. Package Query")
    print("3. Summary of all Trucks")
    print("4. Exit")


# Main function
def main():
    # Load all data
    CSV_Distance, CSV_Address, CSV_Package = load_data()

    # Initialize the packages hash map
    packages = load_package_data("packages.csv")

    # Driver objects
    driver1 = DeliveryDriver(101)
    driver2 = DeliveryDriver(102)

    # Package lists for trucks
    package_list1 = [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40]
    package_list2 = [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39]
    package_list3 = [2, 4, 5, 7, 8, 9, 10, 11, 25, 28, 32, 33]

    # Calculate weights
    total_weight1 = calculate_weight(package_list1, packages)
    total_weight2 = calculate_weight(package_list2, packages)
    total_weight3 = calculate_weight(package_list3, packages)

    # Create trucks
    truck1 = Truck(driver1, 1,16, 18, total_weight1, package_list1, 0.0, "4001 South 700 East", datetime.timedelta(hours=8))
    truck2 = Truck(driver2, 2,16, 18, total_weight2, package_list2, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))
    truck3 = Truck(None, 3,16, 18, total_weight3, package_list3, 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))

    # Assign trucks to drivers
    driver1.assign_truck([truck1])
    driver2.assign_truck([truck2])

    # MAIN MENU PROMPT
    main_menu_option()
    user_input1 = input("\nEnter your selection here: ")
    if user_input1 == "4": # Menu option 4
        exit(0)

    user_time = get_user_time()
    check_and_update_package_9([truck3], packages, user_time) # Correct Package 9's address after 10:20

    # Deliver packages using nearest neighbor algorithm
    delivering_packages(truck1, packages, CSV_Distance, CSV_Address)
    delivering_packages(truck2, packages, CSV_Distance, CSV_Address)

    # Assign driver to Truck 3
    driver1.remove_truck()
    driver1.assign_truck([truck3])

    # Deliver Truck 3's packages (Delayed due to package 9)
    delivering_packages(truck3, packages, CSV_Distance, CSV_Address)

    # Menu option 1
    if user_input1 == "1":
        print(f"\nDelivery Status at: {user_time}")
        general_report(packages, user_time)
        print(f"Truck 1 mileage at {user_time}: {truck_mileage(truck1, user_time)}")
        print(f"Truck 2 mileage at {user_time}: {truck_mileage(truck2, user_time)}")
        print(f"Truck 3 mileage at {user_time}: {truck_mileage(truck3, user_time)}")
        print(f"\nThe total mileage of all trucks at {user_time} is {total_mileage_at_time([truck1,truck2,truck3], user_time)}")

    # Menu option 2
    if user_input1 == "2":
        user_pck = input("Input Package ID: ")
        package_query(packages, user_pck, user_time)

    # Menu option 3
    if user_input1 == "3":
        print("\nTruck Summary:")
        print(truck1)
        print(truck2)
        print(truck3)


if __name__ == "__main__":
    main()