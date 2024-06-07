import csv
import pymysql
import maskpass

class StudentManagementSystem:
    def __init__(self):
        self.connection = pymysql.connect(host="localhost",
                                          user="root",
                                          password="",
                                          database='student_db')
        self.cursor = self.connection.cursor()


    def login(self, username, password):
        try:
            self.cursor.execute("SELECT * FROM admins WHERE username=%s AND password=%s", (username, password))
            admin = self.cursor.fetchone()
            if admin:
                print("Login successful. Welcome,", username)
                return True
            else:
                print("Invalid username or password.")
                return False
        except Exception as e:
            print("Error during login:", e)


    def add_student(self, rollno, name, email, gender, contact, dob, address, course):
        
        """
    Add a new student to the database.

    Parameters:
    roll_no (int): The unique roll number of the student.
    name (str): The name of the student.
    email (str): The email address of the student.
    gender (str): The gender of the student.
    contact (str): The contact number of the student.
    dob (str): The date of birth of the student in the format 'DD-MM-YYYY'.
    address (str): The address of the student.
    course (str): The course the student is enrolled in.

    Returns:
    None

    Raises:
    Exception: If an error occurs while adding the student to the database.

    This method first checks if the roll number already exists in the database. If it does, an error message is printed and the method returns without adding the student. If the roll number is unique, the method inserts the student's details into the 'students' table of the database and commits the changes. Finally, a success message is printed.
    """
        try:
            # Check if the roll number already exists
            self.cursor.execute("SELECT COUNT(*) FROM students WHERE rollno=%s", (rollno,))
            count = self.cursor.fetchone()[0]
            
            if count > 0:
                print("Roll number already exists. Please enter a unique roll number.")
                return
            self.cursor.execute("INSERT INTO students (rollno, name, email, gender, contact, dob, address, course) VALUES (%s, %s, %s, %s, %s, STR_TO_DATE(%s, '%%d-%%m-%%Y'), %s, %s)",
                                (rollno, name, email, gender, contact, dob, address, course))
            self.connection.commit()
            print("Student added successfully")
        except Exception as e:
            print("Error adding student:", e)

    def export_student_data_to_csv(self, file_name):
        try:
           
            self.cursor.execute("SELECT * FROM students")
            
            rows = self.cursor.fetchall()
            
            with open(file_name, 'w', newline='') as file:
        
                csv_writer = csv.writer(file)
                
                csv_writer.writerow([i[0] for i in self.cursor.description])
                
                # Write each row of data to the CSV file
                csv_writer.writerows(rows)
            
            print("Student data exported successfully to", file_name)
            
        except Exception as e:
            print("Error exporting student data:", e)


    def delete_student(self, roll_no):
        try:
            # Check if the roll number exists
            self.cursor.execute("SELECT * FROM students WHERE roll_no=%s", (roll_no,))
            student = self.cursor.fetchone()
            if student:
                # Roll number exists, proceed with deletion
                self.cursor.execute("DELETE FROM students WHERE roll_no=%s", (roll_no,))
                self.connection.commit()
                print("Student deleted successfully")
            else:
                # Roll number does not exist
                print("Roll number not present in database.")
        except Exception as e:
            print("Error deleting student:", e)


    def update_student(self, rollno, name, email, gender, contact, dob, address, course):
        try:
            self.cursor.execute("UPDATE students SET name=%s, email=%s, gender=%s, contact=%s, dob=STR_TO_DATE(%s, '%%d-%%m-%%Y'), address=%s, course=%s WHERE rollno=%s",
                                (name, email, gender, contact, dob, address, course, rollno))
            self.connection.commit()
            print("Student updated successfully")
        except Exception as e:
            print("Error updating student:", e)

    def search_student(self, search_term, search_by="rollno"):
        try:
            if search_by == "rollno":
                self.cursor.execute("SELECT * FROM students WHERE rollno=%s", (search_term,))
            elif search_by == "email":
                self.cursor.execute("SELECT * FROM students WHERE email=%s", (search_term,))
            else:
                print("Invalid search option. Please choose 'rollno' or 'email'.")

            student = self.cursor.fetchone()
            if student:
                print("Student found:")
                print("Roll No.: ", student[0])
                print("Name: ", student[1])
                print("Email: ", student[2])
                print("Gender: ", student[3])
                print("Contact: ", student[4])
                print("Date of Birth: ", student[5])
                print("Address: ", student[6])
                print("Course: ", student[7])
            else:
                print("Student not found.")
        except Exception as e:
            print("Error searching for student:", e)

    def close_connection(self):
        self.connection.close()

def main():
    """
    This function is the entry point of the StudentManagementSystem application.
    It displays a menu to the user and calls the appropriate methods based on the user's choice.

    Parameters:
    None

    Returns:
    None

    Raises:
    None
    """   
    student_mgmt_system = StudentManagementSystem()

    # Login
    username = input("Enter username: ")
    password = maskpass.askpass("Enter Password : ")
    if not student_mgmt_system.login(username, password):
        print("Login failed. Exiting...")
        return

while True:
        

    print("Student Management System Menu:")
    print("1. Add Student")
    print("2. Update Student")
    print("3. Delete Student")
    print("4. Search Student ")
    print("5. Export Student Data to CSV")
    print("6. Exit")

    option = input("Enter your choice (1-6): ")

    if option == "1":
        rollno = int(input("Enter Roll No.: "))
        name = input("Enter Name: ")
        email = input("Enter Email: ")
        gender = input("Enter Gender: ")
        contact = input("Enter Contact: ")
        dob = input("Enter Date of Birth (DD-MM-YYYY): ")
        address = input("Enter Address: ")
        course = input("Enter Course: ")
        student_mgmt_system.add_student(rollno, name, email, gender, contact, dob, address, course)
    elif option == "2":
        rollno = int(input("Enter Roll No. of student to update: "))
        name = input("Enter New Name: ")
        email = input("Enter New Email: ")
        gender = input("Enter New Gender: ")
        contact = input("Enter New Contact: ")
        dob = input("Enter New Date of Birth (DD-MM-YYYY): ")
        address = input("Enter New Address: ")
        course = input("Enter New Course: ")
        student_mgmt_system.update_student(rollno, name, email, gender, contact, dob, address, course)
    elif option == "3":
        rollno = int(input("Enter Roll No. of student to delete: "))
        student_mgmt_system.delete_student(rollno)
    elif option == "4":
        print("Search Student Menu:")
        print("1. Search by Roll No.")
        print("2. Search by Email")
        search_option = input("Enter your choice (1-2): ")
        if search_option == "1":
            rollno = input("Enter Roll No. to search: ")
            student_mgmt_system.search_student(rollno, "rollno")
        elif search_option == "2":
            email = input("Enter Email ID to search: ")
            student_mgmt_system.search_student(email, "email")
        else:
            print("Invalid search option. Please enter 1 or 2.")
    elif option == "5":
        file_name = input("Enter CSV file name: ")
        student_mgmt_system.export_student_data_to_csv(file_name)
    elif option == "6":
        print("Exiting...")
        student_mgmt_system.close_connection()
        sys.exit()
    else:
        print("Invalid option. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
