import tkinter as tk
from tkinter import filedialog, messagebox
import PIL.Image, PIL.ImageTk, PIL.ImageDraw
import pystray
from pystray import MenuItem as item
import threading, os, sys, subprocess
import driver

class LcdBearApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LCD-BEAR GAMING v1.2")
        self.root.geometry("400x500")
        self.root.configure(bg="#0a0a0a")
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.res_w, self.res_h = tk.StringVar(value="320"), tk.StringVar(value="240")
        self.bear_img = self.create_bear_icon()
        self.setup_ui()

    def create_bear_icon(self):
        img = PIL.Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        draw = PIL.ImageDraw.Draw(img)
        draw.ellipse([20, 15, 50, 45], fill="#1a1a1a") 
        draw.ellipse([78, 15, 108, 45], fill="#1a1a1a")
        draw.ellipse([20, 25, 108, 110], fill="white", outline="#00ff00", width=2)
        draw.ellipse([35, 50, 55, 75], fill="#1a1a1a")
        draw.ellipse([73, 50, 93, 75], fill="#1a1a1a")
        draw.ellipse([42, 58, 48, 64], fill="#00ff00")
        draw.ellipse([80, 58, 86, 64], fill="#00ff00")
        draw.polygon([(60, 85), (68, 85), (64, 92)], fill="#1a1a1a")
        return img

    def setup_ui(self):
        self.logo_img = PIL.ImageTk.PhotoImage(self.bear_img.resize((80, 80)))
        tk.Label(self.root, image=self.logo_img, bg="#0a0a0a").pack(pady=10)
        tk.Label(self.root, text="LCD-BEAR GAMING", font=("Impact", 22), fg="#00ff00", bg="#0a0a0a").pack()
        frame = tk.LabelFrame(self.root, text=" SYSTEM CONFIG ", fg="#00ff00", bg="#1a1a1a", padx=10, pady=10)
        frame.pack(pady=20, padx=30, fill="x")
        tk.Label(frame, text="W:", bg="#1a1a1a", fg="white").grid(row=0, column=0)
        tk.Entry(frame, textvariable=self.res_w, width=6).grid(row=0, column=1, padx=5)
        tk.Label(frame, text="H:", bg="#1a1a1a", fg="white").grid(row=0, column=2)
        tk.Entry(frame, textvariable=self.res_h, width=6).grid(row=0, column=3, padx=5)
        tk.Button(self.root, text="⚡ UPLOAD SKIN ⚡", command=self.update, bg="#00ff00", fg="black", font=("Arial", 10, "bold")).pack(pady=10, padx=40, fill="x")
        tk.Button(self.root, text="OFFLINE", command=self.clear, bg="#1a1a1a", fg="#ff4444").pack(pady=5, padx=40, fill="x")

    def update(self):
        file = filedialog.askopenfilename()
        if file:
            driver.TurzxDevice().send_image(file, int(self.res_w.get()), int(self.res_h.get()))
    def clear(self):
        driver.TurzxDevice().send_image(None, int(self.res_w.get()), int(self.res_h.get()))
    def hide_window(self):
        self.root.withdraw()
        menu = (item("Show", self.show_window), item("Exit", self.quit_window))
        self.icon = pystray.Icon("LCD-BEAR", self.bear_img, "LCD-BEAR GAMING", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()
    def show_window(self):
        self.icon.stop(); self.root.deiconify()
    def quit_window(self):
        if hasattr(self, "icon"): self.icon.stop()
        self.root.destroy(); os._exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = LcdBearApp(root)
    root.mainloop()