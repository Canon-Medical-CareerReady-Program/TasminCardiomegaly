import tkinter as tk
from App.main_app_window import MainAppWindow

def main():
    root = tk.Tk(className="Cardiomegaly Application")
    app = MainAppWindow(root)

    root.mainloop()


if __name__ == "__main__":
    main()
