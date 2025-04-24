from main import calculate_distance, get_address
import datetime


class Truck:
    def __init__(self, assigned_driver, truck_id, max_capacity, travel_speed, current_load, package_list, total_mileage, address, departure_time):
        self.assigned_driver = assigned_driver
        self.truck_id = truck_id
        self.max_capacity = max_capacity
        self.travel_speed = travel_speed
        self.current_load = current_load
        self.package_list = package_list
        self.total_mileage = total_mileage
        self.address = address
        self.departure_time = departure_time
        self.time_of_departure = departure_time
        self.hub_address = "4001 South 700 East"

    def __repr__(self):
        return f"Driver: {self.assigned_driver}, Max Capacity: {self.max_capacity}, Speed: {self.travel_speed}, Load: {self.current_load}, " \
               f"Packages: {self.package_list}, Mileage: {self.total_mileage}, Location: {self.address}, Departure: {self.departure_time}"

    def get_mileage(self):
        return self.total_mileage

    def update_mileage(self, distance):
        self.total_mileage += distance

    def remove_package(self, package):
        if package in self.package_list:
            self.package_list.remove(package)
            self.current_load -= self.package_list[package.weight]

    def get_truck_id(self):
        return f"Truck {self.truck_id}"

    def return_to_hub(self, CSV_Distance, CSV_Address):
        return_distance = calculate_distance(get_address(self.address, CSV_Address),
                                             get_address(self.hub_address, CSV_Address), CSV_Distance)

        # Update truck's mileage and address when it returns to the hub
        self.total_mileage += return_distance
        self.address = self.hub_address
        self.time_of_departure += datetime.timedelta(hours=return_distance / self.travel_speed)

        #print(f"Truck {self.truck_id} returned to the hub at {self.time_of_departure}")
