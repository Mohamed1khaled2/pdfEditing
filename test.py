import customtkinter
from tkinterdnd2 import TkinterDnD, DND_ALL

class App(customtkinter.CTk, TkinterDnD.DnDWrapper):
      def __init__(self):
          super().__init__()
          self.TkinterDnDVersion = TkinterDnD._require(self)

          self.title("Drag and Drop Example")
          self.geometry("400x300")

          self.label = customtkinter.CTkLabel(self, text="Drop files here")
          self.label.pack(pady=20)

          # Configure the label to accept file drops
          self.label.dnd_bind('<<Drop>>', self.handle_drop)

      def handle_drop(self, event):
          # The event.data contains the path(s) of the dropped file(s)
          print(f"Dropped files: {event.data}")
          self.label.configure(text=f"Dropped: {event.data}")

if __name__ == "__main__":
    app = App()
    app.mainloop()