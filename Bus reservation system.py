# -*- coding: utf-8 -*-


# Commented out IPython magic to ensure Python compatibility.
# %load_ext sql

# Commented out IPython magic to ensure Python compatibility.
# %%sql
# sqlite:///BUS.db

import sqlite3

from datetime import date, timedelta

current_date = date.today()
next_day = current_date + timedelta(days=1)

conn = sqlite3.connect('BUS.db')

conn.execute('''
CREATE TABLE BUS_DETAILS(bus_id CHAR(5) NOT NULL PRIMARY KEY, bus_company VARCHAR(15), from_station VARCHAR(15), to_station VARCHAR(15),
capacity INTEGER, departure_time TIME, arrival_time TIME, economy_price FLOAT, business_price FLOAT);
''')

conn.commit()
print("BUS_DETAILS Table created.")

conn.execute('''
CREATE TABLE STATION_DETAILS(station_id CHAR(3), station_location VARCHAR(15), bus_id CHAR(5),
FOREIGN KEY(bus_id) REFERENCES BUS_DETAILS(bus_id) ON DELETE CASCADE ON UPDATE CASCADE, PRIMARY KEY(station_id, bus_id));
''')

conn.commit()
print("STATION_DETAILS Table created.")

conn.execute('''
CREATE TABLE LOGIN_DETAILS(customer_id CHAR(5) NOT NULL PRIMARY KEY, customer_name VARCHAR(25), customer_phone CHAR(10) UNIQUE, customer_password VARCHAR(15));
''')

conn.commit()
print("LOGIN_DETAILS Table created.")

conn.execute('''
CREATE TABLE SEATING_DETAILS(seat_type VARCHAR(10) PRIMARY KEY, luggage_limit VARCHAR(5), cancellation_charge FLOAT, meal_provided VARCHAR(5));
''')
conn.commit()
print("SEATING_DETAILS Table created.")

conn.execute('''INSERT INTO BUS_DETAILS VALUES("B001", "StarBus", "New York", "Boston", 50, "08:00:00", "12:00:00", 30.00, 50.00);''')
conn.execute('''INSERT INTO BUS_DETAILS VALUES("B002", "Greyhound", "San Francisco", "Los Angeles", 40, "09:30:00", "14:00:00", 25.00, 45.00);''')
conn.execute('''INSERT INTO BUS_DETAILS VALUES("B003", "Megabus", "Chicago", "Washington", 60, "10:00:00", "18:00:00", 35.00, 55.00);''')

conn.execute('''INSERT INTO STATION_DETAILS VALUES("NY1", "New York Bus Station", "B001");''')
conn.execute('''INSERT INTO STATION_DETAILS VALUES("BOS1", "Boston Bus Station", "B001");''')
conn.execute('''INSERT INTO STATION_DETAILS VALUES("SF1", "San Francisco Bus Station", "B002");''')
conn.execute('''INSERT INTO STATION_DETAILS VALUES("LA1", "Los Angeles Bus Station", "B002");''')
conn.execute('''INSERT INTO STATION_DETAILS VALUES("CHI1", "Chicago Bus Station", "B003");''')
conn.execute('''INSERT INTO STATION_DETAILS VALUES("WAS1", "Washington Bus Station", "B003");''')

conn.execute('''INSERT INTO LOGIN_DETAILS VALUES("C001", "Sarthak", "1234567890", "password123");''')
conn.execute('''INSERT INTO LOGIN_DETAILS VALUES("C002", "Anant", "8797495485", "aster");''')

conn.execute('''
CREATE TABLE BOOKING_DETAILS(
    booking_id CHAR(5) NOT NULL PRIMARY KEY,
    booking_date DATE,
    customer_id CHAR(5),
    passenger_count INTEGER,
    bus_id CHAR(5),
    departure_date DATE,
    seat_type VARCHAR(10),
    FOREIGN KEY(customer_id) REFERENCES LOGIN_DETAILS(customer_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(bus_id) REFERENCES BUS_DETAILS(bus_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(seat_type) REFERENCES SEATING_DETAILS(seat_type) ON DELETE CASCADE ON UPDATE CASCADE
);
''')
conn.commit()

conn.execute('''INSERT INTO SEATING_DETAILS VALUES("Standard", "20kg", 10.00, "No");''')
conn.execute('''INSERT INTO SEATING_DETAILS VALUES("Premium", "30kg", 15.00, "Yes");''')

cursor = conn.execute("SELECT * FROM BUS_DETAILS")
print("BUS_DETAILS Table:")
for row in cursor:
    print(row)

cursor = conn.execute("SELECT * FROM STATION_DETAILS")
print("\nSTATION_DETAILS Table:")
for row in cursor:
    print(row)

cursor = conn.execute("SELECT * FROM LOGIN_DETAILS")
print("\nLOGIN_DETAILS Table:")
for row in cursor:
    print(row)

cursor = conn.execute("SELECT * FROM SEATING_DETAILS")
print("\nSEATING_DETAILS Table:")
for row in cursor:
    print(row)

def create_login():
    print("Create Login Details")
    customer_name = input("Enter your name: ")
    customer_phone = input("Enter your phone number: ")
    customer_password = input("Create a password: ")

    # Generate a unique customer ID (You may use your own logic for generating IDs)
    customer_id = "C" + str(len(conn.execute("SELECT * FROM LOGIN_DETAILS").fetchall()) + 1).zfill(3)

    conn.execute('''INSERT INTO LOGIN_DETAILS VALUES(?,?,?,?)''', (customer_id, customer_name, customer_phone, customer_password))
    conn.commit()
    print("Login details created successfully!")
    return customer_id

def make_reservation(customer_id):
    print("\nAvailable Buses:")
    cursor = conn.execute("SELECT bus_id, bus_company, from_station, to_station, economy_price FROM BUS_DETAILS")
    for row in cursor:
        print(row)

    bus_choice = input("\nEnter the Bus ID to make a reservation: ")
    seat_type = input("Enter seat type (Standard/Premium): ")
    passenger_count = int(input("Enter the number of passengers: "))

    # Generate a unique booking ID
    booking_id = "BI" + str(len(conn.execute("SELECT * FROM BOOKING_DETAILS").fetchall()) + 1).zfill(3)

    conn.execute('''INSERT INTO BOOKING_DETAILS (booking_id, booking_date, customer_id, passenger_count, bus_id, departure_date, seat_type)
                 VALUES (?,?,?,?,?,?,?)''',
                 (booking_id, current_date, customer_id, passenger_count, bus_choice, next_day, seat_type))
    conn.commit()
    print("Reservation successfully made!")
    print(booking_id)
    return booking_id

def get_booking_details(booking_id):
    cursor = conn.execute("SELECT * FROM BOOKING_DETAILS WHERE booking_id=?", (booking_id,))
    booking_details = cursor.fetchone()

    if booking_details:
        print("Booking Details:")
        print(f"Booking ID: {booking_details[0]}")
        print(f"Booking Date: {booking_details[1]}")
        print(f"Customer ID: {booking_details[2]}")
        print(f"Passenger Count: {booking_details[3]}")
        print(f"Bus ID: {booking_details[4]}")
        print(f"Departure Date: {booking_details[5]}")
        print(f"Seat Type: {booking_details[6]}")
        # Add more details as needed based on your table structure

        # You can also return the booking_details if required
        return booking_details
    else:
        print("Booking ID not found.")

print("Welcome to the Bus Reservation System")
login_option = input("Do you have an account? (yes/no): ")

if login_option.lower() == "no":
    customer_id = create_login()
elif login_option.lower() == "yes":
    customer_phone = input("Enter your phone number: ")
    customer_password = input("Enter your password: ")

    # Check if login credentials are valid
    cursor = conn.execute("SELECT customer_id FROM LOGIN_DETAILS WHERE customer_phone=? AND customer_password=?",
                          (customer_phone, customer_password))
    result = cursor.fetchone()

    if result:
        customer_id = result[0]
        print(f"Login successful! Your customer ID is {customer_id}")
    else:
        print("Invalid login credentials. Please try again.")
        # Implement retry logic or other actions

if 'customer_id' in locals():
    reservation_option = input("\nDo you want to make a reservation? (yes/no): ")
    if reservation_option.lower() == "yes":
        make_reservation(customer_id)
    else:
        print("Thank you for using the Bus Reservation System.")
else:
    print("Exiting the system. Have a good day!")
booking_id_input = input("Enter your Booking ID to view details: ")
get_booking_details(booking_id_input)
