import tkinter as tk
from app.gui import FRASApp

def main():
    root = tk.Tk()
    app = FRASApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()