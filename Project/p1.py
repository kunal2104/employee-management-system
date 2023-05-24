from sqlite3 import *
from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import requests
import bs4
import pandas as pd
import matplotlib.pyplot as plt


# TO OPEN THE ADD WINDOW AND WITHDRAW(CLOSE) THE MAIN WINDOW

def f1():
	add_window.deiconify()
	main_window.withdraw()

# TO GO BACK FROM ADD WINDOW TO MAIN WINDOW

def f2():
	main_window.deiconify()
	add_window.withdraw()

# TO OPEN VIEW WINDOW AND WITHDRAW THE MAIN WINDOW
 
def f3():
	view_window.deiconify()
	main_window.withdraw()
	vw_st_data.delete(1.0,END)

	info = ""
	con = None
	try:
		con = connect("ems.db")
		cursor = con.cursor()
		sql = "select * from employee"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = info + "ID: " + str(d[0]) + " | Name: " + str(d[1]) + " | Salary: " + str(d[2]) + "\n"
		vw_st_data.insert(INSERT, info)
	except Exception as e:
		showerror("Issue Can't see the data", e)
	finally:
		if con is not None:
			con.close()

# TO GO BACK TO MAIN WINDOW FROM THE VIEW WINDOW

def f4():
	main_window.deiconify()
	view_window.withdraw()

# TO OPEN UPDATE WINDOW AND WITHDRAW FROM MAIN WINDOW

def f5():
	update_window.deiconify()
	main_window.withdraw()

# TO GO BACK TO MAIN WINDOW FROM UPDATE WINDOW

def f6():
	main_window.deiconify()
	update_window.withdraw()

# TO OPEN DELETE WINDOW AND WITHDRAW THE MAIN WINDOW

def f7():
	delete_window.deiconify()
	main_window.withdraw()

# TO GO BACK TO MAIN WINDOW FROM THE DELETE WINDOW

def f8():
	main_window.deiconify()
	delete_window.withdraw()

# T0 ENTER DATA IN DATABASE
def f9():
	con = None
	try:
		con = connect("ems.db")
		cursor = con.cursor()
		sql="insert into employee values ('%d','%s','%f')"
		if len(aw_ent_id.get()) != 0:
			id = int(aw_ent_id.get())
			if id == int(aw_ent_id.get()):
				if id > 0:
					if len(aw_ent_name.get()) != 0:
						name=aw_ent_name.get()
						if name.isalpha():
							if len(name) >= 2:

								try:
									if len(aw_ent_salary.get()):
										salary=float(aw_ent_salary.get())
										if salary > 0:
											if salary >= 8000:
												cursor.execute(sql %(id, name, salary))
												con.commit()
												showinfo("SUCCESS", "Record Is Added")
												aw_ent_id.delete(0,END)
												aw_ent_name.delete(0,END)
												aw_ent_salary.delete(0,END)
												aw_ent_id.focus()
											else:
												showerror("Salary Error","Salary should be Minimum 8000")
										else:
											showerror("Salary Error","Salary should be a Positive Number")
									else:
										showerror("Salary Error", "Salary should not be empty")
								except ValueError:
									showerror("Salary Error","Salary Should be number only Not Letter")
									con.rollback()

								finally:
									if con is not None:
										con.close
							else:
								showerror("Name Error", "Minimum Two Charcter are required for Name")
						else:
							showerror("Name Error", "Name Should Required Letter Only")
					else:
						showerror("Name Error", "Name Should Not be Empty")
				else:
					showerror("ID Error", "Enter Valid ID ")
			else:
				showerror("ID Error", "ID should not be empty")
		else:
			showerror("error", "All Fields Are Required")

	except ValueError:
		showerror("ID Error", "Check ID Should be Number Only")
		con.rollback()
	except IntegrityError:
		showerror("ID Error", "id alredy exists")
		con.rollback()
	except Exception as e:
		showerror("Insertion Issue", e)
		con.rollback()
	finally:
		if con is not None:
			con.close()

# TO UPDATE THE DATA
def f10():
	con = None
	try:
		con = connect("ems.db")
		cursor = con.cursor()
		sql="update employee set name = '%s', salary = '%f' where id = '%d' "
		if len(uw_ent_id.get()) != 0:
			id = int(uw_ent_id.get())
			if id > 0:
				if len(uw_ent_name.get()) != 0:
					name=uw_ent_name.get()
					if name.isalpha():
						if len(name) >= 2:

							try:
								if len(uw_ent_salary.get()):
									salary=float(uw_ent_salary.get())
									if salary > 0:
										if salary >= 8000:
											cursor.execute(sql %(name, salary, id))
											if cursor.rowcount == 1:
												con.commit()
												showinfo("SUCCESS", "Record Is Updated")
											else:
												showerror("Failure", "Record Does Not Exists ")

											uw_ent_id.delete(0,END)
											uw_ent_name.delete(0,END)
											uw_ent_salary.delete(0,END)
											uw_ent_id.focus()
										else:
											showerror("Salary Error","Salary shud be Minimum 8000")
									else:
										showerror("Salary Error","Salary shud be a Positive Number")
								else:
									showerror("Salary Error", "Salary shud not be empty")
							except ValueError:
								showerror("Salary Error","Salary Shud be number only Not Letter")
								con.rollback()

							finally:
								if con is not None:
									con.close
						else:
							showerror("Name Error", "Minimum Two Char are required for Name")
					else:
						showerror("Name Error", "Name Shud Required Letter Only")
				else:
					showerror("Name Error", "Name Shud Not be Empty")
			else:
				showerror("ID Error", "Enter Valid ID ")
		else:
			showerror("Error", "All Fields Are Required")

	except ValueError:
		showerror("ID Error", "Check ID Shud be Number Only")
		con.rollback()
	except Exception as e:
		showerror("ID error","Employee Id already exists",e)
		con.rollback()
	finally:
		if con is not None:
			con.close()


# TO DELETE THE DATA
def f11():
	con = None
	try:
		con = connect("ems.db")
		cursor = con.cursor()
		sql = "delete from employee where id = '%d'"
		if len(dw_ent_id.get()) != 0:
			id = int(dw_ent_id.get())
			cursor.execute(sql % id)
			if id < 0:
				if cursor.rowcount == 1:
					con.commit()
					showinfo("Success", " Record Deleted ")
					dw_ent_id.delete(0,END)
				else:
					showerror("Failure", "Id Should Be Positive Integer only")
			else:
				showerror("Failure", "Record does not exists")
		else:
			showerror("ID Error", "ID should not be empty")
	except ValueError:
		showerror("IDError","Record does not exists")
		con.rollback()
	except Exception as e:
		showerror("ISSUE", e)
		con.rollback()
	finally:
		if con is not None:
			con.close()

# TO PLOT THE GRAPH
def f12():
	con = None
	try:
		con = connect("ems.db")
		cursor = con.cursor()
		data = pd.read_sql_query("select name, salary from employee",con)
		employee = data['name'].tolist()
		salary = data['salary'].tolist()

		res = {}
		for key in employee:
			for value in salary:
				res[key] = value
				salary.remove(value)
				break
		sort_order = sorted(res.items(), key=lambda x:x[1], reverse=True)
		max = sort_order[0:5]

		a,b = [],[]
		for i in max:
			a.append(i[0])
			b.append(i[1])

		employeee = a
		salaryy = b

		plt.bar(employeee,salaryy, width = 0.5, color=["red","green","yellow","blue","orange"])
		plt.xlabel("Employee")
		plt.ylabel("Salary")
		plt.grid()
		plt.title("Top Five Highest Earning Salary Employee")

		plt.show()
	except Exception as e:
		showerror("issue", e)
	finally:
		if con is not None:
			con.close()


# MAIN WINDOW 

main_window = Tk()
main_window.title("E.M.S")
main_window.geometry("500x500+100+100")
main_window.configure(bg='light green')
main_window.iconbitmap("profile.ico")

f = ("Arial", 20, "bold")
y = 5
q = ("Arial", 12, "bold", "italic")
quote = []

# code for quote

try:
	wa = "https://www.beaninspirer.com/quote-of-the-day/"
	res = requests.get(wa)
	data = bs4.BeautifulSoup(res.text, "html.parser")
	quote = data.find("blockquote").text
	for item in quote:
		title = item.find("span")		
		
except Exception as e:
	print("Issue", e)

mw_btn_add = Button(main_window, text="Add", font=f, width= 7,bd="7", command=f1)
mw_btn_view = Button(main_window, text="View", font=f, width= 7,bd="7", command=f3)
mw_btn_update = Button(main_window, text="Update", font=f, width= 7,bd="7", command=f5)
mw_btn_delete = Button(main_window, text="Delete", font=f, width= 7,bd="7", command=f7)
mw_btn_chart = Button(main_window, text="Chart", font=f, width= 7,bd="7", command= f12)
mw_text_quote = Message(main_window, text=("QOTD:",quote),bg='light green',width = "450", font=q,borderwidth=2,relief='solid')

mw_btn_add.pack(pady=y)
mw_btn_view.pack(pady=y)
mw_btn_update.pack(pady=y)
mw_btn_delete.pack(pady=y)
mw_btn_chart.pack(pady=y)
mw_text_quote.pack(pady=y)


# ADD WINDOW

add_window = Toplevel(main_window)
add_window.title("Add Emp")
add_window.geometry("500x500+100+100")
add_window.configure(bg='light blue')
add_window.iconbitmap("profile.ico")

aw_lab_id = Label(add_window, text="enter id:", font=f)
aw_ent_id = Entry(add_window, font=f, bd=4)
aw_lab_name = Label(add_window, text="enter name:", font=f)
aw_ent_name = Entry(add_window, font=f, bd=4)
aw_lab_salary = Label(add_window, text="enter salary:", font=f)
aw_ent_salary = Entry(add_window, font=f, bd=4)
aw_btn_save = Button(add_window, text="Save", font=f, bd="7",command=f9)
aw_btn_back = Button(add_window, text="Back", font=f, command=f2, bd="7")

aw_lab_id.pack(pady=y)
aw_ent_id.pack(pady=y)
aw_lab_name.pack(pady=y)
aw_ent_name.pack(pady=y)
aw_lab_salary.pack(pady=y)
aw_ent_salary.pack(pady=y)
aw_btn_save.pack(pady=y)
aw_btn_back.pack(pady=y)

add_window.withdraw()


# VIEW WINDOW

view_window = Toplevel(main_window)
view_window.title("View Emp")
view_window.geometry("500x500+100+100")
view_window.configure(bg='khaki')
view_window.iconbitmap("profile.ico")

vw_st_data = ScrolledText(view_window, width=30, height=10, font=f)
vw_btn_back = Button(view_window, text="Back", font=f,command=f4, bd="7")
vw_st_data.pack(pady=y)
vw_btn_back.pack(pady=y)

view_window.withdraw()


# UPDATE WINDOW

update_window = Toplevel(main_window)
update_window.title("Update Emp")
update_window.geometry("500x500+100+100")
update_window.configure(bg='light pink')
update_window.iconbitmap("profile.ico")

uw_lab_id = Label(update_window, text="enter id:", font=f)
uw_ent_id = Entry(update_window, font=f, bd=4)
uw_lab_name = Label(update_window, text="enter name:", font=f)
uw_ent_name = Entry(update_window, font=f, bd=4)
uw_lab_salary = Label(update_window, text="enter salary:", font=f)
uw_ent_salary = Entry(update_window, font=f, bd=4)
uw_btn_save = Button(update_window, text="Save", font=f, bd="7", command = f10)
uw_btn_back = Button(update_window, text="Back", font=f,bd="7", command=f6)

uw_lab_id.pack(pady=y)
uw_ent_id.pack(pady=y)
uw_lab_name.pack(pady=y)
uw_ent_name.pack(pady=y)
uw_lab_salary.pack(pady=y)
uw_ent_salary.pack(pady=y)
uw_btn_save.pack(pady=y)
uw_btn_back.pack(pady=y)

update_window.withdraw()


# DELETE WINDOW

delete_window = Toplevel(main_window)
delete_window.title("Delete Emp")
delete_window.geometry("500x500+100+100")
delete_window.configure(bg='mediumpurple')
delete_window.iconbitmap("profile.ico")


dw_lab_id = Label(delete_window, text="enter id:", font=f)
dw_ent_id = Entry(delete_window, font=f, bd=4)
dw_btn_delete = Button(delete_window, text="Delete",width=7, font=f, bd="7", command = f11)
dw_btn_back = Button(delete_window, text="Back",width=7, font=f,bd="7", command=f8)

dw_lab_id.pack(pady=y)
dw_ent_id.pack(pady=y)
dw_btn_delete.pack(pady=y)
dw_btn_back.pack(pady=y)

delete_window.withdraw()

main_window.mainloop()