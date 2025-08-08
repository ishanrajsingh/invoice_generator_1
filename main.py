'''from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

class InvoiceGenerator(App):
    def build(self):
        self.invoice_data = {}

        # Main layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Input fields
        layout.add_widget(Label(text='Customer Name:'))
        self.customer_name_input = TextInput(multiline=False)
        layout.add_widget(self.customer_name_input)

        layout.add_widget(Label(text='Product Name:'))
        self.product_name_input = TextInput(multiline=False)
        layout.add_widget(self.product_name_input)

        layout.add_widget(Label(text='Quantity:'))
        self.quantity_input = TextInput(multiline=False, input_type='number')
        layout.add_widget(self.quantity_input)

        layout.add_widget(Label(text='Price per Unit:'))
        self.price_input = TextInput(multiline=False, input_type='number')
        layout.add_widget(self.price_input)

        # Generate Invoice Button
        generate_button = Button(text='Generate Invoice')
        generate_button.bind(on_press=self.generate_invoice)
        layout.add_widget(generate_button)

        return layout

    def generate_invoice(self, instance):
        customer_name = self.customer_name_input.text.strip()
        product_name = self.product_name_input.text.strip()
        quantity = self.quantity_input.text.strip()
        price_per_unit = self.price_input.text.strip()

        if not customer_name or not product_name or not quantity or not price_per_unit:
            self.show_error_popup('Please fill in all fields.')
            return

        total_price = float(quantity) * float(price_per_unit)

        invoice_text = (
            f"Customer: {customer_name}\n"
            f"Product: {product_name}\n"
            f"Quantity: {quantity}\n"
            f"Price per Unit: {price_per_unit}\n"
            f"Total Price: {total_price}"
        )

        self.show_invoice_popup(invoice_text)

    def show_error_popup(self, message):
        error_popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        error_popup.open()

    def show_invoice_popup(self, invoice_text):
        invoice_popup = Popup(title='Invoice', content=Label(text=invoice_text), size_hint=(None, None), size=(400, 200))
        invoice_popup.open()


if __name__ == '__main__':
    InvoiceGenerator().run()
'''

import tkinter
from tkinter import ttk
from docxtpl import DocxTemplate
import datetime
import datetime as dt
from tkinter import messagebox,simpledialog,filedialog
from tkcalendar import *
import os
import getpass
import platform
from PIL import Image, ImageTk
from urllib.request import urlopen
import requests
import shutil
from journeys_sample import options
import csv
from docx import Document
import subprocess
import pandas

global customer_info_exists
customer_info_exists = False

username = getpass.getuser()
customer_info_excel_path = f"/Users/{username}/Desktop/customer_info.xlsx"

image_url = "https://complainthub.in/wp-content/uploads/2023/08/DTDC-logo.png"
response = requests.get(image_url,stream=True)

img = open("icon.jpg","wb")

response.raw_decode_content = True

shutil.copyfileobj(response.raw,img)

del response
def toggle_fullscreen(event=None):
    state = not window.attributes('-fullscreen')
    window.attributes('-fullscreen', state)
    if state:  # If entering fullscreen
        window.geometry('{0}x{1}+0+0'.format(window.winfo_screenwidth(), window.winfo_screenheight()))
    else:  # If exiting fullscreen
        window.geometry('800x600')  # Set the initial window size
        #frame.size('800x600')
def set_fullscreen():
    window.attributes('-fullscreen', True)
    window.geometry('{0}x{1}+0+0'.format(window.winfo_screenwidth(), window.winfo_screenheight()))

def read_csv_to_dict(filename):
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            my_dict = {row[0]: row[1] for row in reader}
        return my_dict
    except FileNotFoundError:
        return {}
# CSV file to store the dictionary data
csv_filename = 'journeys_data.csv'

# Read the initial data from the CSV file into the dictionary
journeys_dictionary = read_csv_to_dict(csv_filename)

#recent invoices generated
MAX_RECENT_FILES = 5
recent_files = []
RECENT_FILES_CSV = "recent_files_stored.csv"

def open_file(file_path):
    try:
        if platform.system() == "Windows":
            subprocess.Popen(["start", "", file_path], shell=True)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", file_path])
        elif platform.system() == "Linux":
            subprocess.Popen(["xdg-open", file_path])
        else:
            #print(f"Unsupported platform: {platform.system()}")
            messagebox.showerror("Unsupported platforn",f"Unsupported platform: {platform.system()}")

    except FileNotFoundError:
        #print(f"File not found: {file_path}")
        messagebox.showerror("File not found",f"File not found: Either the file has been deleted or moved to another location- {file_path}")
    except Exception as e:
        #print(f"An error occurred: {e}")
        messagebox.showerror("An error occured",f"An error occurred: {e}")
    except FileExistsError:
        messagebox.showerror("File not found", f"File not found: Either the file has been deleted or moved to another location- {file_path}")
    else:
        messagebox.showerror("File not found", f"File not found: Either the file has been deleted or moved to another location- {file_path}")

'''def open_file_dialog():
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        open_file(file_path)
        update_recent_files_menu(file_path,recent_files)'''

def open_recent_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as file:
            content = file.read()
            #print(content)
            # You can perform further actions with the file content here
    except FileNotFoundError:
        #print(f"File not found: {file_path}")
        messagebox.showerror("File not found", f"File not found: {file_path}")
    except UnicodeDecodeError as e:
        #print(f"Error decoding the file: {e}")
        messagebox.showerror("An error occured", f"An error occurred: {e}")
        # Handle the decoding error here

def update_recent_files_menu(new_file, recent_files):
    # Add the new file to the recent files list
    recent_files.insert(0, new_file)
    # Keep only the first MAX_RECENT_FILES files in the list
    recent_files = recent_files[:MAX_RECENT_FILES]

    # Update the Recent Files menu dynamically
    recent_menu.delete(0, tkinter.END)
    for i, file_path in enumerate(recent_files):
        label = f"Invoice {i + 1} :// {file_path}" if i + 1 <= len(recent_files) else file_path
        recent_menu.add_command(label=label, command=lambda path=file_path: open_file(path))
    # Save recent files to CSV
    save_recent_files_to_csv(recent_files)
    on_treeview_select()

def save_recent_files_to_csv(recent_files):
    with open(RECENT_FILES_CSV, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["File Path"])  # Header
        for file_path in recent_files:
            csv_writer.writerow([file_path])

def load_recent_files_from_csv():
    recent_files = []
    try:
        with open(RECENT_FILES_CSV, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header
            for row in csv_reader:
                recent_files.append(row[0])
    except FileNotFoundError:
        #messagebox.showerror("No files found", f"No recent files found, please generate invoice")
        pass  # CSV file doesn't exist yet

    return recent_files
recent_files = load_recent_files_from_csv()
def write_dict_to_csv(filename, my_dict):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for key, value in my_dict.items():
            writer.writerow([key, value])

def move_up():
    selected_item = tree.selection()
    if selected_item:
        above_item = tree.prev(selected_item)
        if above_item:
            tree.move(selected_item, tree.parent(selected_item), tree.index(above_item))
            item_values = list(tree.item(selected_item, "values"))
            converted_values = []
            #print(item_values)
            for value in item_values:
                try:
                    converted_value = int(value)
                except ValueError:
                    try:
                        converted_value = float(value)
                    except ValueError:
                        converted_value = value
                converted_values.append(converted_value)
            #print(converted_values)
            #print(invoice_list)
            invoice_list.remove(converted_values)
            invoice_list.insert(tree.index(above_item)-1,converted_values)
            #print(invoice_list)
            enable_disable_buttons()

def move_down():
    selected_item = tree.selection()
    if selected_item:
        below_item = tree.next(selected_item)
        if below_item:
            tree.move(selected_item, tree.parent(selected_item), tree.index(below_item) + 1)
            #print(tree.index(below_item))
            item_values = list(tree.item(selected_item, "values"))
            converted_values = []
            # print(item_values)
            for value in item_values:
                try:
                    converted_value = int(value)
                except ValueError:
                    try:
                        converted_value = float(value)
                    except ValueError:
                        converted_value = value
                converted_values.append(converted_value)
            # print(converted_values)
            print(invoice_list,"before")
            invoice_list.remove(converted_values)
            invoice_list.insert(tree.index(below_item)-1, converted_values)
            print(invoice_list,"after")
            enable_disable_buttons()

def enable_disable_buttons(move_up_button,move_down_button):
    selected_item = tree.selection()
    if selected_item:
        move_up_button["state"] = "normal"
        move_down_button["state"] = "normal"
    else:
        move_up_button["state"] = "disabled"
        move_down_button["state"] = "disabled"


def clear_item():
    qty_spinbox.delete(0, tkinter.END)
    qty_spinbox.insert(0, "1")
    extra_description.delete(0,tkinter.END)
    extra_price.delete(0,tkinter.END)
    extra_price.insert(0,0)
    #desc_entry.delete(0, tkinter.END)
    #price_spinbox.delete(0, tkinter.END)
    #price_spinbox.insert(0, "0.0")


invoice_list = []
extra_invoice_list = []


def add_item():
    qty = int(qty_spinbox.get())
    journey = ""
    #desc = desc_entry.get()
    journey_selected = variable.get()
    if journey_selected == "Add A New Journey":
        messagebox.showerror("No Journey Selected","Please Select Journey")
    if journey_selected != "Add A New Journey":
        journey = variable.get()
        #print(journey)
    price = float(price_spinbox.cget("text"))
    line_total = qty * price


    if journey!="":
        invoice_item = [qty, journey, price, line_total]
        invoice_list.append(invoice_item)
        tree.insert('', 0, values=invoice_item)
        clear_item()

def add_extra_item():
    #qty = int(qty_spinbox.get())
    try:
        extra_price_get = int(extra_price.get())
    except ValueError:
        messagebox.showerror("Enter Valid Price","Please enter a valid price")
        extra_price_get = 0

    '''try:
        line_total = qty * extra_price_get
    except UnboundLocalError:
        pass'''
    if extra_description.get()!="":
        invoice_extra_item = [extra_description.get(),extra_price_get]
        extra_invoice_list.append(invoice_extra_item)
        extra_tree.insert('',0,values=invoice_extra_item)
        clear_item()
    else:
        messagebox.showerror("Extra details required","Please Enter Extra Details")

def update_customer_info(name, phone, email):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    customer_info_file = os.path.join(desktop_path, 'customer_info.xlsx')

    # Read existing customer information from Excel
    try:
        customer_df = pandas.read_excel(customer_info_file)
    except FileNotFoundError:
        # If the file doesn't exist, create a new DataFrame
        customer_df = pandas.DataFrame(columns=['Name', 'Phone', 'Email'])

    # Check if the customer is already in the DataFrame
    customer_exists = customer_df[(customer_df['Name'] == name) & (customer_df['Phone'] == phone) & (customer_df['Email'] == email)].empty

    # If the customer doesn't exist, add a new row
    if customer_exists:
        new_customer = pandas.DataFrame({'Name': [name], 'Phone': [phone],'Email': [email]})
        customer_df = pandas.concat([customer_df, new_customer], ignore_index=True)

        # Save the updated customer information to Excel
        customer_df.to_excel(customer_info_file, index=False)

def open_excel_file(file_path):
    try:
        if platform.system() == "Windows":
            subprocess.Popen(["start", "", file_path], shell=True)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", file_path])
        elif platform.system() == "Linux":
            subprocess.Popen(["xdg-open", file_path])
        else:
            # print(f"Unsupported platform: {platform.system()}")
            messagebox.showerror("Unsupported platforn", f"Unsupported platform: {platform.system()}")

    except FileNotFoundError:
        # print(f"File not found: {file_path}")
        messagebox.showerror("No Customer Details Exists, Please Generate Invoice to get customer details")
    except Exception as e:
        # print(f"An error occurred: {e}")
        messagebox.showerror("An error occured", f"An error occurred: {e}")


def new_invoice():
    first_name_entry.delete(0, tkinter.END)
    last_name_entry.delete(0, tkinter.END)
    phone_entry.delete(0, tkinter.END)
    email_entry.delete(0, tkinter.END)
    #from_date_entry.delete(0, tkinter.END)
    #from_date_entry.insert(0, f"{datetime.datetime.now().day}/{datetime.datetime.now().month}/{datetime.datetime.now().year}")
    #to_date_entry.delete(0, tkinter.END)
    #to_date_entry.insert(0, f"{datetime.datetime.now().day}/{datetime.datetime.now().month}/{datetime.datetime.now().year}")
    clear_item()
    tree.delete(*tree.get_children())
    extra_tree.delete(*extra_tree.get_children())

    invoice_list.clear()
    extra_invoice_list.clear()

def generate_invoice():

    doc = DocxTemplate("invoice_template.docx")
    #context = {'title': 'Read-Only Document', 'content': 'This document is set to read-only.'}
    name = first_name_entry.get() + last_name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    main_subtotal = sum(item[3] for item in invoice_list) if invoice_list else 0
    extra_subtotal = sum(extra_item[1] for extra_item in extra_invoice_list) if extra_invoice_list else 0
    subtotal = main_subtotal+extra_subtotal
    salestax = 0.18
    total = subtotal * (1 + salestax)
    username = getpass.getuser()
    doc_path = f"/Users/{username}/Desktop/new_invoice"
    doc.render({"name": name,
                "phone": phone,
                "invoice_list": invoice_list,
                "extra_invoice_list": extra_invoice_list,
                "subtotal": subtotal,
                "salestax": str(salestax * 100) + "%",
                "total": total})

    doc_name = doc_path + name + datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S") + ".docx"
    #x=datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    #save_directory = filedialog.askdirectory(title="Select Directory to Save Invoice")
    #doc_name = save_directory
    #print(doc_name)
    if doc_name:
        global customer_info_exists
        #invoice_file_path = os.path.join(save_directory, f"{name} new invoice {x}.docx")
        doc.save(doc_name)
        #invoice_file_path = os.path.join(save_directory,"invoice.docx")
        #doc.save(invoice_file_path)

        messagebox.showinfo("Invoice Complete", "Invoice Complete")
        #recent_files.append(doc_name)
        update_recent_files_menu(os.path.abspath(doc_name),recent_files)
        update_customer_info(name, phone, email)
        customer_info_exists = True
        new_invoice()
    else:
        pass


window = tkinter.Tk()
window.title("Invoice Generator Form")
window.config(background="papayawhip")
img = tkinter.Image('photo',file="icon.jpg")
#img = Image.open(requests.get("https://3.imimg.com/data3/CN/WQ/MY-4334925/dtdc-courier-service.jpg", stream=True).raw)
window.tk.call('wm','iconphoto',window._w,img)
window.minsize(width=850,height=600)
#window.bind("<F11>", toggle_fullscreen)
def on_treeview_select():
    # Check if any item is selected in the Treeview
    selected_items = tree.selection()
    if selected_items:
        # Enable the delete button if an item is selected
        delete_button["state"] = "normal"
        edit_menu.entryconfig("Remove Selected Entry",state=tkinter.NORMAL)
    else:
        # Disable the delete button if no item is selected
        delete_button["state"] = "disabled"
        edit_menu.entryconfig("Remove Selected Entry", state=tkinter.DISABLED)

def on_extra_treeview_select():
    # Check if any item is selected in the Treeview
    selected_items = extra_tree.selection()
    if selected_items:
        # Enable the delete button if an item is selected
        delete_extra_button["state"] = "normal"
        edit_menu.entryconfig("Remove Selected Extra Entry",state=tkinter.NORMAL)
    else:
        # Disable the delete button if no item is selected
        delete_extra_button["state"] = "disabled"
        edit_menu.entryconfig("Remove Selected Extra Entry", state=tkinter.DISABLED)

def delete_selected_entry():
    selected_item = tree.selection()
    #print(selected_item)
    #print(invoice_list)
    if selected_item:
        item_values = list(tree.item(selected_item, "values"))
        converted_values = []
        for value in item_values:
            try:
                converted_value = int(value)
            except ValueError:
                try:
                    converted_value = float(value)
                except ValueError:
                    converted_value = value
            converted_values.append(converted_value)
        tree.delete(selected_item)
        #print(converted_values)
        #print(invoice_list)
        invoice_list.remove(converted_values)
        #print(item_values)
        delete_button["state"] = "disabled"

def delete_selected_extra_entry():
    selected_item = extra_tree.selection()
    # print(selected_item)
    # print(invoice_list)
    if selected_item:
        item_values = list(extra_tree.item(selected_item, "values"))
        converted_values = []
        for value in item_values:
            try:
                converted_value = int(value)
            except ValueError:
                try:
                    converted_value = float(value)
                except ValueError:
                    converted_value = value
            converted_values.append(converted_value)
        extra_tree.delete(selected_item)
        # print(converted_values)
        # print(invoice_list)
        extra_invoice_list.remove(converted_values)
        # print(item_values)
        delete_extra_button["state"] = "disabled"

def delete_option_journey():
    selected_key = variable.get()
    if selected_key != "Add A New Journey":
        confirmation = messagebox.askyesno("Confirmation", f"Do you want to delete '{selected_key}'?")
        if confirmation:
            del journeys_dictionary[selected_key]
            update_values()
            write_dict_to_csv(csv_filename, journeys_dictionary)
            variable.set(list(journeys_dictionary.keys())[len(list(journeys_dictionary.keys()))-1])  # Clear the current selection
    if selected_key == "Add A New Journey":
        messagebox.showerror("No Journey Selected","Please Select A Journey To Delete")

def center_frame(frame):
    frame.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()

    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)

    frame.place(x=x, y=y)

def draw_rounded_rectangle(canvas, x, y, width, height, radius, color):
    # Draw a rounded rectangle on the canvas
    canvas.create_polygon(
        x + radius, y,
        x + width - radius, y,
        x + width, y + radius,
        x + width, y + height - radius,
        x + width - radius, y + height,
        x + radius, y + height,
        x, y + height - radius,
        x, y + radius,
        fill=color,
        outline=color
    )
def get_entry_default_width(entry):
    # Trigger the widget to calculate its default width
    entry.update_idletasks()
    # Return the default width of the entry widget
    return entry.winfo_reqwidth()

def on_treeview_scroll(*args):
    tree.yview(*args)

def on_extra_treeview_scroll(*args):
    extra_tree.yview(*args)

def set_small_dimensions():
    window.geometry('700x800')
# Bind the Escape key to exit fullscreen
#window.bind("<Escape>", lambda event: set_small_dimensions())

# Toggle fullscreen at startup
toggle_fullscreen()
frame = tkinter.Frame(window,background="papayawhip")
#frame.pack(padx=20, pady=10)
frame.grid(padx=20,pady=10)
#frame.pack_propagate(False)
center_frame(frame)
#canvas = tkinter.Canvas(frame, width=150, height=50, highlightthickness=0)
#canvas.grid(row=0, column=0)
#draw_rounded_rectangle(canvas, 50, 50, 150, 50, 20, "lightblue")
# Get the default width of the Entry widget

#entry_default_width = get_entry_default_width(first_name_entry)
first_name_label = tkinter.Label(frame, text="First Name",background="MistyRose2",borderwidth=10,highlightthickness="2",highlightbackground="NavajoWhite2",width=15,relief=tkinter.RIDGE)
first_name_label.grid(row=0, column=0,padx=10)
last_name_label = tkinter.Label(frame, text="Last Name",background="MistyRose2",relief=tkinter.RIDGE,borderwidth=10,highlightthickness="2",highlightbackground="NavajoWhite2",width=15)
last_name_label.grid(row=0, column=1,pady=10,padx=0)

first_name_entry = tkinter.Entry(frame,background="white",highlightthickness="2",highlightbackground="NavajoWhite3",width=20,relief=tkinter.RIDGE)
first_name_entry.grid(row=1, column=0,ipady=2,pady=10)

last_name_entry = tkinter.Entry(frame,background="white",highlightthickness="2",highlightbackground="NavajoWhite3",width=20,relief=tkinter.RIDGE)

last_name_entry.grid(row=1, column=1,ipady=2,pady=0)

phone_label = tkinter.Label(frame, text="Phone",background="MistyRose2",relief=tkinter.RIDGE,borderwidth=10,highlightthickness="2",highlightbackground="NavajoWhite2",width=15)
phone_label.grid(row=0, column=2,padx=0)
phone_entry = tkinter.Entry(frame,background="white",highlightthickness="2",highlightbackground="NavajoWhite3",width=20,relief=tkinter.RIDGE)
phone_entry.grid(row=1, column=2,ipady=2,pady=0)

email_label = tkinter.Label(frame,text="Email",background="MistyRose2",relief=tkinter.RIDGE,borderwidth=10,highlightthickness="2",highlightbackground="NavajoWhite2",width=15)
email_label.grid(row=0,column=3,padx=0)
email_entry = tkinter.Entry(frame,background="white",highlightthickness="2",highlightbackground="NavajoWhite3",width=20,relief=tkinter.RIDGE)
email_entry.grid(row=1,column=3,ipady=2,pady=10)

qty_label = tkinter.Label(frame, text="No.of Persons",relief=tkinter.RIDGE,background="MistyRose2",borderwidth=10,highlightthickness="2",highlightbackground="NavajoWhite2",width=15)
qty_label.grid(row=2, column=0,pady=10)
qty_spinbox = tkinter.Spinbox(frame, from_=1, to=100,background="white",borderwidth=10,highlightthickness="2",highlightbackground="NavajoWhite2",width=17,relief=tkinter.FLAT)
qty_spinbox.grid(row=3, column=0)

variable = tkinter.StringVar(window)
#options = {"one": 1, "two": 2, "three": 3}
#variable.set("Sangha")
variable.set(list(journeys_dictionary.keys())[len(list(journeys_dictionary.keys()))-1])

price_label = tkinter.Label(frame, text="Unit Price ($)",relief=tkinter.RIDGE,background="MistyRose2",borderwidth=10,highlightthickness="2",highlightbackground="NavajoWhite2",width=15)
price_label.grid(row=2, column=2)
price_spinbox = tkinter.Label(frame,text=(journeys_dictionary[variable.get()]),state="disabled",background="white",borderwidth=10,highlightthickness="2",highlightbackground="NavajoWhite2",width=15,relief=tkinter.FLAT)
price_spinbox.grid(row=3, column=2)
#move_up_button = tkinter.Button(frame, text="Move Up", command=move_up,state="disabled")
#move_down_button = tkinter.Button(frame, text="Move Down", command=move_down,state="disabled")
#move_up_button.grid(row=5,column=5)
#move_down_button.grid(row=5,column=6)
# Bind arrow keys to move functions
#window.bind("<Up>", lambda event: move_up())
#window.bind("<Down>", lambda event: move_down())
def add_journey_window():
    popup_window = tkinter.Toplevel(frame)
    popup_window.title("Add A New Journey")

    # Entry widgets for user input
    entry1_label = ttk.Label(popup_window, text="Journey:")
    entry1_entry = ttk.Entry(popup_window)

    entry2_label = ttk.Label(popup_window, text="Price:")
    entry2_entry = ttk.Entry(popup_window)

    entry1_label.grid(row=0, column=0, padx=10, pady=5, sticky=tkinter.W)
    entry1_entry.grid(row=0, column=1, padx=10, pady=5)

    entry2_label.grid(row=1, column=0, padx=10, pady=5, sticky=tkinter.W)
    entry2_entry.grid(row=1, column=1, padx=10, pady=5)

    # Button to process entries
    submit_button = ttk.Button(popup_window, text="Submit", command=lambda: process_entries(entry1_entry.get(), entry2_entry.get()))
    submit_button.grid(row=2, column=0, columnspan=2, pady=10)

def add_journey_popup():

        new_key = simpledialog.askstring("Input", "Enter a new Journey:")
        if new_key is not None:
            new_value = simpledialog.askstring("Input", "Enter price:")
            if new_value is not None:
                confirmation = messagebox.askyesno("Confirm to Proceed", "Are you sure you want to add a New Journey")
                if confirmation:
                    journeys_dictionary[new_key] = new_value
                    update_values()
                    write_dict_to_csv(csv_filename, journeys_dictionary)
                    process_entries(new_key,new_value)

def update_values():
    O_menu = tkinter.OptionMenu(frame, variable, *journeys_dictionary.keys(), command=sample)
    O_menu.config(width=17)

    O_menu.grid(row=3, column=1)

def process_entries(entry1_value, entry2_value):
    messagebox.showinfo("Popup Result", f"Journey: {entry1_value}\nPrice: {entry2_value}")
def sample(*args):
    result = variable.get()
    if result == "Add A New Journey":
        #add_journey_window()
        add_journey_popup()
    #print(options[result])
    price_spinbox["text"] = journeys_dictionary[result]

#def recent_file_selected(file_path):
#    pass
# select journey date range
def pick_date(event,date_entry):
    global cal, date_window
    date_window = tkinter.Toplevel(window)
    date_window.geometry('300x300')
    date_window.grab_set()
    date_window.title("Select Journey From Date")
    window.iconify()
    #date_window.iconify()# Minimize the window
    #date_window.geometry('250x220+590+370')
    cal = Calendar(date_window,selectmode="day",date_pattern="dd/mm/y",width=12, background='darkblue', foreground='white', borderwidth=2)
    cal.place(x=0,y=0)

    submit_date_btn = tkinter.Button(date_window,text="Submit",command=lambda: grab_date(date_entry))
    submit_date_btn.place(x=80,y=190)

def grab_date(date_entry):
    date_entry.delete(0,tkinter.END)
    date_entry.insert(0,cal.get_date())
    #toggle_fullscreen()
    window.wm_state("zoomed")
    date_window.destroy()


desc_label = tkinter.Label(frame, text="Journey",relief=tkinter.RIDGE,background="MistyRose2",borderwidth=10,highlightthickness="2",highlightbackground="NavajoWhite2",width=15)
#desc_entry = tkinter.Entry(frame)
desc_label.grid(row=2, column=1)
O_menu = tkinter.OptionMenu(frame, variable, *journeys_dictionary.keys(),command=sample)
O_menu.config(width=17,background="white",borderwidth=0,highlightthickness="2",highlightbackground="NavajoWhite2",relief=tkinter.FLAT)

O_menu.grid(row=3,column=1)
'''
from_label = tkinter.Label(frame,text="From: ")
from_label.grid(row=4,column=5)
from_date_entry = tkinter.Entry(frame)
from_date_entry.grid(row=4,column=6)
from_date_entry.insert(0,f"{datetime.datetime.now().day}/{datetime.datetime.now().month}/{datetime.datetime.now().year}")
to_label = tkinter.Label(frame, text="To: ")
to_label.grid(row=5,column=5)
to_date_entry = tkinter.Entry(frame)
to_date_entry.grid(row=5,column=6)
to_date_entry.insert(0,f"{datetime.datetime.now().day}/{datetime.datetime.now().month}/{datetime.datetime.now().year}")
'''
#desc_entry.grid(row=3, column=1)

#O_menu.pack(padx=100,pady=0)


#bu = tkinter.Button(window, text="print", command=sample).pack()
# Create a style
#style = ttk.Style()

# Configure the style to set separator width and color
#style.configure("TSeparator", thickness=5, background="blue")
add_item_button = tkinter.Button(frame, text="Add item", command=add_item,background="white",borderwidth=0,highlightthickness="2",highlightbackground="NavajoWhite2",width=17,relief=tkinter.FLAT)
add_item_button.grid(row=4, column=2, pady=5)
delete_button = tkinter.Button(frame, text="Delete Selected Item", command=delete_selected_entry,state="disabled",background="white",borderwidth=0,highlightthickness="2",highlightbackground="NavajoWhite2",width=17,relief=tkinter.FLAT)
delete_button.grid(row=4,column=0)
delete_journey_button = tkinter.Button(frame, text="Delete Selected Journey", command=delete_option_journey,background="white",borderwidth=0,highlightthickness="2",highlightbackground="NavajoWhite2",width=17,relief=tkinter.FLAT)
delete_journey_button.grid(row=4,column=1)
add_journey_button = tkinter.Button(frame,text="Add A Joureny", command=add_journey_popup,background="white",borderwidth=0,highlightthickness="2",highlightbackground="NavajoWhite2",width=17,relief=tkinter.FLAT)
add_journey_button.grid(row=4,column=3)
columns = ('qty', 'desc', 'price', 'total')
style = ttk.Style()

# Change background color
style.configure("Treeview", background="bisque",fieldbackground='bisque')

# Change border color
style.map("Treeview", background=[('selected', 'dark salmon')])

# Change borderwidth
style.configure("Treeview", borderwidth=10)
tree = ttk.Treeview(frame, columns=columns, show="headings",selectmode="browse")
tree.heading('qty', text='No.of Persons')
tree.heading('desc', text='Description')
#tree.heading('duration',text='Duration')
tree.heading('price', text='Unit Price')
tree.heading('total', text="Total")


scrollbar = ttk.Scrollbar(frame, orient="vertical", command=on_treeview_scroll)
scrollbar.grid(row=7, column=4, sticky="ns", rowspan=1+len(invoice_list),padx=10,pady=20)
tree.configure(yscrollcommand=scrollbar.set)
tree.grid(row=7, column=1, columnspan=3, padx=0, pady=20,sticky="nsew")
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
columns = ('extra_desc', 'extra_total')
extra_tree = ttk.Treeview(frame, columns=columns, show="headings",selectmode="browse",height=5)
#extra_tree.heading('qty', text='No.of Persons')
extra_tree.heading('extra_desc', text='Extra')
#tree.heading('duration',text='Duration')
#extra_tree.heading('extra_price', text='Unit Price')
extra_tree.heading('extra_total', text="Total")


scrollbar_2 = ttk.Scrollbar(frame, orient="vertical", command=on_extra_treeview_scroll)
scrollbar_2.grid(row=10, column=3, sticky="ns",padx=0,pady=20)
extra_tree.configure(yscrollcommand=scrollbar_2.set)
extra_tree.grid(row=10, column=1, columnspan=2, padx=20, pady=20,sticky="nsew")
frame.grid_rowconfigure(10, weight=1)
frame.grid_columnconfigure(1, weight=1)
separator = ttk.Separator(frame, orient="horizontal")
separator.grid(row=8, column=0, columnspan=5, sticky="ew", padx=0, pady=10)
extra_label = tkinter.Label(frame, text="Extra: ",relief=tkinter.RIDGE,background="MistyRose2",borderwidth=10,highlightthickness="2",highlightbackground="NavajoWhite2",width=15)
extra_label.grid(row=9,column=0,padx=0)
extra_description_label = tkinter.Label(frame, text="Description: ",relief=tkinter.RIDGE,background="MistyRose2",borderwidth=10,highlightthickness="2",highlightbackground="NavajoWhite2",width=15)
extra_description_label.grid(row=9,column=1,padx=10)
extra_description = tkinter.Entry(frame,background="white",highlightthickness="2",highlightbackground="NavajoWhite3",width=20,relief=tkinter.RIDGE)
extra_description.grid(row=9,column=2)
extra_price_label = tkinter.Label(frame, text="Price ($): ",background="MistyRose2",relief=tkinter.RIDGE,borderwidth=10,highlightthickness="2",highlightbackground="NavajoWhite2",width=15)
extra_price_label.grid(row=9,column=3,padx=20)
extra_price = tkinter.Entry(frame,background="white",highlightthickness="2",highlightbackground="NavajoWhite3",width=20,relief=tkinter.RIDGE)
extra_price.grid(row=9,column=4,padx=20)
extra_price.insert(0,0)
add_extra_item_button = tkinter.Button(frame, text="Add extra", command=add_extra_item,background="white",borderwidth=0,highlightthickness="2",highlightbackground="NavajoWhite2",width=17,relief=tkinter.FLAT)
add_extra_item_button.grid(row=10, column=4, pady=20,padx=5)
delete_extra_button = tkinter.Button(frame, text="Delete Selected Extra Item", command=delete_selected_extra_entry,state="disabled",background="white",borderwidth=0,highlightthickness="2",highlightbackground="NavajoWhite2",width=17,relief=tkinter.FLAT)
delete_extra_button.grid(row=11,column=4)
save_invoice_button = tkinter.Button(frame, text="Generate Invoice", command=generate_invoice,background="white",borderwidth=5,highlightthickness="2",highlightbackground="NavajoWhite2",width=17,relief=tkinter.FLAT)
save_invoice_button.grid(row=12, column=1, columnspan=4, sticky="news", padx=20, pady=15)
new_invoice_button = tkinter.Button(frame, text="New Invoice", command=new_invoice,background="white",borderwidth=5,highlightthickness="2",highlightbackground="NavajoWhite2",width=17,relief=tkinter.FLAT)
new_invoice_button.grid(row=13, column=1, columnspan=4, sticky="news", padx=20, pady=5)
#date_range_button = tkinter.Button(frame, text="Select Date Range",command=get_date_range)
#date_range_button.grid(row=4,column=3)


menu_bar = tkinter.Menu(window)

# Create File menu
file_menu = tkinter.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New Invoice",command=new_invoice,accelerator="Ctrl+N")
file_menu.add_command(label="Save Invoice",command=generate_invoice,accelerator="Ctrl+S")

file_menu.add_command(label="Open Last Modified Invoice", command=lambda: open_file(recent_files[0]) if recent_files else messagebox.showerror("No files found","No recent files exists"),accelerator="Ctrl+O")
file_menu.add_command(label="Customer Info",command=lambda: open_excel_file(customer_info_excel_path) if customer_info_exists else messagebox.showerror("No Customer Details Exists", "Please Generate any Invoice to get customer details"),accelerator="Ctrl+I")
recent_menu = tkinter.Menu(file_menu, tearoff=0)
# Update the Recent Files menu whenever a file is opened
file_menu.add_cascade(label="Recent Files", menu=recent_menu)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.destroy)
menu_bar.add_cascade(label="File", menu=file_menu)



if not recent_files:
    recent_menu.add_command(label="No recent files found", state=tkinter.DISABLED)
else:
    for i, file_path in enumerate(recent_files):
        label = f"Invoice {i + 1} :// {file_path}" if i + 1 <= len(recent_files) else file_path
        recent_menu.add_command(label=label, command=lambda path=file_path: open_file(path))

# Add the "Generate Invoice" button
#add known recent files
'''for i, file_path in enumerate(recent_files):
    label = f"Invoice {i + 1} :// {file_path}" if i + 1 <= len(recent_files) else file_path
    recent_menu.add_command(label=label, command=lambda path=file_path: open_file(path))'''

# Create recent files submenu dynamically
#recent_menu = file_menu.nametowidget(file_menu.index("Recent Files"))
#update_recent_menu()

#file_menu.add_separator()
#menu_bar.add_cascade(label="File", menu=file_menu)

# Create Edit menu
edit_menu = tkinter.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Add A Journey",command=add_journey_popup,accelerator="Control+J")
edit_menu.add_command(label="Remove Selected Journey",command=delete_option_journey,accelerator="Control+R")
edit_menu.add_command(label="Add Entry",command=add_item,accelerator="Control+A")
edit_menu.add_command(label="Remove Selected Entry",command=delete_selected_entry,state=tkinter.DISABLED,accelerator="Control+D")
edit_menu.add_command(label="Add Extra",command=add_extra_item,accelerator="Control+X")
edit_menu.add_command(label="Remove Selected Extra Entry",command=delete_selected_extra_entry,state=tkinter.DISABLED,accelerator="Control+E")
menu_bar.add_cascade(label="Edit", menu=edit_menu)

#enable widgets
def widgets_initial_state():
    first_name_label["state"] = "normal"
    last_name_label["state"] = "normal"

def entry_focus(event):
    widgets_initial_state()

# Set the menu bar
window.config(menu=menu_bar)

#delete_selected_entry()
tree.bind("<<TreeviewSelect>>", lambda event: on_treeview_select())
extra_tree.bind("<<TreeviewSelect>>", lambda event: on_extra_treeview_select())
variable.trace_add("write", lambda *args: delete_journey_button.config(state="normal") if variable.get() else delete_journey_button.config(state="disabled"))

#binding keys controls

window.bind("<Control-o>",lambda event: open_file(recent_files[0]) if recent_files else messagebox.showerror("No files found","No recent files exists"))
window.bind("<Control-s>",lambda event: generate_invoice())
window.bind("<Control-n>",lambda event: new_invoice())
window.bind("<Control-a>",lambda event: add_item())
window.bind("<Control-j>",lambda event: add_journey_popup())
window.bind("<Control-r>",lambda event: delete_option_journey())
window.bind("<Control-d>",lambda event: delete_selected_entry())
window.bind("<Control-i>",lambda event: open_excel_file(customer_info_excel_path) if customer_info_exists else messagebox.showerror("No Customer Details Exists", "Please Generate any Invoice to get customer details"))
window.bind("<Control-x>",lambda event: add_extra_item())
window.bind("<Control-e>",lambda event: delete_selected_extra_entry())
#widgets_initial_state()
#from_date_entry.bind("<Button-1>" ,lambda event: pick_date(event,from_date_entry))
#from_date_entry.bind("<FocusIn>",entry_focus)
#to_date_entry.bind("<Button-1>", lambda event: pick_date(event, to_date_entry))

window.mainloop()