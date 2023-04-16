from operator import truediv
import time # For .sleep() method
import sys # For .write() mathod
import os # For the clearScreen function
from datetime import datetime
from turtle import clearscreen
import mariadb
import sys

def clearScreen(): # For the clearing of terminal screen
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')
        
def delayPrint(string):
    for char in string:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)

def prompt():
    prompt = input("Please press enter to continue.")
    
def checkIfExists(string, type, forAdd):
    if type:        # Task title
        cur.execute("SELECT * FROM task")
        row = cur.fetchone()
        if row == None and not forAdd: # Returns empty if task list is empty
            return "empty"
        else:
            cur.execute("SELECT * FROM task WHERE title = ?", (string,))
            row = cur.fetchone()
            if row != None:
                return row
            return False
    else:          # Category name
        cur.execute("SELECT * FROM category")
        row = cur.fetchone()
        if row == None and not forAdd: # Returns empty if category list is empty
            return "empty"
        else:
            cur.execute("SELECT * FROM category WHERE category_name = ?", (string,))
            row = cur.fetchone()
            if row != None:
                return row
            return False

def dayChecker():
    monthWith31 = [1, 3, 5, 7, 8, 10, 12]
    isLeapYear = False

    # User Input (Date)
    while True:

        # Month
        deadlineMonth = input("Enter the deadline month[1-12]: ")
        while int(deadlineMonth) > 12 or int(deadlineMonth) < 1:
            deadlineMonth = input("Enter a valid deadline month[1-12]: ")
        
        # Year
        deadlineYear = input("Enter the deadline year: ")
        while len(deadlineYear) != 4:
            deadlineYear = input("Enter a valid deadline year: ")
        if int(deadlineYear) % 4 == 0:
            isLeapYear = True
            
        # Checks for the number of days in a given month
        deadlineDay = input("Enter deadline Day: ")
        if int(deadlineMonth) in monthWith31:
            while int(deadlineDay) > 31 or int(deadlineDay) < 1:
                deadlineDay = input("Enter a valid deadline Day: ")
        elif int(deadlineMonth) not in monthWith31 and int(deadlineMonth) != 2:
            while int(deadlineDay) > 30 or int(deadlineDay) < 1:
                deadlineDay = input("Enter a valid deadline Day: ")

        # Number of days of February based on leap year
        elif int(deadlineMonth) == 2 and isLeapYear == False:
            while int(deadlineDay) > 28 or int(deadlineDay) < 1:
                deadlineDay = input("Enter a valid deadline Day: ")
        elif int(deadlineMonth) == 2 and isLeapYear == True:
            while int(deadlineDay) > 29 or int(deadlineDay) < 1:
                deadlineDay = input("Enter a valid deadline Day: ")
        else:
            while int(deadlineDay) > 30 or int(deadlineDay) < 1:
                deadlineDay = input("Enter a valid deadline Day: ")
        
        # Appends 0 if length of month and day is equal to 1
        if len(deadlineMonth) == 1:
            deadlineMonth = "0" + deadlineMonth
        if len(deadlineDay) == 1:
            deadlineDay = "0" + deadlineDay

        # Checks if user input date is after current date
        deadlineDate = deadlineYear + "-" + deadlineMonth + "-" + deadlineDay
        currentDate = datetime.today().strftime('%Y-%m-%d')
        if deadlineDate >= currentDate:
            break
        else:
            print("Deadline date cannot be before the current date!!\n")
    return deadlineDate

def addTask():
    clearScreen()
    print("Creating Task\n")
    
    # User Inputs (Title && Description)
    title = input("Enter Title: ")

    # Checks for similar task names
    if checkIfExists(title, True, True):
        print("Title already exist!")
        prompt()
        return

    description = input("Enter Description: ")

    # User Inputs (Deadline Date)
    deadlineDate = dayChecker()
    
    try:
        cur.execute("INSERT INTO task (title, description, deadline_date) VALUES (?, ?, ?)", (title, description
    , deadlineDate))
    except mariadb.Error as e:
        print("MariaDB error: {e}")
    
    print("\nTask successfully created.")
    prompt()
            

def editTask():
    clearScreen()
    print("Editing Task\n")
    isEmpty = checkIfExists("random", True, False)
    # Checks if task list is empty
    if isEmpty == "empty":
        print("No records yet!")
        prompt()
        return
    # Lists titles and asks for user input
    titles = viewTaskTitle()
    toEdit = input("Enter the task number to edit: ")
    if toEdit < "1" or toEdit > str(titles):
        print("\nInvalid Choice!")
        prompt()
        clearScreen()
        return
    cur.execute("SELECT * FROM task WHERE task_id = (SELECT task_id FROM task ORDER BY task_id LIMIT ?, ?)",(int(toEdit)-1, 1))
    
    row = cur.fetchone()

    # Edit Task Menu
    while True:
        print("\n")
        print("[1] Edit Title")
        print("[2] Edit Description")
        print("[3] Edit Deadline Date")
        print("[4] Back")

        # User Input (Choice)
        editChoice = input("Enter choice: ")
                    
        # User Edit (Title)
        if editChoice == "1": 
            print("Current Title: " + str(row[1]))
            titleEdit = input("Enter New Title: ")

            row2 = checkIfExists(titleEdit, True, False)
            if row2:
                print("Title already exists!")
                continue

            try:
                cur.execute("UPDATE task SET title = ? WHERE task_id = (SELECT task_id FROM task ORDER BY task_id LIMIT ?, ?)", (titleEdit, int(toEdit)-1, 1))
            except mariadb.Error as e:
                print(f"MariaDB Error : {e}")

        # User Edit (Description)
        elif editChoice == "2":
            print("Current Description: " + str(row[2]))
            descEdit = input("Enter New Description: ")
            try:
                cur.execute("UPDATE task SET description = ? WHERE task_id = (SELECT task_id FROM task ORDER BY task_id LIMIT ?, ?)", (descEdit, int(toEdit)-1, 1))
            except mariadb.Error as e:
                print(f"MariaDB Error : {e}")
            
        # User Edit (Deadline)
        elif editChoice == "3":
            date1 = row[3]
            print("Current Deadline Date: " + date1.strftime('%B %d, %Y'))
           
            deadlineEdit = dayChecker()
    
            try:
                cur.execute("UPDATE task SET deadline_date = ? WHERE task_id = (SELECT task_id FROM task ORDER BY task_id LIMIT ?, ?)", (deadlineEdit, int(toEdit)-1, 1))
            except mariadb.Error as e:
                print(f"MariaDB Error : {e}")
                    
        elif editChoice == "4":
            break
        else:
            print("Invalid Choice!")

    prompt()
    
    
def deleteTask():
    clearScreen()
    print("Deleting Task\n")
    isEmpty = checkIfExists("random", True, False)
    if isEmpty == "empty":
        print("No records yet!")
        prompt()
        return
    showTitles = viewTaskTitle()
    toDelete = input("Enter task number to delete: ")

    if toDelete < "1" or toDelete > str(showTitles):
        print("\nInvalid Choice!")
        prompt()
        clearScreen()
        return

    # Checks if Select Statement returns Multiple Entries
    try:
        cur.execute("DELETE FROM task WHERE task_id = (SELECT task_id FROM task ORDER BY task_id LIMIT ?, ?)", (int(toDelete)-1, 1))
    except mariadb.Error as e:
        print(f"MariaDB Error : {e}")

    print("Task successfully deleted.\n")
    prompt()
        
def viewTask():
    clearScreen()
    print("Viewing Tasks\n")
    
    isEmpty = checkIfExists("random", True, False)
    if isEmpty == "empty":
        print("No records yet!")
        prompt()
        return

    cur.execute("SELECT task_id, title, description, date_created, deadline_date, status, t.category_id, category_name FROM task t LEFT JOIN category c ON t.category_id = c.category_id")
    
    # Lists the tasks
    j = 1
    for i in cur:
        print("Title: " + str(i[1])) 
        print("Description: " + str(i[2]))
        date1 = i[3]
        print("Date created: " + date1.strftime('%B %d, %Y'))
        date2 = i[4]
        print("Deadline date: " + date2.strftime('%B %d, %Y'))
        if i[5] == 0: 
            print("Status: In progress")
        else:
            print("Status: Done")
        print("Category: " + str(i[7]))
        print("\n")
        
        j += 1
    prompt()
        
def markDone():
    clearScreen()
    print("Marking task as done\n")
    isEmpty = checkIfExists("random", True, False)
    if isEmpty == "empty":
        print("No records yet!")
        prompt()
        return
    cur.execute("SELECT title FROM task WHERE status = ?", (0,))
    j = 1
    print("========List of Tasks========")
    for i in cur:
        print("["+ str(j) +"] " + str(i[0]))
        j += 1
    print("\n")

    if j == 1:
        print("All tasks has already been done!")
        prompt()
        clearScreen()
        return

    toMark = input("Enter task number to mark as done: ")
    
    # Checks if task to be marked done exists
    if toMark < "1" or toMark > str(j-1):
        print("\nInvalid Choice!")
        prompt()
        clearScreen()
        return

    try:
        cur.execute("UPDATE task SET status = ? WHERE task_id = (SELECT task_id FROM task WHERE status = ? ORDER BY task_id LIMIT ?, ?)", (1, 0, int(toMark)-1, 1))
    except mariadb.Error as e:
        print(f"MariaDB Error : {e}")

    print("Task succesfully updated.\n")
    prompt()

def addCategory():
    clearScreen()
    print("Adding Category\n")
    categoryName = input("Enter category name: ")
    
    # Checks if category name already exists
    if checkIfExists(categoryName, False, True):
        print("Category already exists!")
        prompt()
        return
    
    try:
        cur.execute("INSERT INTO category (category_name) VALUES(?)", (categoryName,))
    except mariadb.Error as e:
        print(f"MariaDB Error : {e}")
 
    print("Category successfully created!\n")
    prompt()
    
def editCategory():
    clearScreen()
    showCategories = viewCategory()
    print("Editing Category\n")
    isEmpty = checkIfExists("random", False, False)
    if isEmpty == "empty":
        print("No categories to edit.\n")
        prompt()
        return
    categoryToEdit = input("Enter category number to edit: ")

    if categoryToEdit < "1" or categoryToEdit > str(showCategories):
        print("\nInvalid Choice!")
        prompt()
        clearScreen()
        return

    newCategName = input("Enter new category name: ")

    # Checks if new category name exists
    if checkIfExists(newCategName, False, False):
        print("Category name already exist!")
        prompt()
        return

    try:
        cur.execute("UPDATE category SET category_name = ? WHERE category_id = (SELECT category_id FROM category ORDER BY category_id LIMIT ?, ?)", (newCategName, int(categoryToEdit)-1, 1))
    except mariadb.Error as e:
        print(f"MariaDB Error : {e}")

    print("Category successfully edited!")    
    prompt()

def deleteCategory():
    clearScreen()
    showCategories = viewCategory()
    print("Deleting Category\n")
    isEmpty = checkIfExists("random", False, False)
    if isEmpty == "empty":
        print("Nothing to delete\n")
        prompt()
        return
    categoryToDelete = input("Enter category number to delete: ")

    if categoryToDelete < "1" or categoryToDelete > str(showCategories):
        print("\nInvalid Choice!")
        prompt()
        clearScreen()
        return
    
    # Sets the foreign key of tasks under the category to be deleted to NULL
    try:
        cur.execute("UPDATE task SET category_id = ? WHERE category_id = (SELECT category_id FROM category ORDER BY category_id LIMIT ?, ?)", (None, int(categoryToDelete)-1, 1))
    except mariadb.Error as e:
        print(f"MariaDB Error: {e}")
    
    # Deletes the category
    try:
        cur.execute("DELETE FROM category WHERE category_id = (SELECT category_id FROM category ORDER BY category_id LIMIT ?, ?)", (int(categoryToDelete)-1, 1))
    except mariadb.Error as e:
        print(f"MariaDB Error: {e}")

    print("Category successfully deleted.")
    prompt()
    
def viewCategory():
    clearScreen()
    print("View Category\n")

    isEmpty = checkIfExists("random", False, False)
    if isEmpty == "empty":
        print("No records yet!")
        return
    
    categoryName = "SELECT * FROM category"
    cur.execute(categoryName)

    # Lists the categories
    j = 1
    print("========List of Categories========")
    for i in cur:
        print("["+ str(j) +"] " + str(i[1]))
        j += 1
    print("\n")

    return j-1


def addTaskToCategory():
    clearScreen()
    print("Add Task To Category\n")

    isEmpty = checkIfExists("random", True, False)
    if isEmpty == "empty":
        print("No records yet!")
        prompt()
        return
    
    # Lists the tasks
    cur.execute("SELECT title FROM task WHERE category_id IS NULL")
    j = 1
    print("========List of Tasks========")
    for i in cur:
        print("["+ str(j) +"] " + str(i[0]))
        j += 1
    print("\n")
    
    if j==1:
        print("All tasks already have category!")
        prompt()
        return

    taskToAdd = input("Enter task number to add: ")

    if taskToAdd < "1" or taskToAdd > str(j-1):
        print("\nInvalid Choice!")
        prompt()
        clearScreen()
        return

    showCategories = viewCategory()

    isEmpty = checkIfExists("random", False, False)
    if isEmpty == "empty":
        print("\nThere are no categories yet!")
        prompt()
        return

    categoryToAdd = input("Enter category number: ")

    if categoryToAdd < "1" or categoryToAdd > str(showCategories):
        print("\nInvalid Choice!")
        prompt()
        clearScreen()
        return

    # Sets the task's foreign key to specified category ID
    try:
        cur.execute("UPDATE task SET category_id = (SELECT category_id FROM category ORDER BY category_id LIMIT ?, ?) WHERE task_id = (SELECT task_id FROM task WHERE category_id IS NULL ORDER BY task_id LIMIT ?, ?)", (int(categoryToAdd)-1, 1, int(taskToAdd)-1, 1))
    except mariadb.Error as e:
        print(f"MariaDB Error : {e}")
        
    print("Successfully added task to a category!")
    prompt()

def viewTaskTitle():        # For other function use
    cur.execute("SELECT task_id, title, description, date_created, deadline_date, status, t.category_id, category_name FROM task t LEFT JOIN category c ON t.category_id = c.category_id")
    j = 1
    print("========List of Tasks========")
    for i in cur:
        print("["+ str(j) +"] " + str(i[1]))
        j += 1
    print("\n") 
    return j-1

def title():
	title = open("title.txt", "r")
	for line in title:
		print("\033[1;33;40m" + line + "\033[0;37;40m", end="")

def menu():
    title()
    print("\n")
    print("\033[1;32;40m=========Menu=========\033[0;37;40m \n")
    delayPrint("[1]  Add/Create Task\n")
    delayPrint("[2]  Edit Task\n")
    delayPrint("[3]  Delete Task\n")
    delayPrint("[4]  View all Tasks\n")
    delayPrint("[5]  Mark Task as Done\n")
    delayPrint("[6]  Add Category\n")
    delayPrint("[7]  Edit Category\n")
    delayPrint("[8]  Delete Category\n")
    delayPrint("[9]  View Category\n")
    delayPrint("[10] Add task to a category\n")
    delayPrint("[0]  Exit\n")
    print("\033[1;32;40m======================\033[0;37;40m \n")
    

#MAIN
clearScreen()
while True:
    rootPass = input("Enter the password of your MariaDB root user: ")
    print("\n")
    try:
        conn = mariadb.connect(
            user="root",
            password= rootPass,
            host="localhost",
            port=3306,
            database="app",
            autocommit=True

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}") 
        print("Password is incorrect!")
        continue

    cur = conn.cursor()
    clearScreen()
    break


while True:     # Main Menu
    menu()
    choice = input("Enter choice: ")
    print("\n")
    if choice == "1":
        # Add/Create Task
        addTask()
    elif choice == "2":
        # Edit Task
        editTask()
    elif choice == "3":
        # Delete Task  
        deleteTask()
    elif choice == "4":
        # View All Task
        viewTask()
    elif choice == "5":
        # Mark Task as Done
        markDone()
    elif choice == "6":
        # Add Category
        addCategory()
    elif choice == "7":
        # Edit Category
        editCategory()
    elif choice == "8":
        # Delete Category
        deleteCategory()
    elif choice == "9":
        # View Category  
        viewCategory()
        prompt()
    elif choice == "10":
        # Add task to a category
        addTaskToCategory()
    elif choice == "0":
        # Exit
        conn.close()
        print("Thank you!\n")
        sys.exit(1)
    else:
        # If user enters an incorrect choice
        print("Invalid Choice!\n")
        

    clearScreen()