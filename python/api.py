import sqlite3
from flask import *
import json
from cars import AllCars

app = Flask(__name__)

def go_home():
    c = sqlite3.connect('cars.db').cursor()

    c.execute('CREATE TABLE IF NOT EXISTS CARS'
                "(id TEXT,  car_name TEXT, car_price TEXT, description, TEXT, car_seats TEXT, car_gear TEXT, car_fuel TEXT)" 
    )
    c.connection.close()

@app.route('/', methods=['GET', 'POST'])
def go__home_index():
    go_home()
    return 'Welcome to the Cars API'

@app.route('/getCars', methods=['GET'])
def get_go_cars():
    c = sqlite3.connect('cars.db').cursor()
    c.execute('SELECT * FROM CARS')
    data = c.fetchall()
    return jsonify(data)

@app.route('getCarsById/<cars_id>', methods=['GET'])
def get_go_cars_by_id(cars_id):
    c = sqlite3.connect('cars.db').cursor()
    c.execute('SELECT * FROM CARS WHERE id=?', (cars_id))
    data = c.fetchone()
    return json.dumps(data)

@app.route('/addCars', methods=['POST', 'GET'])
def add_go_car():
    db = sqlite3.connect('cars.db')
    c = db.cursor()
    cars = AllCars(
        request.form['car_name'],
        request.form['car_price'],
        request.form['description'],
        request.form['car_seats'],
        request.form['car_gear'],
        request.form['car_fuel'],

    )
    print(cars)
    c.execute("INSERT INFO CARS VALUES(?,?,?,?,?,?)",
              (cars.car_name, cars.car_price, cars.description, cars.car_seats, cars.car_gear, cars.car_fuel))
    db.commit()
    data = c.lastrowid
    return json.dumps(data)

@app.route('/updateCars/<cars_id>', methods=['PUT'])
def update_go_cars(cars_id):
    db = sqlite3.connect('cars.db')
    c = db.cursor()
    cars = AllCars(
        request.form['car_name'],
        request.form['car_price'],
        request.form['description'],
        request.form['car_seats'],
        request.form['car_gear'],
        request.form['car_fuel'],
    )

    print(cars)
    c.execute('UPDATE CARS SET car_name=?, car_price=?, description=?, car_seats=?, car_gear=?, car_fuel=? WHERE id=?',
    (cars.id, cars.car_name, cars.car_price, cars.description, cars.car_seats, cars.car_gear, cars.car_fuel))
    db.commit()
    return json.dumps("Record was succesfully updated")

@app.route('/deleteCars/<cars_id>', methods=['DELETE'])
def delete_go_cars(cars_id):
    db = sqlite3.connect('cars.db')
    c = db.cursor()
    c.execute('DELETE FROM CARS WHERE id=?', (cars_id,))
    db.commit()
    return json.dumps('Record was successfully deleted')

if __name__ == '__main__':
    app.run(debug=True)