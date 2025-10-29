import customtkinter as ctk
from tkinter import filedialog
from pdf_edit import PDFEdit
from CTkMessagebox import CTkMessagebox


class ShowData(ctk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class ConformSplitButtonWindow(ctk.CTkToplevel):
    def __init__(self, parent, error_message_box, *args, fg_color=None, **kwargs):

        self.from_to = {}
        self.__error_message_box = error_message_box
        super().__init__(parent, *args, fg_color=fg_color, **kwargs)

        self.title("Conform Split Window")
        self.geometry("400x200")
        self.attributes("-topmost", True)
        self.focus_force()
        self.lift()
        self.after(200, lambda: self.attributes("-topmost", False))

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1), weight=1)

        self.from_entry = ctk.CTkEntry(self, placeholder_text="Split PDF From..")
        self.from_entry.grid(column=0, row=0)
        self.from_entry.bind("<Return>", self.submit_fun)
        self.to_entry = ctk.CTkEntry(self, placeholder_text="Split PDF To..")

        self.to_entry.grid(column=1, row=0)
        self.to_entry.bind("<Return>", self.submit_fun)

        self.submit_btn = ctk.CTkButton(self, text="Submit", command=self.submit_fun)

        self.submit_btn.grid(row=1, column=0, columnspan=2)

    def submit_fun(self, event=None):
        self.from_to["from"] = self.from_entry.get()
        self.from_to["to"] = self.to_entry.get()

        if self.__error_message_box:

            if self.from_to["from"].isdigit() and self.from_to["to"].isdigit():
                self.destroy()

            else:
                self.__error_message_box("You are not typing count in from or to")


class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, parent, name="Untitled", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.pdf_edit = PDFEdit()

        self.name = name
        self.title(self.name)
        self.geometry("600x400")

        self.attributes("-topmost", True)
        self.focus_force()
        self.lift()
        self.after(200, lambda: self.attributes("-topmost", False))

        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.label_name_process = ctk.CTkLabel(
            self, text=f"{self.name} PDF", font=("arial", 24, "bold")
        )
        self.label_name_process.grid(padx=20, pady=10, row=0, column=0, columnspan=2)

        self.scroll_frame = ShowData(self, width=400, height=200)
        self.scroll_frame.grid(
            padx=20,
            pady=10,
            row=1,
            column=0,
            columnspan=2,
            sticky="nsew",
        )

        # مكان عرض الملفات المختارة داخل scroll frame
        self.label_files = ctk.CTkLabel(self.scroll_frame, text="", font=("arial", 16))

        self.choose_files_btn = ctk.CTkButton(
            self, text=f"{"Choose Files"}", command=self.choose_files_fun
        )
        self.choose_files_btn.grid(row=2, column=0)

        self.function_btn = ctk.CTkButton(
            self, text=f"Click To {self.name}", command=self.btn_fun
        )
        self.function_btn.grid(row=2, column=1, pady=10)

        self.path_files = ()
        self.pdfs_names = ""

    def choose_files_fun(self):
        self.path_files = filedialog.askopenfilenames(
            filetypes=[("pdf", "*.pdf")],
        )  # Tuple of file paths
        if self.path_files:
            self.pdfs_names = [file.split("/")[-1] for file in self.path_files]
            self.label_files.configure(
                text="\n".join(self.pdfs_names),
                text_color="green",
                font=("arial", 18, "bold"),
                justify="center",
                anchor="center",
            )
            self.label_files.grid(row=0, column=0, padx=20, sticky="nsew")
            self.after(100, lambda: (self.lift(), self.focus_force()))
        else:
            self.__no_files_selected()
            # because of already any name files in scrollable frame
            self.label_files.grid_forget()

    def btn_fun(self):

        if len(self.path_files) != 0:
            if self.name == "Reverse":
                pdf_rev = self.pdf_edit.pdf_reverse([path for path in self.path_files])
                if isinstance(pdf_rev, tuple):
                    if ".pdf extension" in pdf_rev[1]:
                        self.__error_message_box(message="Error in extension files")

                self.label_files.grid_forget()

            elif self.name == "Marge":
                pdf_marge = self.pdf_edit.pdf_marge([path for path in self.path_files])
                if isinstance(pdf_rev, tuple):
                    if ".pdf extension" in pdf_marge[1]:
                        self.__error_message_box(message="Error in extension files")
                self.label_files.grid_forget()

                # error handled in pdf_marge method
            elif self.name == "Split":
                if (
                    not hasattr(self, "split_window")
                    or not self.split_window.winfo_exists()
                ):
                    self.split_window = ConformSplitButtonWindow(
                        self, error_message_box=self.__error_message_box
                    )
                    self.wait_window(self.split_window)
                else:
                    self.split_window.focus()
                    self.split_window.lift()

                from_to = (
                    int(self.split_window.from_to["from"]),
                    int(self.split_window.from_to["to"]),
                )
                pdf_split = self.pdf_edit.pdf_split(
                    [path for path in self.path_files], from_=from_to[0], to=[1]
                )

                if isinstance(pdf_split, tuple):
                    if ".pdf extension" in pdf_split[1]:
                        self.__error_message_box(message="Error in extension files")
                self.label_files.grid_forget()
        else:
            self.__error_message_box(message="You don't choose any files")
            self.label_files.grid_forget()

    def __error_message_box(self, message):
        CTkMessagebox(
            title="Error", message=message.capitalize(), icon="cancel", sound=True
        )


class PDFEditGui(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PDF Editing")
        self.geometry("600x400")

        self.windows = {}  # هنا نخزن كل نافذة مفتوحة حسب اسمها

        self.pdf_reverse_btn = ctk.CTkButton(
            self, text="Reverse PDF", command=lambda: self.open_toplevel_fun("Reverse")
        )
        self.pdf_reverse_btn.pack(expand=True)

        self.pdf_split_btn = ctk.CTkButton(
            self, text="Split PDF", command=lambda: self.open_toplevel_fun("Split")
        )
        self.pdf_split_btn.pack(expand=True)

        self.pdf_marge_btn = ctk.CTkButton(
            self, text="Marge PDF", command=lambda: self.open_toplevel_fun("Marge")
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
