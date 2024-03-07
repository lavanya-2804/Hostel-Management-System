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

# Function to add a new student
def add_student():
    name = input("Enter student name: ")
    roll_no = input("Enter student roll number: ")
    
    # Display available departments
    cursor.execute("SELECT department_name FROM departments")
    departments = cursor.fetchall()
    print("Available Departments:")
    for department in departments:
        print(department[0])
        
    department = input("Enter student department: ")
    
    # Retrieve the department's fees from the database
    cursor.execute("""
        SELECT fees FROM departments
        WHERE department_name = %s
    """, (department,))
    result = cursor.fetchone()
    
    if result:
        fees = float(result[0])
    else:
        print("Department not found.")
        return

    # Insert the student record into the database
    cursor.execute("""
        INSERT INTO students (name, roll_no, department, room_no, fees_paid, fees_due)
        VALUES (%s, %s, %s, NULL, 0.0, %s)
    """, (name, roll_no, department, fees))

    # Commit the changes to the database
    db.commit()

    print("Student added successfully.")

# Function to assign rooms to students
def assign_rooms():
    # Retrieve students without assigned rooms
    cursor.execute("SELECT id, department FROM students WHERE room_no IS NULL")
    unassigned_students = cursor.fetchall()

    # Retrieve vacant rooms by department
    cursor.execute("SELECT room_no, max_occupancy FROM rooms WHERE is_occupied = 0")
    vacant_rooms = cursor.fetchall()

    # Assign rooms to students based on department and availability
    for student in unassigned_students:
        student_id, department = student

        # Find a vacant room with matching department
        assigned_room = None
        for room in vacant_rooms:
            room_no, max_occupancy = room
            if max_occupancy > 0 and department == "CSE":
                assigned_room = room_no
                max_occupancy -= 1
                vacant_rooms.remove(room)
                vacant_rooms.append((room_no, max_occupancy))
                break

        # Update the student's assigned room in the database
        if assigned_room:
            update_query = "UPDATE students SET room_no = %s WHERE id = %s"
            cursor.execute(update_query, (assigned_room, student_id))

    # Commit the changes to the database
    db.commit()

    print("Rooms assigned successfully.")

# Function to manage fees
def manage_fees():
    student_id = input("Enter student ID: ")
    fees_paid = float(input("Enter fees paid: "))

    # Retrieve the student's department and total fees from the database
    cursor.execute("""
        SELECT department, fees FROM students
        INNER JOIN departments ON students.department = departments.department_name
        WHERE students.id = %s
    """, (student_id,))
    result = cursor.fetchone()
    
    if result:
        department = result[0]
        total_fees = float(result[1])
    else:
        print("Student not found.")
        return

    # Calculate the new fees_due
    fees_due = max(0.0, total_fees - fees_paid)

    # Update the fees_paid and fees_due fields for the student in the database
    cursor.execute("""
        UPDATE students
        SET fees_paid = fees_paid + %s,
            fees_due = %s
        WHERE id = %s
    """, (fees_paid, fees_due, student_id))

    # Commit the changes to the database
    db.commit()

    print("Fees managed successfully.")

# Function to get student information
def get_student_information():
    student_id = input("Enter student ID: ")

    # Retrieve the student's information from the database
    cursor.execute("""
        SELECT * FROM students
        WHERE id = %s
    """, (student_id,))
    result = cursor.fetchone()

    if result:
        print("Student ID:", result[0])
        print("Name:", result[1])
        print("Roll Number:", result[2])
        print("Department:", result[3])
        print("Room Number:", result[4])
        print("Fees Paid:", result[5])
        print("Fees Due:", result[6])
    else:
        print("Student not found.")

# Main program loop
while True:
    print("Hostel Management System")
    print("1. Add Student")
    print("2. Assign Room")
    print("3. Manage Fees")
    print("4. Get Student Information")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        add_student()
    elif choice == "2":
        assign_rooms()
    elif choice == "3":
        manage_fees()
    elif choice == "4":
        get_student_information()
    elif choice == "5":
        break
    else:
        print("Invalid choice. Please try again.")

# Close the database connection
db.close()

print("Exiting Hostel Management System.")
