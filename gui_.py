import customtkinter as ctk
from tkinter import filedialog
from pdf_edit import PDFEdit

class ShowData(ctk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, parent, name="Untitled", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.name = name
        self.title(self.name)
        self.geometry("600x400")

        self.attributes('-topmost', True)
        self.focus_force()
        self.lift()
        self.after(200, lambda: self.attributes('-topmost', False))

        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.label = ctk.CTkLabel(self, text=f"{self.name} PDF", font=('arial', 24, 'bold'))
        self.label.grid(padx=20, pady=10, row=0, column=0, columnspan=2)

        # ✅ هنا التعديل المهم
        self.scroll_frame = ShowData(self, width=400, height=200)
        self.scroll_frame.grid(padx=20, pady=10, row=1, column=0, columnspan=2, sticky="nsew")

        self.choose_files_btn = ctk.CTkButton(self, text="Choose Files", command=self.choose_files_fun)
        self.choose_files_btn.grid(row=2, column=0)

        self.function_btn = ctk.CTkButton(self, text=f"Click To {self.name}", command=self.btn_fun)
        self.function_btn.grid(row=2, column=1, pady=10)

        # مكان عرض الملفات المختارة داخل scroll frame
        self.label_files = ctk.CTkLabel(self.scroll_frame, text="", font=('arial', 16))
        self.label_files.grid(row=0, column=0, padx=20)

    def choose_files_fun(self):
        self.path_files = filedialog.askopenfilenames()
        if self.path_files:
            names = [file.split('/')[-1] for file in self.path_files]
            self.label_files.configure(text="\n".join(names), text_color='green',font=('arial', 18, 'bold') )
        self.after(100, lambda: (self.lift(), self.focus_force()))

    def btn_fun(self):
        if self.name == 'Reverse':
          if (PDFEdit().pdf_reverse([path for path in self.path_files])):
              self.label_files.grid_forget()
            
        elif self.name == "Marge":
            if (PDFEdit().pdf_marge([path for path in self.path_files])):
                        self.label_files.grid_forget()
        elif self.name == "Split":
            print("Split")
        else :
            print("Idk")


class PDFEditGui(ctk.CTk):
    def __init__(self):
        super().__init__()


        self.title("PDF Editing")
        self.geometry("600x400")

        self.windows = {}  # هنا نخزن كل نافذة مفتوحة حسب اسمها

        self.pdf_reverse_btn = ctk.CTkButton(
            self,
            text="Reverse PDF",
            command=lambda: self.open_toplevel_fun('Reverse')
        )
        self.pdf_reverse_btn.pack(expand=True)

        self.pdf_split_btn = ctk.CTkButton(
            self,
            text="Split PDF",
            command=lambda: self.open_toplevel_fun('Split')
        )
        self.pdf_split_btn.pack(expand=True)

        self.pdf_marge_btn = ctk.CTkButton(
            self,
            text="Marge PDF",
            command=lambda: self.open_toplevel_fun('Marge')
        )
        self.pdf_marge_btn.pack(expand=True)

    def open_toplevel_fun(self, name):
        # لو النافذة دي مش مفتوحة أو اتقفلت بالفعل → افتحها
        if name not in self.windows or not self.windows[name].winfo_exists():
            self.windows[name] = ToplevelWindow(self, name=name)
        else:
            # لو مفتوحة، رجعها للواجهة بدل ما تفتح تانية
            self.windows[name].focus()
            self.windows[name].lift()


if __name__ == "__main__":
    app = PDFEditGui()
    app.mainloop()
