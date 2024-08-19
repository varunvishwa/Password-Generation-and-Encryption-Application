from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
from aes_encryption import AES_Encryption
from sha_encryption import SHA_Encryption
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "
                                                      f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            
            #SHA ENCRYPTION
            encrypted_password = SHA_Encryption.sha_encrypt(password)

            print(encrypted_password)

            #AES ENCRYPTION
            x = AES_Encryption("dummykey")
            aes_encrypted_password = x.aes_encrypt(encrypted_password)

            print(aes_encrypted_password)

            data = {
                website: {
                    "email": email,
                    "password": aes_encrypted_password
                    }
                    }
            
            try:
                with open("data.json", "r") as data_file:
                    old_data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            else:
                old_data.update(data)
                with open("data.json", "w") as data_file:
                    json.dump(old_data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

# ---------------------------- SEARCH DATA ------------------------------- #

def search_data():
    website_name = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            file_data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data has been added yet")
    else:
        if website_name in file_data:
            messagebox.showinfo(title="Website Details", message=f"Website: {website_name}\n Email: {file_data[website_name]["email"]}\n Password: {file_data[website_name]["password"]}")
        else:
            messagebox.showinfo(title="Website Details", message="Data not found")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

#Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

#Entries
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "varunvishwa11@gmail.com")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search", command=search_data, width=13)
search_button.grid(row=1, column=2)
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()