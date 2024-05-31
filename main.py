from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
import mysql.connector

mydb = mysql.connector.connect(
            host="XXXXX",
            user="XXXXX",
            password="XXXXX",
            database="XXXXX"
)    


top = Tk()
top.geometry("1020x580")

style = ttk.Style()
style.theme_use('alt')

list_data = []

def tabify(text, lenght=20):
    text_char_len = lenght - len(text)
    s = text.ljust((len(text)) + text_char_len)
    return s 

class Filter:
    option = ("Show all","Source IP","Dest IP","Source Port","Dest Port")
    var = ""
    category = "Show all"
    selected = ""
    status = ""

class List_item():
    def __init__(self, id, src_ip, dst_ip, s_port, d_port, proto, raw, status, datetime):
        self.id = id
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.s_port = s_port
        self.d_port = d_port
        self.raw = raw
        self.status = status
        self.datetime = datetime

def change():
    list_box.delete(0,END)
    list_data.clear()
    update()

def show_packet(event):
    if len(list_box.curselection()) > 0: 
        try:
            id_no = list_box.curselection()
            for item in list_data:
                if str(id_no[0]) == item.id:
                    raw_txt = "asd"
                    vars = [item.id]
                    mycursor = mydb.cursor()
                    mycursor.execute("SELECT packet FROM logs WHERE id=%s",vars)
                    rows = mycursor.fetchall()
                    for row in rows:
                        raw_txt = row[0]
                    Filter.selected = item.id
                    Filter.status = item.status
                    text_area.delete("1.0", END)
                    text_area.insert(INSERT, raw_txt)
        except:
            text_area.delete("1.0", END)
            text_area.insert(INSERT, "")

def change_filter(*arg):
    Filter.category = select_filter.get()

def flag():
    flaged = ""
    
    if (Filter.status == "fine"):
        flaged = "flaged"
    else:
        flaged = "fine"

    mycursor = mydb.cursor()
    vars = [flaged, Filter.selected]
    mycursor.execute("UPDATE logs SET status=%s WHERE id=%s",vars)
    mydb.commit()
    mycursor.close()
    change()

def update():

    try:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT id, src_ip, dst_ip, s_port, d_port, proto, status, time FROM logs")
        rows = mycursor.fetchall()
        for row in rows:
            
            Filter.var = input_field.get() 

            add_to_list = False
            
            if Filter.category == Filter.option[0]:
                add_to_list = True  

            for i in range(4):          
                if Filter.category == Filter.option[i + 1] and row[i + 1] == Filter.var:
                    add_to_list = True


            if add_to_list == True:
                list_data.append( List_item( str(row[0]) , str(row[1]), 
                    str(row[2]), str(row[3]), str(row[4]), str(row[5]), 
                    "", str(row[6]), str(row[7]) ) )
        mycursor.close()
    except:
        print("err2")            
    list_box.insert("end",
            tabify("ID",6) + 
            tabify("Time",26) + 
            tabify("Source IP") + 
            tabify("Destination IP") + 
            tabify("Source Port",14) + 
            tabify("Dest Port",14) +
            tabify("Status",10)
            )

    for item in list_data:
        
        list_box.insert(item.id, 
            tabify(item.id,6) + 
            tabify(item.datetime,26) + 
            tabify(item.src_ip) + 
            tabify(item.dst_ip) + 
            tabify(item.s_port,14) + 
            tabify(item.d_port,14) + 
            tabify(item.status,10)
            )

select_filter = StringVar()

label = Label(top, text="Filter by:")
input_field = Entry(top)
btn = Button(top, text ="ok", command=change, width=10)
btn_refresh = Button(top, text ="refresh", command=change, width=10)
btn_flag = Button(top, text ="Flag", command=flag, width=10)

list_box = Listbox(top,width=110)
scrollbar = Scrollbar(top, orient= "vertical")
combo_box = ttk.Combobox(top, textvariable=select_filter) 
combo_box["values"] = Filter.option 

label.config(font=("Consolas", 12))
input_field.config(font=("Consolas", 12))
btn.config(font=("Consolas", 12))
btn_refresh.config(font=("Consolas", 12))
btn_flag.config(font=("Consolas", 12))

list_box.config(font=("Consolas", 12))
combo_box.config(font=("Consolas", 12))

label.grid(row=0, column=0, pady=2)
combo_box.grid(row=0, column=1, pady=2)
input_field.grid(row=0, column=2, pady=2)
btn.grid(row=0, column=3, pady=2)
btn_refresh.grid(row=0, column=4, pady=2)
btn_flag.grid(row=0, column=5, pady=2)

list_box.grid(row=1, column=0, columnspan=6, pady=2, padx=5)
scrollbar.grid(row = 1, column = 6, sticky=N+S)

list_box.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=list_box.yview)
list_box.bind("<<ListboxSelect>>", show_packet)

select_filter.trace('w', change_filter)

text_area = scrolledtext.ScrolledText(top, wrap=WORD,  
                                      width=110, height=15,  
                                      font = ("Consolas", 12)) 
  
text_area.grid(row=2, column=0, columnspan=7, pady=2, padx=5) 

update()

top.mainloop()
