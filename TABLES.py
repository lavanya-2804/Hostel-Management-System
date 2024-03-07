import mysql.connector

# Establish database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yoursqlpassword",
    database="hostel"
)

# Create cursor
cursor = db.cursor()

# Create departments table
cursor.execute("""
    CREATE TABLE departments (
        department_name VARCHAR(255) PRIMARY KEY,
        fees FLOAT
    )
""")

# Insert initial department data
departments_data = [
    ("CSE", 12000.0),
    ("ECE", 10000.0),
    ("MECH", 15000.0),
    ("CIVIL", 13000.0)
]
cursor.executemany("""
    INSERT INTO departments (department_name, fees)
    VALUES (%s, %s)
""", departments_data)

# Create rooms table
cursor.execute("""
    CREATE TABLE rooms (
    room_no INT PRIMARY KEY,
    max_occupancy INT,
    is_occupied BOOLEAN
    )
""")

# Insert initial room data
rooms_data = [(101,), (102,), (103,), (104,), (105,)]
cursor.executemany("""
    INSERT INTO rooms (room_no)
    VALUES (%s)
""", rooms_data)
room_data = [
    (101, 2),
    (102, 3),
    (103, 2),
    (104, 4),
    (105, 3)
]
# Update max_occupancy values for each room
for room in room_data:
    room_no, max_occupancy = room
    update_query = "UPDATE rooms SET max_occupancy = %s WHERE room_no = %s"
    cursor.execute(update_query, (max_occupancy, room_no))

# Commit the changes to the database
db.commit()

# Close the database connection
db.close()

update_query = "UPDATE rooms SET max_occupancy = %s WHERE room_no = %s"
cursor.executemany(update_query, room_data)
# Create students table
cursor.execute("""
    CREATE TABLE students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        roll_no VARCHAR(10),
        department VARCHAR(255),
        room_no INT,
        fees_paid FLOAT,
        fees_due FLOAT,
        FOREIGN KEY (department) REFERENCES departments(department_name),
        FOREIGN KEY (room_no) REFERENCES rooms(room_no)
    )
""")

# Commit the changes to the database
db.commit()

# Close the database connection
db.close()

print("Tables created successfully.")
