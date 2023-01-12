import uuid

class AllCars:

    def __init__(self, id, car_name, car_type, car_price, description, car_seats, car_gear, car_fuel):
        self.id = uuid.uuid4.hex
        self.car_name = car_name
        self.car_type = car_type
        self.car_price = car_price
        self.description = description
        self.car_seats = car_seats
        self.car_gear = car_gear
        self.car_fuel = car_fuel

    def __str__(self):
        return f'''
                    id:{self.id}
                    car_name:{self.car_name}
                    car_price:{self.car_price}
                    description:{self.description}
                    car_seats:{self.car_seats}
                    car_gear:{self.car_gear}
                    car_fuel:{self.car_fuel}
                
                '''

