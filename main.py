from tkinter.scrolledtext import ScrolledText
#from utils.database import *
from tkinter import *
from tkinter import ttk
from utils.database import *


window = Tk()
window.title('Text Sender')
window.geometry("1000x500")
window.resizable(width=0, height=0)
selected_item0 = ''

# Here are the three lines by which we set the theme ###
# Create a style
style = ttk.Style(window)

# Import the tcl file
window.tk.call('source', 'azure.tcl')

# Set the theme with the theme_use method
style.theme_use('azure')


def delete_all_members():
    delete_all()
    update_table('text')


def save_record():
    save(entry_name.get().title(), str(entry_phone.get()), combo2.get())
    reset_fields([entry_name, entry_phone])
    entry_name.focus()
    combo2.set('Member')
    update_table('text')


def delete_member():
    global selected_item0
    global lbl_sendto
    print(selected_item0[1])
    if delete(selected_item0[0]):
        lbl_status.config(text=f'{selected_item0[1]} deleted successfully')
        update_table('text')
        btn_delete.config(text='Delete')


# ----- Notebook -----
notebook = ttk.Notebook(window)
notebook.place(x=20, y=20, height=460, width=380)

frame1 = Frame(notebook, height=460, width=560)
frame1.place(x=420, y=20)

frame2 = Frame(notebook, height=460, width=560)
frame2.place(x=420, y=20)

frame3 = Frame(notebook, height=460, width=560)
frame3.place(x=420, y=20)

frame4 = Frame(notebook, height=460, width=560)
frame4.place(x=420, y=20)

notebook.add(frame1, text='Send Message')
notebook.add(frame2, text='Add Members')
notebook.add(frame4, text='Delete Members')
notebook.add(frame3, text='Settings')


# ----- Widgets in Send Message -----
lbl_sendto = ttk.Label(frame1, text='Send to : ')
lbl_sendto.place(x=50, y=20)

groups = ('Everyone', 'Members only', 'Leaders only', 'Select Individuals')
selected_group1 = StringVar()

combo1 = ttk.Combobox(frame1, textvariable=selected_group1)
combo1['values'] = groups
combo1['state'] = 'readonly'
combo1.set('Everyone')
combo1.place(x=140, y=21, width=200)

lbl_text = Label(frame1, text='Message :')
lbl_text.place(x=50, y=55)

text = ScrolledText(frame1, width=36, height=10)
text.place(x=50, y=80)

btn_send_msg = ttk.Button(frame1, text='Send', width=13)
btn_send_msg.place(x=256, y=255)

# Widgets in Add Members
lbl_name = Label(frame2, text='Name : ')
lbl_name.place(x=50, y=20)
entry_name = ttk.Entry(frame2)
entry_name.place(x=140, y=21, width=200)

lbl_phone = Label(frame2, text='Phone : ')
lbl_phone.place(x=50, y=60)
entry_phone = ttk.Entry(frame2)
entry_phone.place(x=140, y=62, width=200)

lbl_phone = Label(frame2, text='Level : ')
lbl_phone.place(x=50, y=100)

selected_group2 = StringVar()

groups_level = ('Member', 'Leader')
combo2 = ttk.Combobox(frame2, textvariable=selected_group2)
combo2['values'] = groups_level
combo2['state'] = 'readonly'
combo2.set('Member')
combo2.place(x=140, y=100, width=200)

btn_save = ttk.Button(frame2, text='Save', style='AccentButton', width=32, command=save_record)
btn_save.place(x=139, y=140)


# Widgets in delete members
lbl_status = ttk.Label(frame4, text='...')
lbl_status.place(x=50, y=20)

lbl_sendto = ttk.Label(frame4, text='1.  Select member to from table to delete. \n2.  Click the button to delete ')
lbl_sendto.place(x=50, y=60)

btn_delete = ttk.Button(frame4, text='Delete', style='AccentButton', width=32, command=delete_member)
btn_delete.place(x=50, y=100)

btn_delete_all = ttk.Button(frame4, text='Delete all ', width=32, command=delete_all_members)
btn_delete_all.place(x=50, y=300)

# ----- TABLE ------
columns = ('#1', '#2', '#3', '#4')

table = ttk.Treeview(window, columns=columns, show='headings')
table.column('#1', minwidth=50, width=50, stretch=0)
table.column('#2', minwidth=50, width=250, stretch=0)
table.column('#3', minwidth=100, width=150, stretch=0)
table.column('#4', minwidth=50, width=107, stretch=0)
table.heading('#1', text='ID')
table.heading('#2', text='Name')
table.heading('#3', text='Phone Number')
table.heading('#4', text='Level')


# bind the select event
def selected_item(event):
    global selected_item0
    for selected_itm in table.selection():
        # dictionary
        item = table.item(selected_itm)
        # list
        record = item['values']
        selected_item0 = [record[0], record[1], record[2], record[3]]
        btn_delete.config(text=f'Delete {record[1]}')
        print(selected_item0)
        # showinfo(title='Information', message=record)


table.bind('<<TreeviewSelect>>', selected_item)
table.place(x=420, y=20, height=460, width=560)

# contacts = []


def update_table(event):
    create_table()
    selected = combo1.get()
    contacts = []
    table.delete(*table.get_children())
    print(selected)

    for n in member_list():
        if selected == 'Members only' and n[3] == 'Member':
            lst = [n[0], n[1], n[2], n[3]]
            contacts.append(lst)
        elif selected == 'Leaders only' and n[3] == 'Leader':
            lst = [n[0], n[1], n[2], n[3]]
            contacts.append(lst)
        elif selected == 'Everyone':
            lst = [n[0], n[1], n[2], n[3]]
            contacts.append(lst)

    for contact in contacts:
        table.insert('', END, values=contact)


update_table('text')
combo1.bind('<<ComboboxSelected>>', update_table)

# ----- Scrollbar -----
scrollbar = Scrollbar(window, orient=VERTICAL, command=table.yview)
table.configure(yscroll=scrollbar.set)
scrollbar.place(y=20, x=980, height=460)

if __name__ == '__main__':

    window.mainloop()
