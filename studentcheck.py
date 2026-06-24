import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

# -------- Database Connection --------
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="studentdb"
)
cur = con.cursor()

# Create users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50)
)
""")

# Create students table (without parent_name)
cur.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    course VARCHAR(50),
    age INT,
    contact VARCHAR(15),
    email VARCHAR(100),
    dob VARCHAR(20),
    gender VARCHAR(10),
    tenth_mark FLOAT,
    twelfth_mark FLOAT,
    attendance FLOAT
)
""")
con.commit()

# Insert default admin
cur.execute("SELECT * FROM users WHERE username='admin'")
if not cur.fetchone():
    cur.execute("INSERT INTO users(username,password) VALUES(%s,%s)", ("admin", "admin123"))
    con.commit()

# -------- Main Window --------
root = Tk()
root.title("Login System with Student Details")
root.geometry("950x650")

# Frames
login_frame = Frame(root, width=950, height=650)
register_frame = Frame(root, width=950, height=650)
student_frame = Frame(root, width=950, height=650)
admin_frame = Frame(root, width=950, height=650)

for f in (login_frame, register_frame, student_frame, admin_frame):
    f.place(x=0, y=0)

def show_frame(frame):
    frame.tkraise()

# -------- Add Background Images --------
# Replace these image files with your own images
login_img = Image.open(r"D:\Zcoding\login_bg.jpg").resize((950,650))
login_bg = ImageTk.PhotoImage(login_img)
Label(login_frame, image=login_bg).place(x=0,y=0)

register_img = Image.open(r"D:\Zcoding\register_bg.jpg").resize((950,650))
register_bg = ImageTk.PhotoImage(register_img)
Label(register_frame, image=register_bg).place(x=0,y=0)

student_img = Image.open(r"D:\Zcoding\student_bg.jpg").resize((950,650))
student_bg = ImageTk.PhotoImage(student_img)
Label(student_frame, image=student_bg).place(x=0,y=0)

admin_img = Image.open(r"D:\Zcoding\admin_bg.jpg").resize((950,650))
admin_bg = ImageTk.PhotoImage(admin_img)
Label(admin_frame, image=admin_bg).place(x=0,y=0)

# -------- Functions --------
def login_user():
    u = user_entry.get()
    p = pass_entry.get()
    cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (u, p))
    result = cur.fetchone()
    if result:
        if u == "admin":
            show_frame(admin_frame)
            load_students_admin()
        else:
            show_frame(student_frame)
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

def register_user():
    u = reg_user.get()
    p = reg_pass.get()
    try:
        cur.execute("INSERT INTO users(username,password) VALUES(%s,%s)", (u,p))
        con.commit()
        messagebox.showinfo("Success", "Registered Successfully")
        show_frame(login_frame)
    except:
        messagebox.showerror("Error", "User already exists")

def save_student():
    data = (
        stu_name.get(), stu_course.get(), stu_age.get(), stu_contact.get(),
        stu_email.get(), stu_dob.get(), stu_gender.get(), stu_10th.get(),
        stu_12th.get(), stu_attendance.get()
    )
    if all(data):
        cur.execute("""INSERT INTO students
            (name, course, age, contact, email, dob, gender, tenth_mark, twelfth_mark, attendance)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", data)
        con.commit()
        messagebox.showinfo("Success","Student Saved")
    else:
        messagebox.showwarning("Warning","Fill all fields")

def view_students():
    view_win = Toplevel(root)
    view_win.title("All Student Details")
    view_win.geometry("700x500")
    view_win.configure(bg="pink")

    Label(view_win, text="Student Records", font=("Arial",16,"bold"), bg="pink").pack(pady=10)

    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()

    text_area = Text(view_win, width=90, height=25, bg="white")
    text_area.pack(padx=10, pady=10)

    if rows:
        for r in rows:
            text_area.insert(END, f"ID:{r[0]} | Name:{r[1]} | Course:{r[2]} | Age:{r[3]} | Contact:{r[4]} "
                                   f"| Email:{r[5]} | DOB:{r[6]} | Gender:{r[7]} | 10th:{r[8]} | 12th:{r[9]} "
                                   f"| Attendance:{r[10]}%\n\n")
    else:
        text_area.insert(END, "No student records found!")

def load_students_admin():
    for widget in admin_list_frame.winfo_children():
        widget.destroy()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    y = 10
    if rows:
        for r in rows:
            Label(admin_list_frame, text=f"ID:{r[0]} | Name:{r[1]} | Course:{r[2]} | Age:{r[3]} | Contact:{r[4]}",
                  bg="pink").place(x=10,y=y)
            y+=25
    else:
        Label(admin_list_frame, text="No Students Found!", bg="pink").place(x=10,y=y)

def edit_student():
    sid = edit_id.get()
    if not sid:
        messagebox.showwarning("Warning","Enter Student ID")
        return
    
    cur.execute("SELECT * FROM students WHERE id=%s", (sid,))
    student = cur.fetchone()
    if not student:
        messagebox.showerror("Error","Student not found")
        return

    updated_data = (
        edit_name.get() if edit_name.get() else student[1],
        edit_course.get() if edit_course.get() else student[2],
        edit_age.get() if edit_age.get() else student[3],
        edit_contact.get() if edit_contact.get() else student[4],
        edit_email.get() if edit_email.get() else student[5],
        edit_dob.get() if edit_dob.get() else student[6],
        edit_gender.get() if edit_gender.get() else student[7],
        edit_10th.get() if edit_10th.get() else student[8],
        edit_12th.get() if edit_12th.get() else student[9],
        edit_attendance.get() if edit_attendance.get() else student[10],
        sid
    )

    cur.execute("""UPDATE students SET
        name=%s, course=%s, age=%s, contact=%s, email=%s, dob=%s, gender=%s,
        tenth_mark=%s, twelfth_mark=%s, attendance=%s WHERE id=%s""", updated_data)
    con.commit()
    messagebox.showinfo("Updated","Student Updated Successfully")
    load_students_admin()

# -------- Login Frame --------
Label(login_frame, text="Login Page", font=("Arial",18,"bold"), bg="pink").place(x=400,y=30)
Label(login_frame, text="Username:", bg="pink").place(x=320,y=120)
user_entry = Entry(login_frame, width=25)
user_entry.place(x=440,y=120)
Label(login_frame, text="Password:", bg="pink").place(x=320,y=170)
pass_entry = Entry(login_frame, width=25, show="*")
pass_entry.place(x=440,y=170)
Button(login_frame, text="Login", command=login_user, bg="lightblue").place(x=370,y=220)
Button(login_frame, text="Register", command=lambda:show_frame(register_frame), bg="orange").place(x=470,y=220)

# -------- Register Frame --------
Label(register_frame, text="Register Page", font=("Arial",18,"bold"), bg="pink").place(x=400,y=30)
Label(register_frame, text="New Username:", bg="pink").place(x=320,y=120)
reg_user = Entry(register_frame, width=25)
reg_user.place(x=460,y=120)
Label(register_frame, text="New Password:", bg="pink").place(x=320,y=170)
reg_pass = Entry(register_frame, width=25, show="*")
reg_pass.place(x=460,y=170)
Button(register_frame, text="Register", command=register_user, bg="green").place(x=380,y=220)
Button(register_frame, text="Back", command=lambda:show_frame(login_frame), bg="red").place(x=480,y=220)

# -------- Student Frame --------
Label(student_frame, text="Student Details", font=("Arial",18,"bold"), bg="pink").place(x=370,y=20)

labels = ["Name","Course","Age","Contact No","Email","DOB","Gender","10th Mark","12th Mark","Attendance %"]
entries = []
y = 80
for i, text in enumerate(labels):
    Label(student_frame, text=f"{text}:", bg="pink").place(x=200,y=y)
    e = Entry(student_frame, width=25)
    e.place(x=350,y=y)
    entries.append(e)
    y+=40

(stu_name, stu_course, stu_age, stu_contact, stu_email,
 stu_dob, stu_gender, stu_10th, stu_12th, stu_attendance) = entries

Button(student_frame, text="Save", command=save_student, bg="purple", fg="white").place(x=200,y=550)
Button(student_frame, text="View", command=view_students, bg="brown", fg="white").place(x=300,y=550)
Button(student_frame, text="Logout", command=lambda:show_frame(login_frame), bg="red").place(x=400,y=550)

# -------- Admin Frame --------
Label(admin_frame, text="Admin Panel", font=("Arial",18,"bold"), bg="pink").place(x=380,y=20)

admin_list_frame = Frame(admin_frame, bg="pink", width=850, height=200)
admin_list_frame.place(x=50,y=60)

Label(admin_frame, text="Edit Student by ID:", bg="pink").place(x=200,y=280)
edit_id = Entry(admin_frame, width=5); edit_id.place(x=350,y=280)

fields = ["Name","Course","Age","Contact","Email","DOB","Gender","10th","12th","Attendance"]
edit_entries=[]
y=310
for f in fields:
    Label(admin_frame, text=f"{f}:", bg="pink").place(x=200,y=y)
    e = Entry(admin_frame, width=20); e.place(x=300,y=y)
    edit_entries.append(e)
    y+=30

(edit_name, edit_course, edit_age, edit_contact, edit_email,
 edit_dob, edit_gender, edit_10th, edit_12th, edit_attendance) = edit_entries

Button(admin_frame, text="Update", command=edit_student, bg="blue", fg="white").place(x=400,y=620)
Button(admin_frame, text="Logout", command=lambda:show_frame(login_frame), bg="red").place(x=500,y=620)

# -------- Show Login First --------
show_frame(login_frame)
root.mainloop()

