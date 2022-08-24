from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website_name = website_input.get()
    username = email_input.get()
    password = password_input.get()
    new_data = {website_name: {
        'Email': username,
        'Password': password,
    }
    }

    if len(website_name) == 0 or len(password) == 0:
        messagebox.showinfo(title='Error', message="Please don't leave any fields empty!")

    # Method 1 for storing data in a txt file
    # else:
    #     is_ok = messagebox.askokcancel(title=website_name, message=f'These are the details entered: \nEmail: {username}'
    #                                                                f'\nPassword: {password} \nIs it okay to save?')
    #
    #     if is_ok:
    #         with open('data.txt', "a") as data_file:
    #             data_file.write(f'{website_name} | {username} | {password}\n')
    #             website_input.delete(0, END)
    #             password_input.delete(0, END)

    # Method 2 for storing data as json file.
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #

def search():
    search_website = website_input.get()
    try:
        with open('data.json', "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title='Error', message='No Data File Found.')
    else:
        if search_website in data:
            user_info = data[search_website]
            messagebox.showinfo(title=search_website, message=f'Email: {user_info["Email"]}\nPassword: {user_info["Password"]}')
        else:
            messagebox.showinfo(title='Error', message=f'No details for {search_website} exists.')


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text='Website:', font=('Times New Roman', 10, 'normal'))
website_label.grid(row=1, column=0)

email_label = Label(text='Email/Username:', font=('Times New Roman', 10, 'normal'))
email_label.grid(row=2, column=0)

password_label = Label(text='Password:', font=('Times New Roman', 10, 'normal'))
password_label.grid(row=3, column=0)

# Entries
website_input = Entry(width=34)
website_input.grid(row=1, column=1)
website_input.focus()

email_input = Entry(width=53)
email_input.grid(row=2, column=1, columnspan=2)
email_input.insert(0, 'xyz@gmail.com')

password_input = Entry(width=34)
password_input.grid(row=3, column=1)

# Buttons
password_button = Button(text='Generate Password', command=generate_password)
password_button.grid(row=3, column=2)

add_button = Button(text='Add', width=45, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text='Search', width=15, command=search)
search_button.grid(row=1, column=2)

window.mainloop()
