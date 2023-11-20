import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
from tkinter import filedialog  

class WishPacketTracer:
    def __init__(self, root):
        self.root = root
        self.root.title("Wish Packet Tracer")

        self.canvas = tk.Canvas(root, bg="ivory", width=800, height=600)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.items = []  # Liste pour stocker les éléments dessinés
        self.current_item = None  # Stocke l'élément actuellement sélectionné
        self.item_images = {}
        self.links=[]

        self.start_link = None  # Initialisation de self.start_link pour gérer les liens

        self.nb_router=0
        self.nb_switch=0
        self.nb_client=0


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

        # Menu contextuel
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Modifier les propriétés", command=self.edit_proprietes)
        self.context_menu.add_command(label="Changer l'icône", command=self.change_icon)  # Ajouter l'option pour changer l'icône
        self.context_menu.add_command(label="Supprimer", command=self.delete_item)
        

        # Evènements souris
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.right_click)
        self.canvas.bind("<B1-Motion>", self.drag_item)
        self.canvas.bind("<Button-2>", self.middle_click)
        # Evènements clavier
        self.root.bind("<Key>", self.key_pressed)
        
        

    def create_client(self):
        item = self.canvas.create_image(100, 100, image=self.image_pc, tags="client")
        self.items.append({"item": item, "type": "client", "proprietes": {"name": f"Client{self.nb_client}"}})
        self.nb_client+=1

    def create_switch(self):
        item = self.canvas.create_image(200, 200, image=self.image_switch, tags="switch")
        self.items.append({"item": item, "type": "switch", "proprietes": {"name": f"Switch{self.nb_switch}"}})
        self.nb_switch+=1

    def create_router(self):
        item = self.canvas.create_image(300, 300, image=self.image_router, tags="router")
        self.items.append({"item": item, "type": "router", "proprietes": {"name": f"Router{self.nb_router}"}})
        self.nb_router+=1
        
    def lien(self, item1, item2):
        x1, y1 = self.canvas.coords(item1)
        x2, y2 = self.canvas.coords(item2)
        line = self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)  # Dessiner une ligne entre les éléments sélectionnés  
        self.links.append(line)  # Ajouter le lien à la liste des liens
        print(self.links)

        # Créer un menu contextuel pour les liens avec uniquement l'option "Supprimer"
        link_menu = tk.Menu(self.root, tearoff=0)
        link_menu.add_command(label="Supprimer", command=lambda: self.delete_link(line))
        self.canvas.tag_bind(line, "<Button-3>", lambda event, menu=link_menu: self.affiche_menu_lien(event, menu))

    def affiche_menu_lien(self, event, menu):
        menu.post(event.x_root, event.y_root)

    def delete_link(self, line):
        self.links.remove(line)  # Retirer le lien de la liste des liens
        print(self.links)
        self.canvas.delete(line)  # Supprimer graphiquement le lien

    def left_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item:
            self.current_item = item[0]

    def right_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item:
            self.current_item = item[0]
            self.context_menu.post(event.x_root, event.y_root)

    def middle_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item:
            if not self.start_link:  # Premier élément sélectionné
                self.start_link = item[0]
                print(self.start_link)
            else:  # Deuxième élément sélectionné
                self.end_link = item[0]
                self.lien(self.start_link, self.end_link)
                self.start_link = None
                print(self.end_link)


    def edit_proprietes(self):
        if self.current_item:
            item_type = self.canvas.gettags(self.current_item)[0]
            item = next(x for x in self.items if x["item"] == self.current_item )
            old_name=item["proprietes"]["name"]
            new_name = simpledialog.askstring("Modifier les propriétés", "Nouveau nom:", initialvalue=old_name)
            if new_name:
                item["proprietes"]["name"] = new_name

    def drag_item(self, event):
        if self.current_item:
            dx = event.x - self.canvas.coords(self.current_item)[0]
            dy = event.y - self.canvas.coords(self.current_item)[1]
            self.canvas.move(self.current_item, dx, dy)

    def load_and_resize_image(self, filename, width, height):
        image = Image.open(filename)
        image = image.resize((width, height))
        photo = ImageTk.PhotoImage(image)
        return photo

    def change_icon(self):
        if self.current_item:
            # Boîte de dialogue pour sélectionner un fichier PNG
            self.filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png")]) 
            if self.filename:
                self.photo=self.load_and_resize_image(self.filename,50,50)
                self.item_images[self.current_item] = self.photo
                # Changer l'image de l'élément actuellement sélectionné
                self.canvas.itemconfig(self.current_item, image=self.photo) 
    

    def key_pressed(self, event):
        key = event.char.upper()
        if key == "C":
            self.create_client()
        elif key == "S":
            self.create_switch()
        elif key == "R":
            self.create_router()
        

    def delete_item(self):
        if self.current_item:
            item = next(x for x in self.items if x["item"] == self.current_item)
            self.items.remove(item)
            self.canvas.delete(self.current_item)
   


root = tk.Tk()
app = WishPacketTracer(root)
root.mainloop()
