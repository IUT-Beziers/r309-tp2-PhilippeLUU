import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk

class WishPacketTracer:
    def __init__(self, root):
        self.root = root
        self.root.title("Wish Packet Tracer")

        self.canvas = tk.Canvas(root, bg="ivory", width=800, height=600)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

if __name__ == "__main__":
    root = tk.Tk()
    app = WishPacketTracer(root)
    root.mainloop()
