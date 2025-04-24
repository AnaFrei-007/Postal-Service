import csv

class Package:
    def __init__(self, package_id, address, city, state, zipcode, deadline, weight, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None
        self.delivered_by = None

    def __repr__(self):
        return f"[Package ID: {self.package_id}]  Address: {self.address}, City: {self.city}, State: {self.state}, " \
               f"Zip: {self.zipcode}, Deadline: {self.deadline}, Weight: {self.weight}, " \
               f"Delivery Time: {self.delivery_time}, Status: {self.status}, Delivered By: {self.delivered_by}"

    def get_weight(self):
        return int(self.weight)

    def set_delivered_by(self, truck):
        self.delivered_by = truck

    def update_address(self, new_address, new_city, new_state, new_zip):
        self.address = new_address
        self.city = new_city
        self.state = new_state
        self.zipcode = new_zip
