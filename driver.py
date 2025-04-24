class DeliveryDriver:
    # Initializes a DeliveryDriver with a unique ID
    def __init__(self, id_number):
        self.id_number = id_number
        self.assigned_truck = None

    # Attempts to assign a truck from the available list to this driver
    def assign_truck(self, available_trucks):
        # Loop through the list of trucks to find one that isn't already assigned
        for truck in available_trucks:
            if truck.assigned_driver is None:
                truck.assigned_driver = self
                self.assigned_truck = truck
                return True
        return False

    # Unassigns the truck from this driver, making it available again
    def remove_truck(self):
        if self.assigned_truck:
            self.assigned_truck.assigned_driver = None
            self.assigned_truck = None

    def get_truck(self):
        return self.assigned_truck

    def __repr__(self):
        # Return a string representation of the driver, which includes the driver ID
        return f"{self.id_number}"