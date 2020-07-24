import Tkinter as tk
import sqlite3
from constants import DELAY,DB_PATH

def update_data_for_cod_bod():
    conn = sqlite3.connect('ubiqx_db.db')
    c = conn.cursor()
    execute_query = c.execute('''select cod,bod,tss from front_end_data where subordinate_id=1''')
    result_set = c.fetchall()

    data_for_cod = 0
    data_for_bod = 0
    data_for_tss = 0
    for row in result_set:
        data_for_cod = row[0] # do you actually want += instead?
        data_for_bod = row[1]
        data_for_tss = row[2]
    # use itemconfig() to modify the labels text
    canvas.itemconfig(lbl_cod_data, text="COD             "+str(data_for_cod))
    canvas.itemconfig(lbl_bod_data, text="BOD             "+str(data_for_bod))
    canvas.itemconfig(lbl_tss_data, text="TSS             "+str(data_for_tss))
    root.after(DELAY, update_data_for_cod_bod)  # Call this function again after DELAY ms.

root = tk.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h)) # (h, w) in your original code
root.title("COD_BOD")
root.configure(background='black')
root.bind("<Escape>", lambda e: root.quit())

# width=h and height=w in your original code
canvas = tk.Canvas(root, width=w, height=h, highlightthickness=0, bg="dark blue")
canvas.pack()

blackline = canvas.create_line(100, 100, 800, 100, fill="yellow")

lbl_font = ("Times New Roman", 50, "bold")
lbl_cod_data = canvas.create_text(100, 100, text="COD", font=lbl_font, anchor='nw', fill="white")
lbl_bod_data = canvas.create_text(100, 180, text="BOD", font=lbl_font, anchor='nw', fill="green")
lbl_tss_data = canvas.create_text(100, 260, text="TSS", font=lbl_font, anchor='nw', fill="yellow")

update_data_for_cod_bod()  # Starts periodic calling of itself.
root.mainloop()