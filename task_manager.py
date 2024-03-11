# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========

'''os = operating system
- Contains functions that perform tasks like navigating the file system, 
interacting with environments
'''
import os 
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""] #List comprehension to filter out empty lines
      # from task data list. 
    # 'for t in task_data' = iterated through each element 't' in task_data list
    # 'if t != ""' = Checks if the element 't' is not an empty string

#====Task list and dictionary====

'''Creating an empty list for the tasks that will be appeneded and removed from tasks.txt
 for loop iterates through task.txt
 These tasks = dictionaries '''
task_list = []
for task_str in task_data: 
    curr_task = {} # Dictionary to store the attributes of a single task

    # Split by semicolon and manually add each information about the task
    # Keys = [''], Values = user input 
    task_components = task_str.split(";")
    curr_task['username'] = task_components[0]
    curr_task['title'] = task_components[1]
    curr_task['description'] = task_components[2]
    # datetime class
    # 'strptime' is a method = string parse time
    # takes the due date string converts it into a datetime object in the YYYY-MM-DD format
    curr_task['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_task['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_task['completed'] = True if task_components[5].lower() == "yes" else False

# Current task dictionary added to task list  where 
    task_list.append(curr_task)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file exists, write one with a default account
if not os.path.exists("user.txt"): 
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n") #splitting lines in user.txt

# Convert to a dictionary
    ''' This allows for easy retrieval of username and password.
    (Beneficial for efficent authentication.) '''
username_password = {} 
for user_line in user_data:
    # Split the user string by semicolon
    user_parts = user_line.split(';')

    # Check if there is any content in the user line
    if user_parts and len(user_parts) >= 2:
        username, password = user_parts[0], ';'.join(user_parts[1:])
        username_password[username] = password
    else:
        # Handle the case where there is no valid username and password
        print(f"Issue with the user data: {user_line}. Skipping.")

# for user in user_data:
#     username, password = user.split(';')
#     username_password[username] = password # Retrieving the username key with corresponding password value

''' Assuming no user has logged in, creating a prompt'''

logged_in = False
while not logged_in: 

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("\nWrong password. Please try again.")
        continue
    else:
        print("\nLogin Successful!")
        logged_in = True

def reg_user():
        '''Function requirements: 
        Function called when user selects 'r' from menu
        Doesn't duplicate usernames when you add a new user to user.txt (provide relevant error message)
        '''
        
        # - Request input of a new username
        new_username = input("New Username: ")

        # Check if username already exists
        if new_username in username_password:
         print("Username already exists. Please choose a different username.")
         return  # Exit the function if the username already exists
        
        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("\nNew user added")
            username_password[new_username] = new_password
            
            # Open the file outside the loop
            with open("user.txt", "a+") as out_file: 
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
               
               # Wrtie all users to the file
                out_file.write("\n".join(user_data))       
        else:
            print("Passwords do not match") 
        
def add_task():
    '''Allow a user to add a new task to task.txt file
    Prompt a user for the following:
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task, and
    - the due date of the task.
    '''

    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return  # Exit the function if the username is not found

    # Otherwise get task info
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")

    # Testing the user's date format for error
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    
    # Add the data to the task_list
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    # Reload task data from tasks.txt
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    # Clear existing task_list
    task_list.clear()

    # Prompt user for completion status
    completion_status = input("Is the task completed? (yes/no): ").lower()

    if completion_status == "yes":
        new_task["completed"] = True
    else:
        new_task["completed"] = False

    # Update task_list with reloaded data
    for task_str in task_data:
        curr_task = {}  # Dictionary to store the attributes of a single task

        # Split by semicolon and manually add each information about the task
        task_components = task_str.split(";")
        curr_task['username'] = task_components[0]
        curr_task['title'] = task_components[1]
        curr_task['description'] = task_components[2]
        curr_task['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_task['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_task['completed'] = True if task_components[5].lower() == "yes" else False

        # Current task dictionary added to task list
        task_list.append(curr_task)

    # Add the new task
    task_list.append(new_task)

    # Write the updated task_list to tasks.txt
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

    print("\nTask added successfully!")

def view_all():
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''
        for t in task_list:
            print("-----------------------------")
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)
            
def view_mine():
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
        for t in task_list:
            if t['username'] == curr_user:
                print("-----------------------------")
                disp_str = f"Task: \t\t {t['title']}\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                print(disp_str)
def edit_task():
    '''Allow admin to edit due date of a task and reassign it to another user.'''
    # Ensure only admin can access this function
    if curr_user != 'admin':
        print("You don't have permission to perform this action.")
        return

    # Prompt for admin login
    admin_login = input("Enter admin username: ")
    admin_password = input("Enter admin password: ")

    if admin_login != 'admin' or admin_password != username_password['admin']:
        print("Invalid admin credentials. Exiting.")
        return

    # Prompt for task details
    task_title_to_edit = input("Enter the title of the task to edit: ")

    # Find the task with the given title
    task_to_edit = None
    for task in task_list:
        if task['title'] == task_title_to_edit:
            task_to_edit = task
            break

    if task_to_edit is None:
        print(f"Task with title '{task_title_to_edit}' not found.")
        return

    # Prompt for new due date
    while True:
        try:
            new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
            task_to_edit['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified.")

    # Prompt for new assigned user
    new_assigned_user = input("Enter the username of the new assigned user: ")

    if new_assigned_user not in username_password.keys():
        print("User does not exist. Please enter a valid username.")
        return

    # Update task details
    task_to_edit['username'] = new_assigned_user

    # Write the updated task_list to tasks.txt
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

    print("Task edited successfully!")

def gen_reports():
    ''' Generates a summary of task completion status and writes it to
    two text files (task_overview.txt and user_overview.txt).'''

    # Information for task_overview.txt and user_overview
    # Set variables to 0
    total_users = len(username_password.keys())
    total_tasks = len(task_list)
    completed_tasks = 0
    overdue_tasks = 0
    incomplete_tasks = 0

    # Creating a dictionary to store tasks for each user
    user_tasks = {}

    # ==== task_overview.txt ====
    # For each task, update variables accordingly
    for task in task_list:
        if task["completed"]:
            completed_tasks += 1
        elif datetime.today() > task["due_date"]:
            overdue_tasks += 1
        incomplete_tasks += 1

        # Update user_tasks dictionary
        if task["username"] not in user_tasks:
            user_tasks[task["username"]] = []

        user_tasks[task["username"]].append(task)

    # Calculate percentage for incomplete and overdue tasks
    try:
        incomplete_percent = (incomplete_tasks / total_tasks) * 100
        overdue_percent = (overdue_tasks / total_tasks) * 100
    except ZeroDivisionError:
        incomplete_percent = overdue_percent = 0

    # Write information to task_overview.txt file
    date_time = datetime.today().strftime(DATETIME_STRING_FORMAT + "%H:%M")

    with open("task_overview.txt", "w", encoding="utf-8") as task_report:
        task_report.write("TASK OVERVIEW\n\n" + date_time + "\n\n")
        task_report.write("-" * 80 + "\n")
        task_report.write("All tasks: \n")
        task_report.write("-" * 80 + "\n")
        task_report.write(f"Total number of tasks = {total_tasks}\n")
        task_report.write(f"Total number of completed tasks = {completed_tasks}\n")
        task_report.write(f"Total number of incomplete tasks = {incomplete_tasks} | {incomplete_percent}%\n")
        task_report.write(f"Total number of overdue tasks = {overdue_tasks} | {overdue_percent}\n")
        task_report.write("-" * 80 + "\n")
        task_report.write("User assigned tasks and details: \n")
        task_report.write("-" * 80 + "\n")

        # Iterate over each task for its information
        for task in task_list:
            task_report.write(f"Title: {task['title']}\n")
            task_report.write(f"Assigned to: {task['username']}\n")
            task_report.write(f"Status: {'Completed' if task['completed'] else 'Incomplete'}\n")
            task_report.write(f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n")
            task_report.write(f"Description: {task['description']}\n")
            task_report.write("-" * 80 + "\n")

    # ==== user_overview.txt ===
    # Write information to user_overview.txt file
    with open("user_overview.txt", "w", encoding="utf-8") as user_report:
        user_report.write("USER OVERVIEW\n" + date_time + "\n")
        user_report.write(f"Total number of users = {total_users}\n")
        user_report.write("-" * 30 + "\n")

        # Iterate through users and display total tasks and completion status
        for user, tasks in user_tasks.items():
          user_report.write(f"User: {user}\n")

          total_user_tasks = len(tasks)
          completed_user_tasks = sum(task["completed"] for task in tasks)
          overdue_user_tasks = sum(1 for task in tasks if not task["completed"] and datetime.today() > task["due_date"])
          incomplete_user_tasks = total_user_tasks - completed_user_tasks

    # Calculate percentage for incomplete and overdue tasks
          try:
            incomplete_percent_user = (incomplete_user_tasks / total_user_tasks) * 100
            overdue_percent_user = (overdue_user_tasks / total_user_tasks) * 100
          except ZeroDivisionError:
            incomplete_percent_user = overdue_percent_user = 0

          user_report.write(f"Total number of completed tasks = {completed_user_tasks}\n")
          user_report.write(f"Total number of incomplete tasks = {incomplete_user_tasks} | {incomplete_percent_user}%\n")
          user_report.write(f"Total number of overdue tasks = {overdue_user_tasks} | {overdue_percent_user}\n")
          user_report.write("-" * 30 + "\n")     

    print("\nReports generated successfully.")


def display_stats():
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    
    # Display task details
        for user in username_password.keys():
            user_completed_tasks = user_incomplete_tasks = user_overdue_tasks = 0

            for task in task_list:
                if task["username"] == user:
                    if task["completed"]:
                       user_completed_tasks += 1
                    elif datetime.today() > task["due_date"]:
                       user_overdue_tasks += 1
                    else:
                       user_incomplete_tasks += 1

        print(f"\nUser: {user}")
        print(f"Total number of completed tasks = {user_completed_tasks}")
        print(f"Total number of incomplete tasks = {user_incomplete_tasks}")
        print(f"Total number of overdue tasks = {user_overdue_tasks}")
        print("-" * 30)

def main_menu():
 while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
 r - Registering a user
 a - Adding a task
 va - View all tasks
 vm - View my task
 et - Edit a task (admin only)            
 gr - Generate report (admin only)
 ds - Display statistics (admin only)
 e - Exit
 : ''').lower()  

    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'et' and curr_user == 'admin':
        edit_task()
    elif menu == 'gr' and curr_user == 'admin':
        gen_reports()
    elif menu == 'ds' and curr_user == 'admin': 
        display_stats()
    elif menu == 'e':
         print('Goodbye!!!')
         break
    else:
        print("You have made a wrong choice, Please try again")  

# Calling the main menu function     
main_menu()