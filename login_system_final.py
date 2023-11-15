import os
from getpass_asterisk.getpass_asterisk import getpass_asterisk
from datetime import datetime
import time
import sqlite3
from random import randint

# Sqlite code starts here -----

# create database name accounts.db
def open_db():
    global conn,c
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()

# close the database
def close_db():
    c.close()
    conn.close()

# Create a new table if not existing in the database
def create_table():
    open_db()
    c.execute('''CREATE TABLE IF NOT EXISTS accounts(
        username TEXT,
        password TEXT,
        security_question TEXT,
        answer TEXT
                )''')
    conn.commit()
    close_db()

# Register function
def register(username,password,sec_ques,ans):
    open_db()
    c.execute('''
                INSERT INTO accounts VALUES (?,?,?,?)
              ''',(username,password,sec_ques,ans))
    conn.commit()
    close_db()

# function update password
def change_password(username,password,new_pass):
    open_db()
    c.execute('''
                UPDATE accounts
                SET password = (?)
                WHERE username = (?) AND password = (?)
              
                ''',(new_pass,username,password))
    conn.commit()
    close_db()

# function to validate the security question
def validate_sec_question(username,sec_question,sec_answer):
    open_db()

    c.execute('''
                SELECT * FROM accounts
                WHERE username = (?) AND security_question = (?) AND answer = (?)
            ''',(username,sec_question,sec_answer))
    
    data = c.fetchone()
    
    if data:
        return True
    else:
        return False

# function to update password using security question and security answer
def forget_password(sec_ques,ans,new_pass):
    open_db()
    c.execute('''
                UPDATE accounts
                SET password = (?)
                WHERE security_question = (?) AND answer = (?)
              
                ''',(new_pass,sec_ques,ans))
    conn.commit()
    close_db()

# Login function
def login(username,password):
    open_db()
    c.execute('''
            SELECT * FROM accounts
            WHERE username = (?) AND password = (?)
            ''',(username,password))
    data = c.fetchone()
    if data:
        close_db()
        return True
    else:
        close_db()
        return False

# Function to check if the user is already used in the database 
def check_username(username):
    open_db()
    c.execute('''
            SELECT * FROM accounts
            WHERE username = (?) 
            ''',(username,))
    data = c.fetchone()
    close_db()
    if data: 
        return True
    else:
        return False

# function to view all data   
def view():
    open_db()
    c.execute('''
                SELECT * FROM accounts
            ''')
    data = c.fetchall()
    close_db()
    for d in data:
        print(d)

# function to write database data to account.txt
def write_account():
    open_db()
    c.execute('SELECT * FROM accounts')
    data = c.fetchall()
    close_db()
    
    
    with open('accounts.txt','w') as f:
        for n in data:
            f.write(f'{str(n)} \n')

        


# Sql code ends here ----



# MAIN PROGRAM CODE STARTS HERE

# Clear screen
def clear_screen():
  if os.name == 'nt': # check if windows
    os.system('cls')
  else:
    os.system('clear') # mac or linux

# function that do the last part of registration process
def reg_lastpart(username,password):
    sec_ques = input('Security question: ')
    ans = input('Answer: ')

    register(username,password,sec_ques,ans)
    print()
    print('Saving...')
    time.sleep(3)
    print()
    print('Registered Successfully')
    write_account()
    time.sleep(3)
    main()

# Show password option
def password_options(username):
    print('Password Option')
    print('Random Password    : 1')
    print('Enter Manually     : 2')
    print('Menu:              : 3')
    print()
    pass_choice = input('>>> ')
    if pass_choice == '1':
        password = random_password()
        print('Password generated successfully!')
        reg_lastpart(username,password)
    elif pass_choice == '2':   
        while True:
            print('Password length is 6-12 characters')
            password = getpass_asterisk('Password: ')

            if len(password) >= 6 and len(password) <= 12:
                confirm_password = getpass_asterisk('Confirm Passsword: ')

                if password != confirm_password:
                    print("Password didn't match")
                    print('Try again: [Y/N]')
                    choice = input('>>> ').upper()
                    
                    if choice == 'N':
                        main()
                    elif choice == 'Y':    
                        register_account()
                
                    else:
                        print('Password Match')
                else:
                    reg_lastpart(username,password)
                    
    elif pass_choice == '3':
        main()
    
    else:
        main()

# function that gives user the option to choose the their password be like
# this function is for change function option
def change_password_option(username,password):
    print('Password Option')
    print('Random Password    : 1')
    print('Enter Manually     : 2')
    print('Menu:              : 3')
    print()
    pass_choice = input('>>> ')
    if pass_choice == '1':
        gen_password = random_password()
        change_password(username,password,gen_password)
        write_account()
        print()
        print('Password generated successfully!')
        time.sleep(2)
        main()

    elif pass_choice == '2':   
        while True:
            print('Password length is 6-12 characters')
            new_password = getpass_asterisk('Enter new password: ')

            if len(new_password) >= 6 and len(new_password) <= 12:
                confirm_password = getpass_asterisk('Confirm new passsword: ')

                if new_password != confirm_password:

                    print("Password didn't match")
                    print('Try again: [Y/N]')
                    choice = input('>>> ').upper()
                    
                    if choice == 'N':
                        main()
                    elif choice == 'Y':    
                        change_password_option(username,password)
                
                elif new_password == confirm_password:
                    # print('Password Match')
                    # print()

                    # Sql querry to update password
                    change_password(username,password,confirm_password)
                    print()
                    print('Password changed successfully!')
                    input('Menu: Press enter key ...')
                    write_account()
                    main()
                
    elif pass_choice == '3':
        main()
    
    else:
        main()

# function that gives user the option to choose the their password be like
# this function is for reset function option
def forgot_password_option(username,sec_question,sec_answer):
    print('Password Option')
    print('Random Password    : 1')
    print('Enter Manually     : 2')
    print('Menu:              : 3')
    print()
    pass_choice = input('>>> ')
    if pass_choice == '1':
        gen_password = random_password()
        forget_password(sec_question,sec_answer,gen_password)
        write_account()
        print()
        print('Password generated successfully!')
        time.sleep(2)
        main()
    elif pass_choice == '2':   
        while True:
            print('Password length is 6-12 characters')
            new_password = getpass_asterisk('Enter new password: ')

            if len(new_password) >= 6 and len(new_password) <= 12:
                confirm_password = getpass_asterisk('Confirm new passsword: ')

                if new_password != confirm_password:
                    print("Password didn't match")
                    print('Try again: [Y/N]')
                    choice = input('>>> ').upper()
                    
                    if choice == 'N':
                        main()
                    elif choice == 'Y':    
                        forgot_password_option(username,sec_question,sec_answer)
                
                elif new_password == confirm_password:
                    
                    forget_password(sec_question,sec_answer,new_password)
                    write_account()
                    print()
                    print('Password changed successfully!')
                    
                    print()
                    input('Menu: Press enter key ...')
                    main()
                
    elif pass_choice == '3':
        main()
    
    else:
        main()






# Register account function
def register_account():
    while True:
        title('Register Account')
        
        
        username = input('Username: ')
        
        if check_username(username): 
            title('Register Account')
            input('Username not available')
            main()

        elif username == '' or len(username) <= 5:
                title('Register Account')
                print('Invalid username')
        
                time.sleep(2)
                main()

        else:         
            title('Register Account')
            
            password_options(username)
            
# function that displays the date 
def timedate():
    date = datetime.now()
    formatted_date = date.strftime("%B %d, %Y")
    return formatted_date

# Main title of the program
def title(subtitle):
    date_now = timedate()
    clear_screen()
    print(f'Gelos Enterprises - {date_now}')
    print()
    print(f'{subtitle}\n--------------------')
    print()


# Main Menu
def login_menu():
    title('Menu')
    print('Login            : 1')
    print('Register         : 2')
    print('Change Password  : 3')
    print('Reset Password   : 4')
    print('View Accounts    : 5')
    print('Exit             : 6')

# function that return to menu
def back_to_menu(option):
    print()
    print(f'Invalid {option}\n')
    print()
    input('Menu - press any key >> ')


# Generate password function
def random_password():
    gen_password = ''
    for x in range(12):
        gen_password += chr(randint(33,126))
    
    return gen_password



    
# Main program - function
def main():
    
    while True:
        clear_screen()
        login_menu()
        print()
        user_choice = input('>>> ')
        if user_choice == '1':
            chance = 3
            while chance != 0:
                clear_screen()
                title('Login')
                
                username = input('Username: ') # ask user to enter username
                if check_username(username): # check username if its in the database
                    password = getpass_asterisk('Password: ')
                    
                    if login(username,password):
                        title('Login')
                        print(f'Welcome {username}')
                        time.sleep(3)
                        main()
                    else:
                        title('Login')
                        print()
                        chance = chance - 1
                        input('Incorrect password\n')
                        print()
                        input(f'attemps remaining: {chance} \n')
                        if chance == 0:
                            
                            input('Contact administrator \n')
                            
                        else:
                            continue
                   
                else:
                    input('No username found in the system\n')
                    chance = chance - 1
                    print()
                    input(f'attemps remaining: {chance} \n')
                    if chance == 0:
                        input('Contact administrator \n')       
                    else:
                        continue
                          
                
        elif user_choice == '2':
            while True:
                register_account()
                print('Menu: M')
                m = input('>>> ').upper()
                if m == 'M':
                    main()
            
        elif user_choice == '3':
            while True:
                title('Change Password')
                username = input('Username: ')

                # check if username is in the system using check_username function
                if check_username(username): 
                    title('Change Password')
                    print(f'Username: {username}')
                    old_password = getpass_asterisk('Enter old password: ')

                    # Validate username and password using login function
                    if login(username,old_password):
                        while True:
                            title('Change Password')
                            print(f'Username: {username}') # just to keep the display the same as above
                            asterisk_ = len(old_password)
                            print('Enter old password:','*'*asterisk_)# Just to keep display the same as above
                            print()
                            change_password_option(username,old_password)


                    else: 
                        back_to_menu('Password')
                        break

                else:
                    back_to_menu('username')
                    break
            
        elif user_choice == '4':
            #forgot password
            title('Forgot Password')
            
            username = input('Username: ')
            if check_username(username): 
                title('Forgot Password')
                print(f'Username: {username}')

                sec_question = input('Security question: ')
                sec_answer = input('Security answer: ')

                data = validate_sec_question(username,sec_question,sec_answer)

                if data:
                    print()
                    forgot_password_option(username,sec_question,sec_answer)

                else: 
                    title('Forgot Password')
                    print('No data found!')

                    input('Menu: Press enter key ...')
                    main()

            else:
                print('No username found')
                input('Menu: Press enter key...')        
                main()

        elif user_choice == '5':
            # try and exept is used to check if username and password are not empty
            try:
                title('View Accounts')
                print('Login administrator account')
                
                username = input('Username: ')
                password = getpass_asterisk('Password: ')

                
                if username == 'admin' and password == 'admin':
                    title('View Accounts')
                    print('User accounts')
                    print('-'*13)
                    view()
                    print()
                    input('Menu : Press enter key ')
                    main()

                else:
                    title('View Accounts')
                    print('Unauthorized account')
                    print()
                    time.sleep(2)
                    main()

            # if the username and password are empty will show Invalid username and password input        
            except ValueError :
                    title('View Accounts')
                    print('Invalid username or password')
                    
                    time.sleep(2)
                    main()
            except EOFError:
                    title('View Accounts')
                    print('Invalid Entry')
                    time.sleep(2)
                    main()
            
        elif user_choice == '6':
            title('Exiting...')
            
            end_time = time.time()
            
            elapsed_time(start_time,end_time)
            time.sleep(3)
            clear_screen()
            exit()


        else:
            continue

def elapsed_time(start_time,end_time):
    # Record the end time
            

            # Calculate minutes and seconds
            elapsed_time_seconds = end_time - start_time
            minutes, seconds = divmod(elapsed_time_seconds, 60)
            print(f'Duration is {int(minutes)} min : {int(seconds)} seconds')

            time.sleep(2)
            
# start the timer            
start_time = time.time()
main()