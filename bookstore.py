"""
Please make sure to look at the below files as well if copy code out to also 
copy below out to run code:
    1. ebookstore_db.db 
    2. user.txt (Login details, and user role)
    
"""
#-------------------------------------------------------------------------
"""
==List of Abbreviations==  (for easy reference that are used in code)
* sp            : Selling Price
* pp            : Purchase Price
* po_qty        : Purchase Order Qty
* user_n        : User Name        
* user_p        : User Password
* user_r        : User Role
* user_pass     : User password
* user_pass_c   : User Password Confirmation
* b_id          : Bookstore ID
* wo_qty        : Write off stock Qty 
* ts_sp         : Total selling qty Selling price
* ts_pp         : Total selling qty Purchase Price
* ts_margin     : Total selling qty Margin 
* ts_margin_per : Total selling qty Margin %

"""
#----------------------------------------------------------------------------
#=====importing libraries===========
from datetime import date
import sqlite3

#----------------------------------------------------------------------------
# ==== List of variables and dictionaries ====
user_name = ""
user_pass = ""
user_role = ""
user_pass_c = ""
user_role_dec = {'admin': 'Administrator',
                 'manag': 'Manager',
                 'clerk': 'Clerk',
                }

#-----------------------------------------------------------------------------
# ==== Database section and Create Table's  ====

# Create a new or open database called ebookstore_db
ebook = sqlite3.connect('ebookstore_db.db')
# Create a cursor object
cursor = ebook.cursor()

# Check if the table exists if not create a table called book
cursor.execute('''
    CREATE TABLE IF NOT EXISTS book(
            b_id            INTEGER NOT NULL    UNIQUE,
            title           CHAR    NOT NULL,
            author          CHAR    NOT NULL,
            isbn            VARCHAR NOT NULL    UNIQUE,
            qty             INTEGER,
            po_qty          INTEGER NOT NULL ON CONFLICT REPLACE DEFAULT 0,
            sp              REAL,
            pp              REAL,
            s_qty           INTEGER NOT NULL ON CONFLICT REPLACE DEFAULT 0,
            p_qty           INTEGER NOT NULL ON CONFLICT REPLACE DEFAULT 0,
            wo_qty          INTEGER NOT NULL ON CONFLICT REPLACE DEFAULT 0,
            ts_sp           REAL NOT NULL ON CONFLICT REPLACE DEFAULT 0,
            ts_pp           REAL NOT NULL ON CONFLICT REPLACE DEFAULT 0,
            ts_margin       REAL NOT NULL ON CONFLICT REPLACE DEFAULT 0,
            ts_margin_per   REAL NOT NULL ON CONFLICT REPLACE DEFAULT 0,
            PRIMARY KEY(b_id))
''')

# Commit the change
ebook.commit()
ebook.close()

#----------------------------------------------------------------------------
# ===== List Of User Defined Functions =======


# Setup a main menu for user with an admin or manag role type
"""
If the login user role type is admin or manager, they can access Finance & 
Administration.
"""
def mainmenu_admin():
    print("1. Enter Book")
    print("2. Update Book")
    print("3. Deleted Book")
    print("4. Search Book")
    print("5. Sales & Purchase")
    print("6. Finance")
    print("7. Administration")
    print("0. Exit")

    global mainmenu_s
    mainmenu_s = ""


# Setup a main menu for user with clerk role    
"""
If the login user role is clerk, the menu must not display Statistics & 
Administration.
"""
def mainmenu_clerk():
    print("1. Enter Book")
    print("2. Update Book")
    print("3. Deleted Book")
    print("4. Search Book")
    print("5. Sales & Purchase")
    print("0. Exit")

    global mainmenu_s
    mainmenu_s = ""

# -------------------------------------------------------------------------

# ======= Login Section =======
print("\n\n\t\tWelcome to Camel Knee Bookstore")
print("\n\n")
print("Please Login:")

user_details = open("user.txt", "r")

# Create a dictionary to check if the user does exist
user_n = []        
user_p = []
user_r = []       
for idata in user_details:
    auser_n,buser_p,cuser_r = idata.split(", ") 
    buser_r = buser_p.strip()
    user_n.append(auser_n)
    user_p.append(buser_p)

user_data = dict(zip(user_n, user_p))

login_user_name = input("\tUsername: ").upper()


# Create a while loop to check the username is valid
while login_user_name not in user_n:
    print("\nThe username enter is invalid.")
    print("Please re-enter your username.")
    login_user_name = input('''\tUsername: ''').upper()
    if login_user_name in user_n:
        continue

user_pass = input("\tPassword: ")
 
# Create a while loop to verify the password
while user_pass != user_data[login_user_name]:
    print("\nThe password you enter is incorrected.")
    user_pass = input("\nPlease re-enter your password: \n\tPassword: ")
    if user_pass == user_data[login_user_name]:
        continue

today1 = date.today()
formatted_date = today1.strftime('%d %B %Y')

print(f"\n\n\n\t\tWelcome, {login_user_name}")


#----------------------------------------------------------------------------
while True:
    print("\n\tCAMEL KNEE BOOKSTORE")
    print("\t\tTask Menu\n")
    """
    If the login user is admin, manager, role they can access Finance & 
    Administration.
    """
    # Create dictionary to check the user role
    user_role_c = open("user.txt", "r")
    user_n = []
    user_p = []  
    user_r = []      
    for idata in user_role_c:
        auser_n,buser_p,cuser_r = idata.split(", ") 
        cuser_r = cuser_r.strip()
        user_n.append(auser_n)
        user_p.append(buser_p)
        user_r.append(cuser_r)

    user_roledata = dict(zip(user_n, user_r))
    
    user_role = user_roledata[login_user_name]
            
    if user_role == "admin" or user_role == "manag":
        mainmenu_admin()
        mainmenu_s = int(input('''\n\nSelect one of the above options
(only enter the number):  '''))
            
    else:
        mainmenu_clerk()
        mainmenu_s = int(input('''\n\nSelect one of the above options
(only enter the number):  '''))


    if mainmenu_s == 1:           
           while True:
              
              """ Double check the user has all the details of the book I create
              a enter book menu to confirm the user have details and if not the 
              user can go back to the main menu."""

              print('''\n\nYou are about to enter a new book into the system. 
Please make sure you have all the details to enter the book.
\nDetails require: Bookstore ID, Title, Author, ISBN, Qty, Selling & Purchase Price. 
                    ''')  
              enter_menu = input('''\nDo you wish to continue to enter the book:
        Y - Yes, I have all details.
        N - No, Return to Task Menu
            :    ''').upper()
              
              if enter_menu == "Y":                    
                    """Ask how many new books is required to add. Then use a for loop 
                    that helps not to go back to main menu and start over to add more 
                    books if more than 1 book needs to be entered."""
                    num_new_book = int(input('''\nHow many books need to be added: '''))
                    num_new_book_p = num_new_book + 1
                    num_new_book_n = num_new_book - 1

                    for i in range (1, num_new_book_p):
                        if i <= num_new_book_p:
                            # Open database called ebookstore_db
                            ebook = sqlite3.connect('ebookstore_db.db')
                            # Create a cursor object
                            cursor = ebook.cursor()

                            # Check if the table exists if not create a table called book
                            cursor.execute('''
                                CREATE TABLE IF NOT EXISTS book(
                                        b_id            INTEGER NOT NULL    UNIQUE,
                                        title           CHAR    NOT NULL,
                                        author          CHAR    NOT NULL,
                                        isbn            VARCHAR NOT NULL    UNIQUE,
                                        qty             INTEGER,
                                        po_qty          INTEGER NOT NULL ON CONFLICT REPLACE DEFAULT 0,
                                        sp              REAL,
                                        pp              REAL,
                                        s_qty           INTEGER NOT NULL ON CONFLICT REPLACE DEFAULT 0,
                                        p_qty           INTEGER NOT NULL ON CONFLICT REPLACE DEFAULT 0,
                                        wo_qty          INTEGER NOT NULL ON CONFLICT REPLACE DEFAULT 0,
                                        ts_sp           REAL NOT NULL ON CONFLICT REPLACE DEFAULT 0,
                                        ts_pp           REAL NOT NULL ON CONFLICT REPLACE DEFAULT 0,
                                        ts_margin       REAL NOT NULL ON CONFLICT REPLACE DEFAULT 0,
                                        ts_margin_per   REAL NOT NULL ON CONFLICT REPLACE DEFAULT 0,
                                        PRIMARY KEY(b_id))      ''')

                            b_id1 = input("\nEnter the bookstore id for the book: \n")
                            title1 = input("Enter the Book Title: \n").upper()
                            author1 = input("Enter the Author: \n").upper()
                            isbn1 = input("Enter the ISBN Number(only numbers, no space): \n")
                            qty1 = int(input("Enter the qty of the book: \n"))
                            sp1 = float(input("Enter the Selling Price(Each): \n"))
                            pp1 = float(input("Enter the Purchase Price(Each): \n"))

                            cursor.execute('''INSERT INTO book(b_id,title,
                                            author, isbn, qty, sp, pp)
                                            VALUES(?,?, ?, ?, ?, ?, ?)''', 
                                            (b_id1, title1, author1, isbn1,
                                            qty1, sp1, pp1))

                            b_id = cursor.lastrowid
                            print('''\nThe book was entered, Bookstore ID: %d 
                                    ''' % b_id)

                            ebook.commit()
                            ebook.close()
                    break
                
              elif enter_menu == "N":
                  print("Returning to Task Menu")
                  break
              
              else:
                  print("Invalid Entry. Only enter Y or N.")
                  print("Please Try again")
                  enter_menu = input('''Do you wish to continue enter book:
        Y - Yes, I have all the details.
        N - No, Return to Task Menu
            :    ''').upper()
                  

    elif mainmenu_s == 2:
        print('''\n\nOnly the following can be updated: Title, Author, ISBN & Qty.
              If You require to updat the Bookstore ID, this must be done in 
              the Administration section. \n''')
        
        while True:
            # create a menu to update book details            
            update_menu = int(input('''Select one of the following options:
                1 - Update Title
                2 - Update Author
                3 - Update ISBN
                4 - Update Qty
                0 - Return to Task Menu
                    :  '''))
            
            if update_menu == 1:
                # Open database called ebookstore_db
                ebook = sqlite3.connect('ebookstore_db.db')
                # Create a cursor object
                cursor = ebook.cursor()

                b_id = input('''Enter the bookstore id \n: ''')
                title = input('''Enter or Updated the Title \n: ''' ).upper()
                
                
                cursor.execute('''UPDATE book SET title = ? 
                                WHERE b_id = ?''', (title, b_id))
                
                print(f'''The book with Bookstore ID: {b_id} Title name was 
                      updated to: {title}.  ''' )
                
                ebook.commit()
                ebook.close()
            
            
            elif update_menu == 2:
                # Open database called ebookstore_db
                ebook = sqlite3.connect('ebookstore_db.db')
                # Create a cursor object
                cursor = ebook.cursor()

                b_id = input('''Enter the bookstore id \n: ''')
                author = input('''Enter or Updated the Author \n: ''' ).upper()
                                
                cursor.execute('''UPDATE book SET author = ? 
                                WHERE b_id = ?''', (author, b_id))
                
                print(f'''The book with Bookstore ID: {b_id} Author name was 
                      updated to: {author}.  ''' )
                
                ebook.commit()
                ebook.close()
                        
            
            elif update_menu == 3:
                # Open database called ebookstore_db
                ebook = sqlite3.connect('ebookstore_db.db')
                # Create a cursor object
                cursor = ebook.cursor()

                b_id = input('''Enter the bookstore id \n: ''')
                isbn = input('''Enter or Updated the ISBN number
                             (Only number, no space) \n: ''' )
                                
                cursor.execute('''UPDATE book SET isbn = ? 
                                WHERE b_id = ?''', (isbn, b_id))
                
                print(f'''The book with Bookstore ID: {b_id} ISBN number was 
                      updated to: {isbn}.  ''' )
                
                ebook.commit()
                ebook.close()
            
            
            elif update_menu == 4:
                while True:
                    qty_update = int(input('''Select 1 of the below options why
                        Stock qty needs to be updated
                            1 - Stock Take
                            2 - Damage: In Store (Write off)
                            3 - Damage: Return from Customers
                            4 - Return to Supplier
                            0 - Return to Task Menu
                                :    '''))
                    
                    if qty_update == 1:
                        while True:
                            stock_take = input('''Did the stock:
                                IN - Increase
                                DE - Decrease 
                                    :   ''').upper
                            
                            if stock_take == "IN":
                                # Create a new or open database called ebookstore_db
                                ebook = sqlite3.connect('ebookstore_db.db')
                                # Create a cursor object
                                cursor = ebook.cursor()

                                b_id = input('''Enter the bookstore id: \n: ''')
                                qty = input('''Enter only difference to Increase stock: \n: ''' )
                                                
                                # creat update to increase stock qty                
                                cursor.execute('''UPDATE book SET qty = qty + ? 
                                                WHERE b_id = ?''', (qty, b_id))

                                print(f'''\n\nThe book with ID:{b_id} Stock  Qty increase: {qty}.  ''' )
                                ebook.commit()

                                # Create update for write off
                                cursor.execute('''UPDATE book SET wo_qty = wo_qty - ? 
                                            WHERE b_id = ?''', (qty, b_id))
                                print(f'''\nThe book id {b_id} w/o stock has decrease with {qty}''')

                                ebook.commit()
                                ebook.close()

                            elif stock_take == "DE":
                                # Create a new or open database called ebookstore_db
                                ebook = sqlite3.connect('ebookstore_db.db')
                                # Create a cursor object
                                cursor = ebook.cursor()

                                b_id = input('''Enter the bookstore id: \n: ''')
                                qty = input('''Enter only difference to decrease stock: \n: ''' )
                                                
                                # creat update to decrease stock qty                
                                cursor.execute('''UPDATE book SET qty = qty - ? 
                                                WHERE b_id = ?''', (qty, b_id))

                                print(f'''\n\nThe book with ID:{b_id} Stock  Qty increase: {qty}.  ''' )
                                ebook.commit()

                                # Create update for write off
                                cursor.execute('''UPDATE book SET wo_qty = wo_qty + ? 
                                            WHERE b_id = ?''', (qty, b_id))
                                print(f'''\nThe book id {b_id} w/o stock has decrease with {qty}''')

                                ebook.commit()
                                ebook.close()

                            else:
                                print('''\nYou have entered an invalid input''')
                                print('Only enter IN or DE')
                                stock_take = input('''Did the stock:
                                IN - Increase
                                DE - Decrease 
                                    :   ''').upper

                    elif qty_update == 2:
                        # Create a new or open database called ebookstore_db
                        ebook = sqlite3.connect('ebookstore_db.db')
                        # Create a cursor object
                        cursor = ebook.cursor()

                        b_id = input('''Enter the bookstore id: \n: ''')
                        qty = input('''Enter Qty to write off stock: \n: ''' )
                                        
                        # creat update to decrease stock qty                
                        cursor.execute('''UPDATE book SET qty = qty - ? 
                                        WHERE b_id = ?''', (qty, b_id))

                        print(f'''\n\nThe book with ID:{b_id} Stock  Qty increase: {qty}.  ''' )
                        ebook.commit()

                        # Create update for write off
                        cursor.execute('''UPDATE book SET wo_qty = wo_qty + ? 
                                    WHERE b_id = ?''', (qty, b_id))
                        print(f'''\nThe book id {b_id} w/o stock has decrease with {qty}''')

                        ebook.commit()
                        ebook.close()

                    elif qty_update == 3:
                        # Create a new or open database called ebookstore_db
                        ebook = sqlite3.connect('ebookstore_db.db')
                        # Create a cursor object
                        cursor = ebook.cursor()

                        b_id = input('''Enter the bookstore id: \n: ''')
                        s_qty = input('''Enter QTY of return stock: \n: ''' )
                                        
                        # creat update to increase stock qty                
                        cursor.execute('''UPDATE book SET s_qty = s_qty - ? 
                                        WHERE b_id = ?''', (s_qty, b_id))

                        print(f'''\n\nThe book with ID:{b_id} Return Qty: {s_qty}.  ''' )
                        ebook.commit()

                        # Create update for write off
                        cursor.execute('''UPDATE book SET wo_qty = wo_qty + ? 
                                    WHERE b_id = ?''', (s_qty, b_id))
                        print(f'''\nThe book id {b_id} w/o stock has increase with {s_qty}''')


                        ebook.commit()
                        ebook.close()

                    elif qty_update == 4:
                        while True:
                            ret_sup = input(''' Was the stock that was return 
                                to supplier written off:
                                    Y - Yes
                                    N - No
                                        :   ''').upper()
                            
                            if ret_sup == "Y" or ret_sup == "YES":
                                # Create a new or open database called ebookstore_db
                                ebook = sqlite3.connect('ebookstore_db.db')
                                # Create a cursor object
                                cursor = ebook.cursor()

                                b_id = input('''Enter the bookstore id: \n: ''')
                                p_qty = input('''Enter QTY of stock return to supplier: \n: ''' )
                                                
                                # creat update to decrease write off stock qty                
                                cursor.execute('''UPDATE book SET wo_qty = wo_qty - ? 
                                                WHERE b_id = ?''', (p_qty, b_id))

                                print(f'''\n\nThe book with ID:{b_id} Return Qty: {p_qty}.  ''' )
                                ebook.commit()

                                # Create update decrease purchase qty
                                cursor.execute('''UPDATE book SET p_qty = p_qty - ? 
                                            WHERE b_id = ?''', (p_qty, b_id))
                                print(f'''\nThe book id {b_id} return stock to supplier {p_qty}''')


                                ebook.commit()
                                ebook.close()

                            elif ret_sup == "N" or ret_sup == "No":
                                # Create a new or open database called ebookstore_db
                                ebook = sqlite3.connect('ebookstore_db.db')
                                # Create a cursor object
                                cursor = ebook.cursor()

                                b_id = input('''Enter the bookstore id: \n: ''')
                                p_qty = input('''Enter QTY of stock return to supplier: \n: ''' )
                                                
                                # creat update to decrease stock qty                
                                cursor.execute('''UPDATE book SET qty = qty - ? 
                                                WHERE b_id = ?''', (p_qty, b_id))

                                print(f'''\n\nThe book with ID:{b_id} Return Qty: {p_qty}.  ''' )
                                ebook.commit()

                                # Create update decrease purchase qty
                                cursor.execute('''UPDATE book SET p_qty = p_qty - ? 
                                            WHERE b_id = ?''', (p_qty, b_id))
                                print(f'''\nThe book id {b_id} return stock to supplier {p_qty}''')


                                ebook.commit()
                                ebook.close()

                            else:
                                print('''\nYou have entered an invalid input''')
                                print('Only enter Y or N')
                                ret_sup = input(''' Was the stock that was return 
                                to supplier writen off:
                                    Y - Yes
                                    N - No
                                        :   ''').upper()

                    elif qty_update == 0:
                        print("\nReturning to the Update Menu")
                        break

                    else:
                        print('''\nYou have entered an invalid input. Only enter 
                            the number. Please try again.''')
                        qty_update = int(input('''Select 1 of the below options why
                        Stock qty needs to update
                            1 - Stock Take
                            2 - Damage: In Store (Write off)
                            3 - Damage: Return from Customers
                            4 - Return to Supplier
                            0 - Return to Task Menu
                                :    '''))
            
            
            elif update_menu == 0:
                print("\nReturning to the Task Menu")
                break
            
            else:
                print('''\nYou have entered an invalid input. 
                        Only enter the number. 
                        Please try again.''')
                update_menu = int(input('''Select one of the following options:
                    1 - Update Title
                    2 - Update Author
                    3 - Update ISBN
                    4 - Update Qty
                    0 - Return to Task Menu
                    :  '''))         
            
        
    elif mainmenu_s == 3:
        print('''\n\nNote that you require the Bookstore ID number to delete
a book from the system. \n''')
        
        book_id_k = input('''Do you have the Bookstore ID:
    Y  -  Yes
    N  -  No
        :   ''').upper()
        
        while True:
            if book_id_k == "Y" or book_id_k == "YES":
                # Open database called ebookstore_db
                ebook = sqlite3.connect('ebookstore_db.db')
                # Create a cursor object
                cursor = ebook.cursor()

                b_id2 = input("\nPlease enter the bookstore ID:  ")

                cursor.execute('''DELETE FROM book Where b_id = ? ''', (b_id2,))
                print(f"\n\nBook with Bookstore ID:{b_id2} was removed from system")
                
                ebook.commit()
                ebook.close()
                break

            elif book_id_k == "N" or book_id_k == "NO":
                print('''\n\nYou do not have the bookstore ID. Please search 
for the book in TASK MENU (option 4).
                      ''')
                break
                
            else:
                print("Invalid Entry. Only enter yes(y) or no(n). ")
                print("Please Try again")
                book_id_k = input('''\nDo you have the Bookstore ID:
                    Y  -  Yes
                    N  -  No
                        :   ''').upper()
                

    elif  mainmenu_s == 4:
        
            while True:
                """ Creat a search menu to give the user option how he would like
                to search for the book"""

                print("\tSearch Menu")

                search_menu = int(input('''Select one of the following options:
                            1 - Qty in Stock
                            2 - Book information 
                            3 - Selling Price
                            0 - Return to Task Menu
                                :  '''))

                    
                if search_menu == 1:
                    while True:

                        sub_menu_search = int(input('''Select one of the following options:
                            1 - Search by Title
                            2 - Search by Author
                            3 - Search by ISBN
                            0 - Return to Search Menu
                                :  '''))
                        
                        if sub_menu_search == 1:
                            # Open database called ebookstore_db
                            ebook = sqlite3.connect('ebookstore_db.db')
                            # Create a cursor object
                            cursor = ebook.cursor()

                            full_name_title = input('''Enter the full title name: \n
                                                    ''').upper()

                            cursor.execute(f'''SELECT b_id, title, author, qty, po_qty FROM book
                                            WHERE title = '{full_name_title}' ''')
                            qty_title_search = cursor.fetchall()
                            
                            print(qty_title_search)
                            
                            ebook.commit()
                            ebook.close()

                        elif sub_menu_search == 2:
                            # Open database called ebookstore_db
                            ebook = sqlite3.connect('ebookstore_db.db')
                            # Create a cursor object
                            cursor = ebook.cursor()

                            full_name_author = input('''Enter the full Author name: \n''').upper()

                            cursor.execute(f'''SELECT b_id, title, author, qty, po_qty FROM book
                                            WHERE author = '{full_name_author}' ''')
                            qty_author_search = cursor.fetchall()
                            
                            print(qty_author_search)

                            ebook.commit()
                            ebook.close()
                            
        
                        elif sub_menu_search == 3:
                            # Open database called ebookstore_db
                            ebook = sqlite3.connect('ebookstore_db.db')
                            # Create a cursor object
                            cursor = ebook.cursor()

                            isbn_number = input('''Please enter the isbn number 
                            (Only numbers, no space): \n:''')

                            cursor.execute(f'''SELECT b_id, title, author, qty, po_qty FROM book
                                            WHERE isbn = '{isbn_number}' ''')
                            qty_isbn_search = cursor.fetchall()
                            
                            print(qty_isbn_search)

                            ebook.commit()
                            ebook.close()
                        
                        elif sub_menu_search == 0:
                            print("\nReturning to the Search Menu")
                            break
                        
                        else:
                            print('''\nYou have entered an invalid input. Only enter the 
        number. Please try again.\n''')
                            sub_menu_search = int(input('''Select one of the following options:
                                1 - Search by Title
                                2 - Search by Author
                                3 - Search by ISBN
                                0 - Return to Search Menu
                                    :  '''))

                elif search_menu == 2:
                    while True:

                        sub_menu_search = int(input('''Select one of the following options:
                            1 - Search by Title
                            2 - Search by Author
                            3 - Search by ISBN
                            0 - Return to Search Menu
                                :  '''))
                        
                        if sub_menu_search == 1:
                            # Open database called ebookstore_db
                            ebook = sqlite3.connect('ebookstore_db.db')
                            # Create a cursor object
                            cursor = ebook.cursor()

                            full_name_title = input('''Enter the full title name: \n
                                                    ''').upper()

                            cursor.execute(f'''SELECT b_id, title, author, isbn FROM book
                                            WHERE title = '{full_name_title}' ''')
                            binfo_title_search = cursor.fetchall()
                            
                            print(binfo_title_search)
                            
                            ebook.commit()
                            ebook.close()

                        elif sub_menu_search == 2:
                            # Open database called ebookstore_db
                            ebook = sqlite3.connect('ebookstore_db.db')
                            # Create a cursor object
                            cursor = ebook.cursor()

                            full_name_author = input('''Enter the full Author name: \n''').upper()

                            cursor.execute(f'''SELECT b_id, title, author, isbn FROM book
                                            WHERE author = '{full_name_author}' ''')
                            binfo_author_search = cursor.fetchall()
                            
                            print(binfo_author_search)

                            ebook.commit()
                            ebook.close()
                            
        
                        elif sub_menu_search == 3:
                            # Open database called ebookstore_db
                            ebook = sqlite3.connect('ebookstore_db.db')
                            # Create a cursor object
                            cursor = ebook.cursor()

                            isbn_number = input('''Please enter the isbn number 
                            (Only numbers, no space): \n:''')

                            cursor.execute(f'''SELECT b_id, title, author, isbn FROM book
                                            WHERE isbn = '{isbn_number}' ''')
                            binfo_isbn_search = cursor.fetchall()
                            
                            print(binfo_isbn_search)

                            ebook.commit()
                            ebook.close()
                        
                        elif sub_menu_search == 0:
                            print("\nReturning to the Search Menu")
                            break
                        
                        else:
                            print('''\nYou have entered an invalid input. Only enter the 
        number. Please try again.\n''')
                            sub_menu_search = int(input('''Select one of the following options:
                                1 - Search by Title
                                2 - Search by Author
                                3 - Search by ISBN
                                0 - Return to Search Menu
                                    :  '''))


                elif search_menu == 3:
                    while True:

                        sub_menu_search = int(input('''Select one of the following options:
                            1 - Search by Title
                            2 - Search by Author
                            3 - Search by ISBN
                            0 - Return to Search Menu
                                :  '''))
                        
                        if sub_menu_search == 1:
                            # Open database called ebookstore_db
                            ebook = sqlite3.connect('ebookstore_db.db')
                            # Create a cursor object
                            cursor = ebook.cursor()

                            full_name_title = input('''Enter the full title name: \n
                                                    ''').upper()

                            cursor.execute(f'''SELECT b_id, title, author, sp FROM book
                                            WHERE title = '{full_name_title}' ''')
                            sp_title_search = cursor.fetchall()
                            
                            print(sp_title_search)
                            
                            ebook.commit()
                            ebook.close()

                        elif sub_menu_search == 2:
                            # Open database called ebookstore_db
                            ebook = sqlite3.connect('ebookstore_db.db')
                            # Create a cursor object
                            cursor = ebook.cursor()

                            full_name_author = input('''Enter the full Author name: \n''').upper()

                            cursor.execute(f'''SELECT b_id, title, author, sp FROM book
                                            WHERE author = '{full_name_author}' ''')
                            sp_author_search = cursor.fetchall()
                            
                            print(sp_author_search)

                            ebook.commit()
                            ebook.close()
                            
        
                        elif sub_menu_search == 3:
                            # Open database called ebookstore_db
                            ebook = sqlite3.connect('ebookstore_db.db')
                            # Create a cursor object
                            cursor = ebook.cursor()

                            isbn_number = input('''Please enter the isbn number 
                            (Only numbers, no space): \n:''')

                            cursor.execute(f'''SELECT b_id, title, author, sp FROM book
                                            WHERE isbn = '{isbn_number}' ''')
                            sp_isbn_search = cursor.fetchall()
                            
                            print(sp_isbn_search)

                            ebook.commit()
                            ebook.close()
                        
                        elif sub_menu_search == 0:
                            print("\nReturning to the Search Menu")
                            break
                        
                        else:
                            print('''\nYou have entered an invalid input. Only 
        enter the number. Please try again.\n''')
                            sub_menu_search = int(input('''Select one of the following options:
                                1 - Search by Title
                                2 - Search by Author
                                3 - Search by ISBN
                                0 - Return to Search Menu
                                    :  '''))
                    
                
                elif search_menu == 0:
                    print("\nReturning to the Task Menu")
                    break


                else:
                    print('''\nYou have entered an invalid input. Only enter the 
        number. Please try again.''')
                    search_menu = int(input('''Select one of the following options:
                            1 - Qty in Stock
                            2 - Book information 
                            3 - Selling Price
                            0 - Return to Task Menu
                                :  '''))
                    

                    print('''\nYou have entered an invalid input. 
                            Only enter the number. 
                            Please try again.''')
                    sub_menu_search = int(input('''Select one of the following options:
                        1 - Search by Title
                        2 - Search by Author
                        3 - Search by ISBN
                        0 - Return to Search Menu
                            :  '''))
        

    elif mainmenu_s == 5:
    
        while True:
            sales_pur_menu = int(input('''Select one of the following options:
                1 - Sales Process
                2 - Sales Report
                3 - Purchase Received
                0 - Return to Task Menu
                    :   '''))
            
            if sales_pur_menu == 1:

                b_id = input('''Enter the bookstore id: \n: ''')
                s_qty1 = input('''Enter sales qty: \n: ''' )
                sp2 = input('''Enter sales price for 1 book: \n:''')

                # Create a new or open database called ebookstore_db
                ebook = sqlite3.connect('ebookstore_db.db')
                # Create a cursor object
                cursor = ebook.cursor()                
                                
                # creat update to increase sales qty                
                cursor.execute('''UPDATE book SET s_qty = s_qty + ? 
                                WHERE b_id = ?''', (s_qty1, b_id))
                print(f'''\nThe book with ID:{b_id} sales Qty increase:{s_qty1}.  ''' )

                ebook.commit()

                # Create update to decrease stock due to sales
                cursor.execute('''UPDATE book SET qty = qty - ? 
                            WHERE b_id = ?''', (s_qty1, b_id))
                print(f'''\nThe book id {b_id} stock has decrease with {s_qty1}''')

                ebook.commit()

                cursor.execute('''Update book SET sp = ?
                               WHERE b_id = ?''', (sp2, b_id))
                print(f'''\n Book Id {b_id} price update to {sp2}\n\n\n''')

                ebook.commit()
                
                #Create update to calculate ts_sp, ts_pp, ts_margin and ts_margin_per
                cursor.execute('''UPDATE book SET ts_sp = ts_sp + (? * ?)
                               WHERE b_id = ?''', (s_qty1, sp2, b_id))
                ebook.commit()

                cursor.execute('''UPDATE book SET ts_pp = ts_pp + (? * pp)
                               WHERE b_id = ?''', (s_qty1, b_id))
                ebook.commit()
                
                margin_results1 = f'''SELECT ts_sp FROM book WHERE b_id = {b_id}'''
                cursor.execute(margin_results1,)
                margin_results1 = cursor.fetchone()[0]

                margin_results2 = f'''SELECT ts_pp FROM book WHERE b_id = {b_id} '''
                cursor.execute(margin_results2,)
                margin_results2 = cursor.fetchone()[0]

                margin_results = margin_results1 - margin_results2
                ebook.commit()

                cursor.execute(f'''UPDATE book SET ts_margin = ? 
                               WHERE b_id = {b_id} ''', (margin_results,))
                ebook.commit()

                margin_perc1 = f'''SELECT ts_sp FROM book WHERE b_id = {b_id} '''
                cursor.execute(margin_perc1,)
                margin_perc1 = cursor.fetchone()[0]

                margin_perc2 = f'''SELECT ts_margin FROM book WHERE b_id = {b_id} '''
                cursor.execute(margin_perc2,)
                margin_perc2 = cursor.fetchone()[0]

                margin_perc = round(((margin_perc2 / margin_perc1) * 100), 2)
                ebook.commit()

                cursor.execute(f'''UPDATE book SET ts_margin_per = ? 
                               WHERE b_id = {b_id} ''', (margin_perc,))
                ebook.commit()

                ebook.close()


            elif sales_pur_menu == 2:
                # Create a new or open database called ebookstore_db
                ebook = sqlite3.connect('ebookstore_db.db')
                # Create a cursor object
                cursor = ebook.cursor()

                cursor.execute('''SELECT b_id, title, s_qty, sp 
                                        FROM book WHERE s_qty > 0
                                        ORDER BY b_id ASC; ''')
                
                book = cursor.fetchall()
                print(book)

                ebook.commit()
                ebook.close()

            elif sales_pur_menu == 3:
                while True:
                    pur_grn = input('''Stock received was it on purchase order:
                        Y - Yes
                        N - No
                            :  ''').upper()
                    
                    if pur_grn == "Y" or pur_grn == "YES":
                        # Create a new or open database called ebookstore_db
                        ebook = sqlite3.connect('ebookstore_db.db')
                        # Create a cursor object
                        cursor = ebook.cursor()

                        b_id = input('''Enter the bookstore id: \n: ''')
                        p_qty = input('''Enter Book qty received: \n: ''' )
                                        
                        # creat update to increase purchase qty                
                        cursor.execute('''UPDATE book SET p_qty = p_qty + ? 
                                        WHERE b_id = ?''', (p_qty, b_id))
                        print(f'''\n\nThe book with ID:{b_id} Purchase Qty capture: {p_qty}.  ''' )

                        ebook.commit()

                        # Create update to increase stock due to recieved
                        cursor.execute('''UPDATE book SET qty = qty + ? 
                                    WHERE b_id = ?''', (p_qty, b_id))
                        print(f'''\nThe book id {b_id} stock has increase with {p_qty}''')

                        ebook.commit()

                        #If PO was create the PO-Qty must decrease
                        cursor.execute('''Update book SET po_qty = po_qty - ?
                                    WHERE b_id = ? ''', (p_qty, b_id))
                        print(f'''\nThe PO qty for book {b_id} has decrease with {p_qty}''')

                        ebook.commit()
                        ebook.close()

                    elif pur_grn == "N" or pur_grn == "NO":
                        # Create a new or open database called ebookstore_db
                        ebook = sqlite3.connect('ebookstore_db.db')
                        # Create a cursor object
                        cursor = ebook.cursor()

                        b_id = input('''Enter the bookstore id: \n: ''')
                        p_qty = input('''Enter Book qty received: \n: ''' )
                                        
                        # creat update to increase purchase qty                
                        cursor.execute('''UPDATE book SET p_qty = p_qty + ? 
                                        WHERE b_id = ?''', (p_qty, b_id))
                        print(f'''\n\nThe book with ID:{b_id} Purchase Qty capture: {p_qty}.  
                              ''' )

                        ebook.commit()

                        # Create update to increase stock due to received
                        cursor.execute('''UPDATE book SET qty = qty + ? 
                                    WHERE b_id = ?''', (p_qty, b_id))
                        print(f'''\nThe book id {b_id} stock has increase with {p_qty}
                            ''')

                        ebook.commit()
                        ebook.close()

                    else:
                       print('''\nYou have entered an invalid input. ''') 
                       print('''Only Enter Y(YES) or N(NO)''')
                       pur_grn = input('''Stock received was it on purchase order:
                        Y - Yes
                        N - No
                            :  ''').upper()

            elif sales_pur_menu == 0:
                print("\n\nReturning to Task Menu")
                break

            else:
                print('''\nYou have entered an invalid input. Only enter the number. 
                    Please try again.''')
                sales_pur_menu = int(input('''Select one of the following options:
                1 - Sales Process
                2 - Sales Report
                3 - Purchase Received
                0 - Return to Task Menu
                    :   '''))
        

    elif mainmenu_s == 6:
        while True:
               
            """If the login user is admin, manager, role they can access finace & 
            Administration."""
        
            # Create dictionary to check the user role
            user_role_c = open("user.txt", "r")
            user_n = []
            user_p = []  
            user_r = []      
            for idata in user_role_c:
                auser_n,buser_p,cuser_r = idata.split(", ") 
                cuser_r = cuser_r.strip()
                user_n.append(auser_n)
                user_p.append(buser_p)
                user_r.append(cuser_r)

            user_roledata = dict(zip(user_n, user_r))
            
            user_role = user_roledata[login_user_name]
                    
            if user_role == "admin" or user_role == "manag":
                
                while True:
                    finance_menu = int(input('''Choose 1 from the following: 
                        1 - Sales Report
                        2 - Place a Purchase Orders
                        3 - Outstanding Purchase Orders Report
                        4 - Write off Report
                        0 - Exit
                            :  '''))
                    
                    if finance_menu == 1:
                        #Retrieve sales data 
                        # Open database called ebookstore_db
                        ebook = sqlite3.connect('ebookstore_db.db')
                        # Create a cursor object
                        cursor = ebook.cursor()

                        cursor.execute('''SELECT b_id, title, s_qty, sp, ts_sp, 
                                       ts_pp, ts_margin, ts_margin_per
                                       FROM book WHERE s_qty > 0
                                        ORDER BY b_id ASC; ''')
                        book = cursor.fetchall()[:]

                        print(book)

                        ebook.commit()
                        ebook.close()


                    elif finance_menu == 2:

                        while True:
                            new_book_order = input('''The book that been ordered 
                            is it new book never stock before? 
                                Y - Yes
                                N - No
                                    :   ''').upper()

                            if new_book_order == "Y" or new_book_order == "YES":
                                print('''Return to Task menu and enter new book 
                                      fist then you can enter the purchase order. 
                                      ''')
                                print("\n\nReturning to Task Menu")
                                break


                            elif new_book_order == "N" or new_book_order == "NO":
                                # Open database called ebookstore_db
                                ebook = sqlite3.connect('ebookstore_db.db')
                                # Create a cursor object
                                cursor = ebook.cursor()
                                
                                b_id4 = input('''Enter the bookstore id for the 
                                    book that been ordered: \n ''')
                                
                                po_qty1 = int(input('''Enter the Qty to purchase \n: 
                                                    '''))
                                                                
                                cursor.execute('''UPDATE book SET po_qty = po_qty + ? 
                                            WHERE b_id = ? ''', (po_qty1, b_id4))
                                
                                print(f'''\nThe Purchase Qty of {po_qty1} for 
                                      book ID: {b_id4} has been updated ''')

                                ebook.commit()
                                ebook.close()


                            else:
                                print('''\nYou have entered an invalid input. 
                                    Only enter the number. Please try again.''')
                                new_book_order = input('''The book that been 
                                    ordered is it new book never stock before? 
                                        Y - Yes
                                        N - No
                                            :   ''').upper()


                    elif finance_menu == 3:
                        # Retrieve all the Books that was order, not received yet
                        # Open database called ebookstore_db
                        ebook = sqlite3.connect('ebookstore_db.db')
                        # Create a cursor object
                        cursor = ebook.cursor()

                        cursor.execute('''SELECT b_id, title, po_qty, pp 
                                        FROM book WHERE po_qty > 0
                                        ORDER BY b_id ASC; ''')
                        book = cursor.fetchall()

                        print(book)

                        ebook.commit()
                        ebook.close()


                    elif finance_menu == 4:
                        #Retrieve write off data 
                        # Open database called ebookstore_db
                        ebook = sqlite3.connect('ebookstore_db.db')
                        # Create a cursor object
                        cursor = ebook.cursor()

                        cursor.execute('''SELECT b_id, title, wo_qty, pp 
                                        FROM book WHERE wo_qty > 0
                                        ORDER BY b_id ASC; ''')
                        book = cursor.fetchall()

                        print(book)

                        ebook.commit()
                        ebook.close()

                    elif finance_menu == 0:
                        print("\n\nGoodbey\n")
                        exit()

                    else:
                        print('''\nYou have entered an invalid input. 
                        Only enter the number. Please try again.''')
                        finance_menu = int(input('''Choose 1 from the following: 
                            1 - Sales Report
                            2 - Purchase Orders
                            3 - Outstanding Purchase Orders Report
                            4 - Write off Report
                            0 - Return to Task Menu
                                :  '''))
        
            else:
                print("\n\nYou are not able to access Finance.\n\n")
                break  


    elif mainmenu_s == 7:
        """If the login user is admin, manager, role they can access finace & 
        Administration."""
    
        # Create dictionary to check the user role
        user_role_c = open("user.txt", "r")
        user_n = []
        user_p = []  
        user_r = []      
        for idata in user_role_c:
            auser_n,buser_p,cuser_r = idata.split(", ") 
            cuser_r = cuser_r.strip()
            user_n.append(auser_n)
            user_p.append(buser_p)
            user_r.append(cuser_r)

        user_roledata = dict(zip(user_n, user_r))
        
        user_role = user_roledata[login_user_name]
                
        if user_role == "admin" or user_role == "manag":

            while True:
                admin_menu = int(input('''Select one of the following options:
                    1 - Add New User
                    2 - Updated Bookstore ID
                    0 - Return to Task Menu
                        :   '''))
                
                if admin_menu == 1:
                    """ Ask how many new users is required to add. That helps not 
                    to go back into menu or start over to add more users.""" 
                    num_new_user = int(input('''Please enter the number of new 
user to be added: \n'''))
                    num_new_user_p = num_new_user + 1
                    num_new_user_n = num_new_user - 1

                    for i in range(1, num_new_user_p):
                        with open('user.txt', 'a+' ) as new_userfile:
                            if i <= num_new_user_p:
                                user_details = open("user.txt", "r")

                                user_name = input('''Please enter new user name \n
                                            (Username must be at least 4 characters): \n
                                            ''').upper() 
                                
                                # Create a dictionary to check if the user does exits
                                user_n = []
                                user_p = []  
                                user_r = []      
                                for idata in user_details:
                                    auser_n,buser_p,cuser_r = idata.split(", ") 
                                    cuser_r = cuser_r.strip()
                                    user_n.append(auser_n)
                                    user_p.append(buser_p)
                                    user_r.append(cuser_r)
                                
                                user_data = dict(zip(user_n, user_p))

                                """Create 2 while loop to make sure the input is more 
                                than 4 characters and that the user name do not exist 
                                all ready."""
                                while len(user_name) <= 5:
                                    print("Username must be at least 6 characters.")
                                    user_name = input('''Please enter new user name: \n
                                                    ''').upper()
                                    continue

                                while user_name in user_n:
                                    print("Username all ready exist")
                                    user_name = input('''Please enter new user name: \n
                                                    ''').upper()
                                    continue

                            # user to input new password     
                                user_pass = input('''Please enter new password 
                                                \n(Password needs to be at least 6 
                                                characters): \n''')
                                
                                while len(user_pass) < 6:
                                    print('''The password you have enter is smaller
                                        than 6 Characters.''')
                                    user_pass = input("Please re-enter new password: \n")
                                    continue
                                
                                """user to re-enter password to confirm it match and 
                                use a while loop to for the process to go on"""
                                user_pass_c = input('''Please re-enter the password: \n
                                                    ''')
                                
                                while user_pass != user_pass_c:
                                    print("The passwords do not match")
                                    user_pass = input("Please re-enter new password: \n")
                                    user_pass_c = input("Please re-confirm password: \n")
                                    if user_pass == user_pass_c:
                                        continue
                                
                                # add a user role.
                                user_role = input('''Select one of the following user role:
                                                Admin - IT Administrator
                                                Manag - Manager
                                                Clerk - Clerk
                                                : \n''').lower()    
                                
                                new_userfile.write("\n" + user_name + ", " 
                                                + user_pass + ", " + user_role)
                                
                                print("User details created successful.")

                        new_userfile.close

                elif admin_menu == 2:
                    # Only Admin and managager can update or change Bookstore ID
                    # Open database called ebookstore_db
                    ebook = sqlite3.connect('ebookstore_db.db')
                    # Create a cursor object
                    cursor = ebook.cursor()

                    isbn2 = input('''Enter the ISBN number of the Book that 
                                  you require to change bookstore ID:  \n''' )
                    b_id3 = input('''Enter the updated bookstore id for the book: \n
                                  ''')
                    
                    cursor.execute('''UPDATE book SET b_id = ? 
                                   WHERE isbn = ?''', (b_id3, isbn2))
                    
                    print(f'''The book with ISBN: {isbn2} numberwas updated 
                          with Bookstore ID: {b_id3}.  ''' )
                    
                    ebook.commit()
                    ebook.close()


                elif admin_menu == 0:
                    print("\n\nReturning to Task Menu")
                    break

                else:
                    print('''\nYou have entered an invalid input. Only enter the number. 
                        Please try again.''')
                    admin_menu = int(input('''Select one of the following options:
                        1 - Add New User
                        2 - Update Bookstore ID
                        0 - Return to Task Menu
                            :   '''))
                    
        else:
            print("\n\nYou are not able to access Administration.\n\n")


    elif mainmenu_s == 0:
        ebook.close()
        print('Goodbye!!!')
        exit()


    else:
        print("You have entered an invalid input. Please try again")

#---------------------------------------------------------------------------


