from customtkinter import CTk
from customtkinter import CTkButton, CTkCanvas, CTkLabel, CTkCheckBox, CTkFrame
from customtkinter import set_default_color_theme, BOTH
from customtkinter import filedialog as fd
# import ctypes
import sqlite3


font_for_btn = ("Comic Sans MS", 30)
font_for_lbl = ("Comic Sans MS", 40)


set_default_color_theme("green")
class MainApplication(CTk):
    def __init__(self):
        super().__init__()
        
        self.title("TeleMove")
        self.iconbitmap("Logo.ico")
        self.geometry("600x450")
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
            self.geometry("780x620")
        
        if page:
            page.place(x=0, y=0, relwidth=1, relheight=1)
            page.tkraise()
            

class HomePage(CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        
        self.directory = ""
        
        self.greeting_lbl = CTkLabel(self, text="Здравствуйте", font=font_for_lbl)
        self.greeting_lbl.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.btn_dir = CTkButton(self, text="Выбрать папку", font=font_for_btn, command=self.choose_directory, width=70, height=40)
        self.btn_dir.grid(row=1, column=0, padx=120, pady=20, sticky="ew")
        
        self.btn_correct = CTkButton(self, text="Подтвердить", font=font_for_btn, command=self.click_on_correct, width=70, height=40)
        self.btn_correct.grid(row=2, column=0, padx=120, pady=20, sticky="ew")
        
        self.insert_deep_dir_chkbx = CTkCheckBox(self, text="Включить подпапки", font=font_for_btn)
        self.insert_deep_dir_chkbx.grid(row=3, column=0, padx=137, pady=20, sticky="ew")
        
        self.label_dir = CTkLabel(self, text="", font=("Comic Sans MS", 20))
        self.label_dir.grid(row=4, column=0, padx=0, pady=0)
        
        self.info_btn = CTkButton(self, text="i", font=("Comic Sans MS", 25), command=self.call_info, width=40, height=10,
                                  fg_color="#6A5ACD", hover_color="#3F32A4")
        self.info_btn.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        
        

    def call_info(self):
        pass
    
    def choose_directory(self):
        try:
            conn = sqlite3.connect("data/TeleMove.db")
            cur = conn.cursor()
            
            cur.execute("DELETE FROM path WHERE pathid=1")
            conn.commit()
        except:
            pass
        
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
        
        self.show_diagramm_btn = CTkButton(self, text="Показать\nдиаграмму", font=("Comic Sans MS", 30), width=220, height=210,
                                           command=self.show_diagram)
        self.show_diagramm_btn.grid(row=0, column=0, padx=20, pady=20, rowspan=4)
        
        self.type_lbl = CTkLabel(self, text="Выберите тип сортировки", font=font_for_lbl)
        self.type_lbl.grid(row=0, column=1, padx=10, pady=10, sticky="nw")
        
        self.sort_by_name_btn = CTkButton(self, text="Сортировать по имени", font=font_for_btn,
                                       command=self.sort_by_name, width=25)
        self.sort_by_name_btn.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        self.sort_by_extension_btn = CTkButton(self, text="Сортировать по расширению", font=font_for_btn,
                                        command=self.sort_by_extension, width=25)
        self.sort_by_extension_btn.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

        self.sort_by_size_btn = CTkButton(self, text="Сортировать по размеру", font=font_for_btn,
                                   command=self.sort_by_size, width=25)
        self.sort_by_size_btn.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
        
        self.sort_by_meta_btn = CTkButton(self, text="Сортировать по метаданным", font=font_for_btn,
                                      command=self.sort_by_meta, width=25)
        self.sort_by_meta_btn.grid(row=4, column=1, padx=20, pady=10, sticky="ew")
        
        self.info_btn = CTkButton(self, text="i", font=("Comic Sans MS", 25), command=self.call_info, width=40, height=10,
                                  fg_color="#6A5ACD", hover_color="#3F32A4")
        self.info_btn.grid(row=5, column=1, columnspan=3, padx=10, pady=10, sticky="e")
        
    
    def show_diagram(self):
        from matplotlib.pyplot import bar, show
        
        ext = ["txt", "doc", "png", "jpg", "py"]
        cnt = [120, 50, 23, 90, 55]
        
        bar(ext, cnt)
        show()
        pass
    def call_info(self):
        pass
        
    def sort_by_name(self):
        pass
        
    def sort_by_extension(self):
        pass
    
    def sort_by_size(self):
        pass
    
    def sort_by_meta(self):
        pass


app = MainApplication()
app.mainloop()