from fastapi import FastAPI
from enum import Enum

app = FastAPI()


class CarType(str, Enum):
    minivan = 'minivan'
    sedan = 'sedan'
    station_wagon = 'station wagon'
    limousine = 'limousine'
    hatchback = 'hatchback'
    coupe = 'coupe'
    pickup_truck = 'pickup truck'


class Gender(str, Enum):
    male = 'male'
    female = 'female'


class PayType(str, Enum):
    card = 'card'
    cash = 'cash'


class Status(str, Enum):
    on_the_way = 'on the way'
    wait_passenger = 'wait passenger'
    done = 'done'
    cancel = 'cancel'


DataClients = {
    1: {'number': 88001112233, 'fullname': 'Romanov Roman Romanovich', 'payment': 'cash'},
    2: {'number': 88002223344, 'fullname': 'Sokolov Semyon Sokolovich', 'payment': 'card'},
    3: {'number': 88003334455, 'fullname': 'Bukin Bogdan Bukinich', 'payment': 'cash'}
}

DataCars = {
    1: {'brand_car': 'Audi', 'state_number': 'оо151о', 'color': 'black', 'car_type': 'minivan'},
    2: {'brand_car': 'BMW', 'state_number': 'а111ач', 'color': 'red', 'car_type': 'sedan'},
    3: {'brand_car': 'Mercedes-Benz', 'state_number': 'м916сх', 'color': 'white', 'car_type': 'station wagon'},
    4: {'brand_car': 'Lexus', 'state_number': 'в004ко', 'color': 'blue', 'car_type': 'limousine'},
    5: {'brand_car': 'Kia', 'state_number': 'б666ух', 'color': 'green', 'car_type': 'hatchback'}
}

DataDrivers = {
    1: {'name': 'Kuznetsov Kuzma Kuznetsovich', 'gender': 'male', 'phone': 7777777, 'car': 3},
    2: {'name': 'Voronin Vasily Voronovich', 'gender': 'male', 'phone': 9999999, 'car': 2},
    3: {'name': 'Kirillova Kira Kirillovna', 'gender': 'female', 'phone': 6666666, 'car': 1}
}

DataOrders = {
    1: {"client": 1, "status": "on the way", "departure_address": 'Lenin 31', "destination_address": 'Amunsena 43', "driver": 1},
    2: {"client": 2, "status": "wait passenger", "departure_address": 'AutoMagistral 32', "destination_address": '8 Marth 111', "driver": 2},
    3: {"client": 3, "status": "wait passenger", "departure_address": 'Vainera 15', "destination_address": 'Mira 32', "driver": 3}
}


##      CLIENTS
@app.get("/clients", tags=["clients"])
def get_Clients():
    return DataClients


@app.post("/clients/", tags=["clients"])
def add_Client(fullname: str, phone: str, payment: PayType):
    newId = len(DataClients.keys()) + 1
    DataClients[newId] = {'fullname': fullname, "phone": phone, 'payment': payment}
    return DataClients


@app.get("/clients/{ClientId}", tags=["clients"])
def get_Client(ClientId: int):
    return DataClients[ClientId]


@app.put("/clients/{ClientId}", tags=["clients"])
def update_Client(ClientId: int, phone: str, fullname: str, payment: PayType):
    DataClients[ClientId] = {'fullname': fullname, "phone": phone, 'payment': payment}
    return DataClients


@app.delete("/clients/{ClientId}", tags=["clients"])
def delete_Client(ClientId: int):
    del DataClients[ClientId]
    return DataClients


##      CARS

@app.get("/cars", tags=["cars"])
def get_Cars():
    return DataCars


@app.post("/cars/", tags=["cars"])
def add_Car(brand_car: str, state_number: str, color: str, car_type: CarType):
    newId = len(DataCars.keys()) + 1
    DataCars[newId] = {'brand_car': brand_car, 'state_number': state_number, 'color': color, 'car_type': car_type}
    return DataCars


@app.get("/cars/{CarId}", tags=["cars"])
def get_Car(CarId: int):
    return DataCars[CarId]


@app.put("/cars/{CarId}", tags=["cars"])
def update_Car(CarId: int, brand_car: str, state_number: str, color: str, car_type: CarType):
    DataCars[CarId] = {'brand_car': brand_car, 'state_number': state_number, 'color': color, 'car_type': car_type}
    return DataCars


@app.delete("/cars/{CarId}", tags=["cars"])
def delete_Car(CarId: int):
    del DataCars[CarId]
    return DataCars


##      DRIVERS

@app.get("/drivers", tags=["drivers"])
def get_Drivers():
    return DataDrivers


@app.post("/drivers/", tags=["drivers"])
def add_Driver(name: str, gender: Gender, phone: int, car_id: int):
    if car_id not in DataCars.keys():
        return {"Error": f"Автомобиль с идентификатором {car_id} не найден"}
    for driver in DataDrivers.values():
        if driver['car'] == car_id:
            return {"Error": "Автомобиль уже закреплен за другим водителем"}
    new_driver_id = len(DataDrivers.keys()) + 1
    DataDrivers[new_driver_id] = {'name': name, 'gender': gender, 'phone': phone, 'car': car_id}
    return DataDrivers

@app.get("/drivers/{DriverId}", tags=["drivers"])
def get_Driver(DriverId: int):
    if DriverId not in DataDrivers.keys():
        return {"Error": f"Не найден водитель с идентификатором {DriverId}"}
    car_id = DataDrivers[DriverId]['car']
    car = DataCars[car_id]
    driver = DataDrivers[DriverId]
    driver['car'] = car
    return driver


@app.put("/drivers/{DriverId}", tags=["drivers"])
def update_Driver(DriverId: int,name: str, gender: Gender, phone: int, car_id: int):
    if car_id not in DataCars.keys():
        return {"Error": f"Автомобиль с идентификатором {car_id} не найден"}
    for driver in DataDrivers.values():
        if driver['car'] == car_id:
            return {"Error": "Автомобиль уже закреплен за другим водителем"}
    DataDrivers[DriverId] = {'name': name, 'gender': gender, 'phone': phone, 'car': car_id}
    return DataDrivers


@app.delete("/drivers/{DriverId}", tags=["drivers"])
def delete_Driver(DriverId: int):
    if DriverId not in DataDrivers.keys():
        return {"Error": f"Не найден водитель с идентификатором {DriverId}"}
    del DataDrivers[DriverId]
    new_drivers_data = {}
    for i, (key, driver) in enumerate(DataDrivers.items(), start=1):
        new_drivers_data[i] = driver
    DataDrivers.clear()
    DataDrivers.update(new_drivers_data)
    return DataDrivers


##      ORDERS


@app.get("/orders", tags=["orders"])
def get_Orders():
    return DataOrders


@app.post("/orders/", tags=["orders"])
def add_Order(client: int, status: Status, departure_address: str, destination_address: str, driver: int):
    if client not in DataClients.keys():
        return {"Error": f"Не найден клиент с идентификатором {client}"}
    if driver not in DataDrivers.keys():
        return {"Error": f"Не найден водитель с идентификатором {driver}"}
    new_id = len(DataOrders.keys()) + 1
    DataOrders[new_id] = {'client': client, 'status': status, 'departure_address': departure_address, 'destination_address': destination_address, 'driver': driver}
    return DataOrders


@app.get("/orders/{OrderId}", tags=["orders"])
def get_Order(OrderId: int):
    if OrderId not in DataOrders.keys():
        return {"Error": f"Не найден заказ с идентификатором {OrderId}"}

    driver_id = DataOrders[OrderId]['driver']
    driver = DataDrivers[driver_id]

    car_id = DataDrivers[driver_id]['car']
    car = DataCars[car_id]

    driver['car'] = car

    order = DataOrders[OrderId]
    order['driver'] = driver
    return order


@app.put("/orders/{OrderId}", tags=["orders"])
def update_Order(OrderId: int, status: Status, driver: int):
    if OrderId not in DataOrders.keys():
        return {"Error": f"Заказ с идентификатором {OrderId} не найден"}
    # for order in DataOrders.values():
    #     if order['driver'] == driver:
    #         return {"Error": "Водитель уже закреплен за другим заказом"}
    DataOrders[OrderId] = {'client': DataOrders[OrderId]['client'], 'status': status, 'departure_address':  DataOrders[OrderId]['departure_address'],
                           'destination_address': DataOrders[OrderId]['destination_address'], 'driver': DataOrders[OrderId]['driver']}
    if DataOrders[OrderId]['status'] == 'done' or DataOrders[OrderId]['status'] == 'cancel':
        del DataOrders[OrderId]
        new_orders_data = {}
        for i, (key, order) in enumerate(DataOrders.items(), start=1):
            new_orders_data[i] = order
        DataOrders.clear()
        DataOrders.update(new_orders_data)
        return DataOrders
    return DataOrders

