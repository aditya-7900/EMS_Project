# ---------------- This Is Made By Aditya Bobade ----------------  #

from tkinter import Toplevel, messagebox, ttk, Button, CENTER, LEFT, Tk, Label, Entry, StringVar
from PIL import Image, ImageTk
import pymysql
import re
# from tkinter import *

# ---------------- DATABASE CONNECTION ----------------  #


def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root@7900",
        database="employee_db"
    )

# ---------------- CRUD OPERATIONS ----------------  #


def show_data():
    view.delete(*view.get_children())
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM emp_db")
        rows = cursor.fetchall()

        # Insert rows with alternating colors
        for index, row in enumerate(rows):
            if index % 2 == 0:
                view.insert("", "end", values=row, tags=("evenrow",))
            else:
                view.insert("", "end", values=row, tags=("oddrow",))

        # Close connection
        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def exit_program():
    win.destroy()


def add_data():
    emp_id = id1.get().strip()
    emp_name = id2.get().strip()
    mob_no = id3.get().strip()
    emp_dept = id4.get().strip()
    emp_salary = id5.get().strip()

    # Validation
    if emp_id == '' or emp_name == '' or mob_no == '' or emp_dept == '' or emp_salary == '':
        messagebox.showinfo('Info', 'ALL fields are compulsory')

    elif not emp_id.isdigit() or int(emp_id) <= 0:
        messagebox.showerror("Error", "Employee ID must be a number")

    elif not re.match(r'^[A-Za-z .]+$', emp_name):
        messagebox.showerror(
            "Error", "Employee Name must contain only letters and spaces")

    elif not re.match(r'^[A-Za-z ]+$', emp_dept):
        messagebox.showerror(
            "Error", "Employee Department must contain only letters and spaces")

    elif not mob_no.isdigit() or len(mob_no) != 10:
        messagebox.showerror("Error", "Mobile Number must be 10 digits")

    elif not emp_salary.isdigit() or int(emp_salary) <= 0:
        messagebox.showerror(
            "Error", "Employee Salary must be a positive number")

    else:
        conn = get_connection()
        qur = f'INSERT INTO emp_db VALUES ("{emp_id}", "{emp_name}", "{mob_no}", "{emp_dept}", "{emp_salary}")'
        cursor = conn.cursor()
        cursor.execute(qur)
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Data Inserted Successfully")

        # Clear input fields
        id1.set("")
        id2.set("")
        id3.set("")
        id4.set("")
        id5.set("")


# ---------------- SALARY MANAGEMENT ----------------  #


def show_salary():
    global win2
    win2 = Toplevel()  # Correct: use Toplevel for new window
    win2.title("Salary Management")
    win2.config(bg="lightblue")
    win2.geometry("1920x1080")  # Optional initial size

    # Load and set background image
    image = Image.open(r"C:\Users\bobad\Data Science\Evening\7 MENTOR\bg5.png")
    image = image.resize((1920, 992), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(image)
    bg_label = Label(win2, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.lower()  # send background to back

    # emp_id >> Label
    l8 = Label(
        win2,
        text="ENTER EMPLOYEE ID",
        bg="white",
        fg="black",
        width=20,
        bd=7,
        relief="ridge",
        font=("times new roman", 12, "bold")
    )
    l8.place(x=450, y=250)

    # emp_id >>> entry
    id8 = StringVar()
    e8 = Entry(
        win2,
        textvariable=id8,
        bg="white",
        width=25,
        bd=5,
        relief="flat",
        font=("times new roman", 12, "bold")
    )
    e8.place(x=700, y=255)
    e8.configure(justify="center")

    # label to display salary
    result_label = Label(
        win2,
        text="",
        font=("Times New Roman", 14, "bold"),
        bg="white",
        fg="black",
        relief="ridge",
        width=34,
        height=5,
        bd=8,
    )
    result_label.place(x=450, y=340)

    # button
    b9 = Button(
        win2,
        text="SHOW SALARY",
        command=lambda: show_sal(id8.get(), result_label),
        relief="ridge",
        bg="gray",
        fg="white",
        bd=4,
        font=("times new roman", 12, "bold"),
        width=15,
    )
    b9.place(x=450, y=500)

# ------------ SHOW SALARY ANOTHER WINDOW ------------

    b10 = Button(
        win2,
        text="SHOW ANALYTICS",
        command=show_analytics,
        relief="ridge",
        bg="gray",
        fg="white",
        bd=4,
        font=("times new roman", 12, "bold"),
        width=15,
    )
    b10.place(x=1000, y=500)

    win2.mainloop()


def show_analytics():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*), AVG(emp_salary), MAX(emp_salary), MIN(emp_salary) FROM emp_db")
    result = cur.fetchone()
    conn.close()
    if result is not None:
        total_employees, avg_salary, max_salary, min_salary = result
    else:
        total_employees, avg_salary, max_salary, min_salary = 0, 0, 0, 0

    # Display results in win2
    Label(
        win2,
        text="Employee Analytics",
        bg="white",
        fg="black",
        width=25,
        bd=5,
        relief="ridge",
        font=("Times New Roman", 18, "bold"),
    ).place(x=1000, y=250)

    Label(
        win2,
        text=f"Total Employees: {int(total_employees)}\n"
        f"Average Salary: {float(avg_salary):,.2f}\n"   # rounded with commas
        f"Highest Salary: {int(max_salary):,}\n"        # safe int cast
        f"Lowest Salary: {int(min_salary):,}",
        font=("Times New Roman", 14),
        bg="white",
        fg="black",
        relief="ridge",
        width=34,
        height=5,
        bd=8,
        justify="left",
    ).place(x=1000, y=340)


# ------------ SHOW SALARY ANOTHER WINDOW ------------

def show_sal(emp_id, result):
    if emp_id == "":
        result.config(text="Please enter an Employee ID")
    elif not emp_id.isdigit():
        result.config(text="Please enter a valid numeric Employee ID")
        return

    emp_id = int(emp_id)
    conn = get_connection()
    cur = conn.cursor()
    # Fetch both name and salary
    cur.execute(
        "SELECT emp_name, emp_salary FROM emp_db WHERE emp_id=%s", (emp_id,))
    row = cur.fetchone()
    conn.close()

    if row:
        emp_name, emp_salary = row  # unpack name and salary
        emp_name = emp_name.title()
        result.config(text=f"Salary of {emp_name} is:  {emp_salary}")
    else:
        result.config(text="Employee not found")


# ---------------- DELETE OPERATION ----------------


def delete_data():
    emp_id = id6.get()
    if emp_id == "":
        messagebox.showerror("Error", "Employee ID is required")
    else:
        # Confirmation before deleting
        confirm = messagebox.askyesno(
            "Confirm Delete", f"Are you sure you want to delete Employee ID {emp_id}?")

        if confirm:  # If YES
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM emp_db WHERE emp_id="{emp_id}"')
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success", f"Employee ID {emp_id} deleted successfully")
            id6.set("")
        else:
            messagebox.showinfo("Cancelled", "Delete operation cancelled")


def select_emp():
    emp_id = id7.get()
    if emp_id == "":
        messagebox.showerror("Error", "Employee ID is required")
    else:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM emp_db WHERE emp_id="{emp_id}"')
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            id1.set(row[0])
            id2.set(row[1])
            id3.set(row[2])
            id4.set(row[3])
            id5.set(row[4])
        else:
            messagebox.showwarning("Error", "Employee not found")


def update_data():
    emp_id = id1.get().strip()
    emp_name = id2.get().strip()
    mob_no = id3.get().strip()
    emp_dept = id4.get().strip()
    emp_salary = id5.get().strip()

    # Validation
    if emp_id == '' or emp_name == '' or mob_no == '' or emp_dept == '' or emp_salary == '':
        messagebox.showinfo('Info', 'ALL fields are compulsory')

    elif not emp_id.isdigit():
        messagebox.showerror("Error", "Employee ID must be a number")

    elif not re.match(r'^[A-Za-z .]+$', emp_name):
        messagebox.showerror(
            "Error", "Employee Name must contain only letters, spaces, and dots")

    elif not re.match(r'^[A-Za-z .]+$', emp_dept):
        messagebox.showerror(
            "Error", "Employee Department must contain only letters, spaces, and dots")

    elif not mob_no.isdigit() or len(mob_no) != 10:
        messagebox.showerror("Error", "Mobile Number must be 10 digits")

    elif not emp_salary.isdigit():
        messagebox.showerror("Error", "Employee Salary must be a number")

    else:
        conn = get_connection()
        mycur = conn.cursor()

        # 🔹 f-string style query
        qur = f'UPDATE emp_db SET emp_name="{emp_name}", mob_no="{mob_no}", emp_dept="{emp_dept}", emp_salary="{emp_salary}" WHERE emp_id="{emp_id}"'

        mycur.execute(qur)
        conn.commit()
        mycur.close()
        conn.close()

        messagebox.showinfo('Info', 'Data updated successfully')

        # Clear fields
        id1.set('')
        id2.set('')
        id3.set('')
        id4.set('')
        id5.set('')
        id7.set('')


def clear_data():
    view.delete(*view.get_children())


# ---------------- GUI SECTION ----------------


win = Tk()
win.title("Employee Management System")
# win.config(bg="lightblue")
image = Image.open(r"C:\Users\bobad\Data Science\Evening\7 MENTOR\bg.png")
image = image.resize((1920, 1080), Image.Resampling.LANCZOS)
bg_image = ImageTk.PhotoImage(image)
bg_label = Label(win, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ---------------- This Is Made By Aditya Bobade ----------------  #

# Main // Heading Label
l0 = Label(
    win,
    text="EMPLOYEE MANAGEMENT SYSTEM",
    bg="white",
    fg="black",
    width=40,
    bd=5,
    relief="sunken",  # We Also Can Use This Designs Also >>> "flat","groove","raised","ridge","solid","sunken"
    font=("times new roman", 18, "bold")
)
# Place Main // Heading Label (top-middle)
l0.pack(anchor="center", pady=40)

# emp_id >> Lable

l1 = Label(
    win,
    text="EMPLOYEE ID",
    bg="white",
    fg="black",
    width=20,
    bd=7,
    relief="ridge",
    font=("times new roman", 12, "bold")
)
l1.place(x=100, y=102)

# emp_id >>> entry

id1 = StringVar()
e1 = Entry(
    win,
    textvariable=id1,
    bg="white",
    width=40,
    bd=5,
    relief="flat",
    font=("times new roman", 12, "bold")
)
e1.place(x=330, y=105)
e1.configure(justify="center")


# emp_name >> Lable

l2 = Label(
    win,
    text="EMPLOYEE NAME",
    bg="white",
    fg="black",
    width=20,
    bd=7,
    relief="ridge",
    font=("times new roman", 12, "bold")
)
l2.place(x=100, y=152)

# emp_name >>> entry

id2 = StringVar()
e2 = Entry(
    win,
    textvariable=id2,
    bg="white",
    width=40,
    bd=5,
    relief="flat",
    font=("times new roman", 12, "bold")
)
e2.place(x=330, y=155)
e2.configure(justify="center")


# mob_no >> Lable

l3 = Label(
    win,
    text="MOBILE NUMBER",
    bg="white",
    fg="black",
    width=20,
    bd=7,
    relief="ridge",
    font=("times new roman", 12, "bold")
)
l3.place(x=100, y=202)

# mob_no >>> entry
id3 = StringVar()
e3 = Entry(
    win,
    textvariable=id3,
    bg="white",
    width=40,
    bd=5,
    relief="flat",
    font=("times new roman", 12, "bold")
)
e3.place(x=330, y=200)
e3.configure(justify="center")

# Department >> Label

l4 = Label(
    win,
    text="DEPARTMENT",
    bg="white",
    fg="black",
    width=20,
    bd=7,
    relief="ridge",
    font=("times new roman", 12, "bold")
)
l4.place(x=100, y=253)

# Department >> Combobox / Entry

id4 = StringVar()
e4 = ttk.Combobox(
    win,
    textvariable=id4,
    width=39,
    font=("times new roman", 12, "bold"),
    values=["Finance", "Marketing", "Production", "HR", "IT", "Sales"],
    state="readonly",

)
e4.place(x=330, y=250, height=35)
e4.current(0)
e4.configure(justify="center")

# Salary >>> label

l5 = Label(
    win,
    text="SALARY",
    bg="white",
    fg="black",
    width=20,
    bd=7,
    relief="ridge",
    font=("times new roman", 12, "bold")
)
l5.place(x=100, y=300)

# salary >>> entry

id5 = StringVar()
e5 = Entry(
    win,
    textvariable=id5,
    bg="white",
    width=40,
    bd=5,
    relief="flat",
    font=("times new roman", 12, "bold")
)
e5.place(x=330, y=300)
e5.configure(justify="center")


# Create Buttons  >>> SHOW,EXIT,ADD,SALARY

# Button >>> SHOW

b1 = Button(
    win,
    text="SHOW",
    command=show_data,
    relief="ridge",
    bd=4,
    bg="gray",
    fg="white",
    font=("times new roman", 12, "bold"),
    width=15,
)
b1.place(x=190, y=370)


# Button >>> EXIT

b2 = Button(
    win,
    text="EXIT PROGRAM",
    command=exit_program,
    relief="ridge",
    bg="gray",
    fg="white",
    bd=4,
    font=("times new roman", 12, "bold"),
    width=15,
)
b2.place(x=190, y=420)


# Button >>> ADD

b3 = Button(
    win,
    text="ADD",
    command=add_data,
    relief="ridge",
    bg="gray",
    fg="white",
    bd=4,
    font=("times new roman", 12, "bold"),
    width=15,
)
b3.place(x=400, y=370)


# Button >>> SALARY

b4 = Button(
    win,
    text="SALARY",
    command=show_salary,
    relief="ridge",
    bg="gray",
    fg="white",
    bd=4,
    font=("times new roman", 12, "bold"),
    width=15,
)
b4.place(x=400, y=420)


# Label >>> Enter ID for Deletion

l6 = Label(
    win,
    text="ENTER ID TO DELETE",
    bg="white",
    fg="black",
    width=20,
    bd=7,
    relief="ridge",
    font=("times new roman", 12, "bold")
)
l6.place(x=100, y=485)


# Entry >>> for ID Deletion

id6 = StringVar()
e6 = Entry(
    win,
    textvariable=id6,
    bg="white",
    width=40,
    bd=5,
    relief="flat",
    font=("times new roman", 12, "bold")
)
e6.place(x=330, y=490)
e6.configure(justify="center")


# Button >> DELETE EMP

b5 = Button(
    win,
    text="DELETE",
    command=delete_data,
    relief="ridge",
    bg="#FF7F7F",
    fg="black",
    bd=4,
    font=("times new roman", 12, "bold"),
    width=15,
)
b5.place(x=300, y=555)


# Label >>> Update EMP INFO

l7 = Label(
    win,
    text="UPDATE EMP INFO",
    bg="white",
    fg="black",
    width=20,
    bd=7,
    relief="ridge",
    font=("times new roman", 12, "bold")
)
l7.place(x=100, y=620)


# Entry >>> Update EMP INFO

id7 = StringVar()
e7 = Entry(
    win,
    textvariable=id7,
    bg="white",
    width=40,
    bd=5,
    relief="flat",
    font=("times new roman", 12, "bold")
)
e7.place(x=330, y=625)
e7.configure(justify="center")


# Button >> SELECT EMP

b6 = Button(
    win,
    text="SELECT",
    command=select_emp,
    relief="ridge",
    bg="gray",
    fg="white",
    bd=4,
    font=("times new roman", 12, "bold"),
    width=15,
)
b6.place(x=190, y=695)


# Button >> UPDATE EMP

b7 = Button(
    win,
    text="UPDATE",
    command=update_data,
    relief="ridge",
    bg="gray",
    fg="white",
    bd=4,
    font=("times new roman", 12, "bold"),
    width=15,
)
b7.place(x=400, y=695)


# ---------------- View Data >>> Treeview Box ---------------- #


style = ttk.Style()
style.configure("mystyle.Treeview",
                borderwidth=5,
                relief="groove",
                font=('Calibri', 12),
                rowheight=27)

style.configure("mystyle.Treeview.Heading",
                font=('Calibri', 12, 'bold'),
                foreground="black",
                background="gray")


view = ttk.Treeview(win, style="mystyle.Treeview")
view.place(x=750, y=100, height=400, width=700)

# Define Columns
view["columns"] = ("1", "2", "3", "4", "5")
view["show"] = "headings"

# Set Column Widths and Alignment
view.column("1", width=90, anchor=CENTER)
view.column("2", width=150, anchor=CENTER)
view.column("3", width=120, anchor=CENTER)
view.column("4", width=120, anchor=CENTER)
view.column("5", width=100, anchor=CENTER)

# Set Column Headings
view.heading("1", text="EMP ID")
view.heading("2", text="NAME")
view.heading("3", text="MOBILE NO.")
view.heading("4", text="DEPARTMENT")
view.heading("5", text="SALARY")


def block_event(event):
    if view.identify_region(event.x, event.y) in ("separator", "heading"):
        return "break"


view.bind("<Button-1>", block_event)

# Alternate Row Colors
view.tag_configure("evenrow", background="#FAFAFA")  # very light grey
view.tag_configure("oddrow", background="#E0E0E0")   # medium grey
view.configure(selectmode="browse")  # single row selection


# CLEAR BUTTON >>> To Clear All Records

b8 = Button(
    win,
    text="CLEAR",
    command=clear_data,
    relief="ridge",
    bg="gray",
    fg="white",
    bd=4,
    font=("times new roman", 12, "bold"),
    width=15,
)
b8.place(x=1030, y=550)

win.state('zoomed')
bg_label.lower()
win.mainloop()


# ---------------- This Is Made By Aditya Bobade ----------------  #


# Task >>> Upload project on Git-Hub
# 1. Create a new repository on GitHub
# 2. Initialize git in your project directory
# 3. Add your files to the staging area
# 4. Commit your changes
# 5. Link your local repository to the GitHub repository
# 6. Push your changes to GitHub


# Task2 >>> Insert an Image in EMS UI background
