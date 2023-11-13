import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk

class WishPacketTracer:
    def __init__(self, root):
        self.root = root
        self.root.title("Wish Packet Tracer")

        self.canvas = tk.Canvas(root, bg="ivory", width=800, height=600)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.items = []  # Liste pour stocker les éléments dessinés
        self.current_item = None  # Stocke l'élément actuellement sélectionné

        # Barre d'outils
        self.toolbar = tk.Frame(root)
        self.toolbar.pack(side=tk.LEFT, fill=tk.Y)

        # Boutons de la barre d'outils (utilisant des images redimensionnées avec PIL)
        self.image_router = self.load_and_resize_image("./img/Router.png", 50, 50)
        self.button_router = tk.Button(self.toolbar, image=self.image_router, command=self.create_router)
        self.button_router.pack(side=tk.LEFT)

        self.image_switch = self.load_and_resize_image("./img/switch.png", 50, 50)
        self.button_switch = tk.Button(self.toolbar, image=self.image_switch, command=self.create_switch)
        self.button_switch.pack(side=tk.LEFT)

        self.image_pc = self.load_and_resize_image("./img/pc.png", 50, 50)
        self.button_client = tk.Button(self.toolbar, image=self.image_pc, command=self.create_client)
        self.button_client.pack(side=tk.LEFT)

    def create_client(self):
        item = self.canvas.create_image(100, 100, image=self.image_pc, tags="client")
    def create_switch(self):
        item = self.canvas.create_image(200, 200, image=self.image_switch, tags="switch")
    
    def create_router(self):
        item = self.canvas.create_image(300, 300, image=self.image_router, tags="router")
    
   
    def load_and_resize_image(self, filename, width, height):
        image = Image.open(filename)
        image = image.resize((width, height))
        photo = ImageTk.PhotoImage(image)
        return photo

root = tk.Tk()
app = WishPacketTracer(root)
root.mainloop()