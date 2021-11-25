import tkinter as tk
import tkinter.filedialog as dialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

# ---------------------------------- 常數設定 ---------------------------------- #
BTN_FONT = ("Arial", 13, "bold")
BTN_COLOR = "#1C7947"
FG = "#fff"
WM_FONT = "arial.ttf"
WM_COLOR = (255, 255, 255, 150)
WINDOW_H = 700
WINDOW_W = 700
BG_IMG_FIELD = "#D3E4CD"


# ---------------------------------- Function ---------------------------------- #
class Ui:
    """
    透過PIL Draw 新增一個同照片大小的畫布，加上浮水印後，再與原照片合併。
    圖片依視窗顯示縮小加上浮水印後，再還原原圖大小。
    """
    def __init__(self, root):
        # 在此建立所有物件(即ui的屬性)
        # part 1: img
        self.field_img = tk.Frame(root, width=WINDOW_W, height=WINDOW_H)
        # Frame大小會跟著children變動，而canvas預設有邊框2，因此一定要額外設highlightthickness=0，這樣取得的winfo_width和winfo_height才會正確。
        self.canvas = tk.Canvas(self.field_img, width=WINDOW_W, height=WINDOW_H, bg=BG_IMG_FIELD, highlightthickness=0)
        # part 2: file
        self.field_file = tk.Frame(root)
        self.btn_open = tk.Button(self.field_file, text="Select Image", command=self.select_img, font=BTN_FONT, bd=3,
                                  bg=BTN_COLOR, fg=FG, width=13)
        self.btn_delete = tk.Button(self.field_file, text="Cancel", command=self.remove_img, font=BTN_FONT, bd=3,
                                    bg="gray", fg=FG, width=13)
        self.btn_rotate = tk.Button(self.field_file, text="Rotate 90°", command=self.rotate, font=BTN_FONT, bd=3,
                                    bg=BTN_COLOR, fg=FG, width=13)
        self.btn_save = tk.Button(self.field_file, text="Save Image", command=self.save_img, font=BTN_FONT, bd=3,
                                  bg="skyblue", fg=FG, width=13)
        # part 3: manipulate
        self.field_manipulate = tk.Frame(root)
        self.label_enter = tk.Label(self.field_manipulate, text="Enter words for watermark:")
        self.entry_watermark = tk.Entry(self.field_manipulate)
        # 設定watermark顯示方式
        self.option_var = tk.IntVar()
        self.option1 = tk.Radiobutton(self.field_manipulate, text="top", variable=self.option_var, value=1)
        self.option2 = tk.Radiobutton(self.field_manipulate, text="center", variable=self.option_var, value=0)
        self.option3 = tk.Radiobutton(self.field_manipulate, text="bottom", variable=self.option_var, value=2)
        self.option4 = tk.Radiobutton(self.field_manipulate, text="45°", variable=self.option_var, value=3)
        self.option5 = tk.Radiobutton(self.field_manipulate, text="315°", variable=self.option_var, value=4)
        self.wm_font = tk.Scale(self.field_manipulate, label='Font Size', from_=30, to=90, orient=tk.HORIZONTAL,
                                length=150, showvalue=1, tickinterval=20, resolution=1)
        self.btn_watermark = tk.Button(self.field_manipulate, text="Add watermark", command=self.add_watermark,
                                       font=BTN_FONT, bd=3, bg=BTN_COLOR, fg=FG, width=13)
        self.img = Image.open("example.png").convert("RGBA")  # origin image
        self.img_width = self.img.size[0]  # store the size of origin image - width
        self.img_height = self.img.size[1]  # store the size of origin image  height
        self.show_img = None  # store the image of showing in the window
        self.canvas_img = None  # 將canvas內的文字widget設成變數，以利後續的更換裡面的圖片(顯示放上浮水印後的圖)。
        self.px = 0  # store the center of canvas
        self.py = 0  # store the center of canvas
        self.wm_x = 0  # store the position of x in order to put watermark
        self.wm_y = 0  # store the position of y in order to put watermark
        self.setting()
        self.get_center()
        self.show()

    def setting(self):
        self.field_img.grid(column=1, row=1, rowspan=2)
        self.canvas.pack()
        self.field_file.grid(column=2, row=1, padx=20)
        self.btn_open.pack(pady=3)
        self.btn_delete.pack(pady=3)
        self.btn_rotate.pack(pady=3)
        self.btn_save.pack(pady=3)
        self.field_manipulate.grid(column=2, row=2)
        self.label_enter.grid(column=2, row=0, columnspan=3, pady=3)
        self.entry_watermark.grid(column=2, row=1, columnspan=3, pady=3)
        self.option1.grid(column=2, row=2)
        self.option2.grid(column=3, row=2)
        self.option3.grid(column=4, row=2)
        self.option4.grid(column=2, row=3)
        self.option5.grid(column=3, row=3)
        self.wm_font.grid(column=2, row=4, columnspan=3, pady=5)
        self.btn_watermark.grid(column=2, row=5, columnspan=3, pady=3)

    def select_img(self):
        path = dialog.askopenfilename(title="選擇檔案(Choose files)", filetypes=(("JPG", ".jpg"), ("PNG", ".png")))
        self.img = Image.open(path).convert("RGBA")  # 以rgba方式讀取檔案，以利後與含浮水印圖片結合
        self.show()

    def show(self):
        self.img_width = self.img.size[0]  # 將原始圖片大小儲存，瀏覽後最後要再轉回原本大小用
        self.img_height = self.img.size[1]  # 將原始圖片大小儲存，瀏覽後最後要再轉回原本大小用
        self.resize(w=self.img_width, h=self.img_height, w_box=self.field_img.winfo_width(),
                    h_box=self.field_img.winfo_height())
        self.show_img = ImageTk.PhotoImage(self.show_img, self.show_img.size)  # 用ImageTk模組來讀取圖片，讓其可以tkinter內使用
        self.canvas_img = self.canvas.create_image(self.px, self.py, image=self.show_img)  # 將圖片放到canvas中心點。

    def remove_img(self):
        self.canvas.delete("all")

    def rotate(self):
        self.img = self.img.transpose(Image.ROTATE_90)  # 用Image.transpose來進行圖片旋轉
        self.show_img = ImageTk.PhotoImage(self.img, self.img.size)  # 依旋轉後的圖片重新讀取
        self.canvas.itemconfig(self.canvas_img, image=self.show_img)
        # 以下將旋轉後的長、寬互換，以利後續合併完圖片後，還原本圖片。
        x = self.img_height
        y = self.img_width
        self.img_width = x
        self.img_height = y
        print(f"rotate x: {self.img_width} rotate y: {self.img_height}")

    def get_center(self):
        self.canvas.update()
        self.px = self.canvas.winfo_width() / 2
        self.py = self.canvas.winfo_height() / 2

    def resize(self, w, h, w_box, h_box):
        if w < w_box and h < h_box:
            self.show_img = self.img
        else:
            # 計算長、寬比例，取最小的，才不會讓resize後的圖片超過容器大小。
            times = min(w_box / w, h_box / h)
            new_w = int(round(w * times, 0))
            new_h = int(round(h * times, 0))
            # 將圖片依倍數重新縮放，調整圖片大小，以利後續讀取
            self.show_img = self.img.resize((new_w, new_h))
            self.img = self.img.resize((new_w, new_h))  # 將resize後的img回存原img，以利後續合併浮水印用

    def add_watermark(self):
        self.show()  # 因應多次加上浮水印，所以每次都要讀取一遍，讓圖片縮小顯示
        wm_font = ImageFont.truetype(WM_FONT, size=self.wm_font.get())
        fake_img = Image.new("RGBA", self.img.size, (0, 0, 0, 0))  # 建立一個完全透明的圖
        # 處理fake_img，建立一個在fake_img上畫圖的物件，操作結果會存在fake_img上。
        draw = ImageDraw.Draw(fake_img)
        wm_text = self.entry_watermark.get()
        rotate = None  # 建立一個rotate的變數
        self.get_wm_position()
        if self.option_var.get() == 1:
            draw.text((self.wm_x, self.wm_y), wm_text, font=wm_font, fill=WM_COLOR, anchor="mt")  # anchor依顯示位置不同而不同
        elif self.option_var.get() == 2:
            draw.text((self.wm_x, self.wm_y), wm_text, font=wm_font, fill=WM_COLOR, anchor="mb")
        elif self.option_var.get() == 3:
            draw.text((self.wm_x, self.wm_y), wm_text, font=wm_font, fill=WM_COLOR, anchor="mm")
            rotate = fake_img.rotate(angle=45, expand=False)
        elif self.option_var.get() == 4:
            draw.text((self.wm_x, self.wm_y), wm_text, font=wm_font, fill=WM_COLOR, anchor="mm")
            rotate = fake_img.rotate(angle=315, expand=False)
        else:
            draw.text((self.wm_x, self.wm_y), wm_text, font=wm_font, fill=WM_COLOR, anchor="mm")
        if rotate:
            fake_img.paste(rotate)
        # 將已上了文字的圖和原物合併
        self.img = Image.alpha_composite(self.img, fake_img)
        self.show_img = ImageTk.PhotoImage(image=self.img, size=self.img)
        self.canvas.itemconfig(self.canvas_img, image=self.show_img)
        self.img = self.img.resize((self.img_width, self.img_height))  # 還原原始圖片大小解析度
        self.img.show()
        print(f"add rotate x: {self.img_width} rotate y: {self.img_height}")

# todo:轉換有問題，圖沒有還原
    def get_wm_position(self):
        # 預設置中
        self.wm_x = self.img.size[0] // 2
        self.wm_y = self.img.size[1] // 2
        if self.option_var.get() == 1:
            self.wm_x = self.img.size[0] // 2
            self.wm_y = 0
        elif self.option_var.get() == 2:
            self.wm_x = self.img.size[0] // 2
            self.wm_y = self.img.size[1]

    def save_img(self):
        filename = dialog.asksaveasfile(mode="w", title="Save To", defaultextension=".png",
                                        filetypes=(("png files", "*.png"), ("All files", "*.*")))
        if filename.name:
            self.img.save(filename.name)


# ---------------------------------- UI setting -Main Window ---------------------------------- #
window = tk.Tk()
window.title("Image Watermarking")
# 設定視窗的位置與大小 widthxheight+x+y
window.geometry(f"{WINDOW_W+180}x{WINDOW_H}+0+0")
window.update()
ui = Ui(window)
window.mainloop()
