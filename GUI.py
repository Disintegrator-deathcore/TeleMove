from customtkinter import *
from customtkinter import filedialog as fd
import matplotlib.pyplot as plt
import ctypes
import sqlite3


font_for_btn = ("Comic Sans MS", 30)
font_for_lbl = ("Comic Sans MS", 35)



try:
    conn = sqlite3.connect("data/TeleMove.db")
    cur = conn.cursor()
    
    cur.execute("DELETE FROM path WHERE pathid=1")
    conn.commit()
except:
    pass

set_default_color_theme("green")
class MainApplication(CTk):
    def __init__(self):
        super().__init__()
        
        self.title("TeleMove")
        self.geometry("600x400")
        self.resizable(width=False, height=False)
        self.conn = sqlite3.connect("data/TeleMove.db")
        self.cur = self.conn.cursor()
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS path(
            pathid INT PRIMARY KEY,
            path TEXT);""")
        self.conn.commit()
        
        self.directory = ""
        
        self.pages = {}
        self.container = CTkFrame(self)
        self.container.pack(fill=BOTH, expand=True)
        
        self.create_page("Главная", HomePage)
        self.create_page("Функции", FuncPage)
        
        self.show_page("Главная")
        
    def create_page(self, title, page_class):
        page = page_class(self.container, self)
        self.pages[title] = page
        
    def show_page(self, title):
        page = self.pages.get(title)
        if title == "Функции":
            self.geometry("1000x1000")
        
        if page:
            page.place(x=0, y=0, relwidth=1, relheight=1)
            page.tkraise()
            

class HomePage(CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        
        self.directory = ""
        
        self.greeting_lbl = CTkLabel(self, text="Здравствуйте", font=("Comic Sans MS", 25))
        self.greeting_lbl.grid(row=0, column=0, padx=20, pady=20)
        
        self.btn_dir = CTkButton(self, text="Выбрать папку", font=font_for_btn, command=self.choose_directory, width=70, height=40)
        self.btn_dir.grid(row=1, column=0, padx=70, pady=20)
        
        self.btn_correct = CTkButton(self, text="Подтвердить", font=font_for_btn, command=self.click_on_correct, width=70, height=40)
        self.btn_correct.grid(row=2, column=0, padx=70, pady=20)
        
        self.label_dir = CTkLabel(self, text="", font=font_for_lbl)
        self.label_dir.grid(row=3, column=0, padx=20, pady=20)
        

    def choose_directory(self):
        self.directory = fd.askdirectory(title="Выбрать папку", initialdir="/")
        
        if self.directory:
            self.app.cur.execute(f"""INSERT INTO path (pathid, path) VALUES ('1', '{self.directory}');""")
            self.app.conn.commit()
            self.label_dir.configure(text=str(self.directory))
            
    def click_on_correct(self):
        if ((self.directory != "") and
            (self.directory != "Вы не выбрали папку")):
            self.open_func_page()
        else:
            self.label_dir.configure(text=str("Вы не выбрали папку"))
            
    def open_func_page(self):
        self.app.show_page("Функции")
        

class FuncPage(CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        
        self.app = app
        
        self.canvas = CTkCanvas(self, width=300, height=300)
        self.canvas.create_oval(50, 50, 250, 250, fill="red")
        self.canvas.create_arc(50, 50, 250, 250, fill="green", start=0, extent=45)
        self.canvas.grid(row=0, column=0, padx=20, pady=20)
        
        self.type_lbl = CTkLabel(self, text="Выберите тип сортировки", font=font_for_lbl)
        self.type_lbl.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        
        self.sort_by_name_btn = CTkButton(self, text="Сортировать по имени", font=font_for_btn,
                                       command=self.sort_by_name, width=25)
        self.sort_by_name_btn.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

        self.sort_by_extension_btn = CTkButton(self, text="Сортировать по расширению", font=font_for_btn,
                                        command=self.sort_by_extension, width=25)
        self.sort_by_extension_btn.grid(row=2, column=1, padx=20, pady=20, sticky="ew")

        self.sort_by_size = CTkButton(self, text="Сортировать по размеру", font=font_for_btn,
                                   command=self.sort_by_size, width=25)
        self.sort_by_size.grid(row=3, column=1, padx=20, pady=20, sticky="ew")
        
    def sort_by_name(self):
        self.app.cur.execute("SELECT * FROM path WHERE pathid=1")
        path = self.app.cur.fetchone()[1] + "\\file.txt"
        func_dll = ctypes.CDLL('C:/programming/pyCpp/TeleMove/func.dll')
        func_dll.read_dir(path.encode("utf-8"))
        
    
    def sort_by_extension(self):
        func_dll = ctypes.CDLL('./func.dll')
        msg = func_dll.show_msg()
        print(msg)
    
    def sort_by_size(self):
        pass


app = MainApplication()
app.mainloop()