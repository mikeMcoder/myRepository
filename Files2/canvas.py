import Tkinter as tk

root = tk.Tk()
cv = tk.Canvas(root)
cv.grid()
lbl = tk.Label(root, text = "Sample Label")
lbl.grid(row = 0, sticky="N")
#lbl.config()
root.mainloop()