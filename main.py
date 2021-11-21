import tkinter as tk
import tkinter.filedialog as dialog
# PIL(Pillow) 為一個著名的影像處理套件
from PIL import Image, ImageTk

# ---------------------------------- 常數設定 ---------------------------------- #

PADDING = 20
BTN_FONT = ("Arial", 13, "bold")
BTN_COLOR = "#1C7947"
FONT = "#fff"
WINDOW_H = 600
WINDOW_W = 700
BG_IMG_FIELD = "#98DED9"
WATERMARK = None

new_image = None
x_gap = 0
y_gap = 0
new_w = 0
new_h = 0
font_size = 0



# ---------------------------------- Function ---------------------------------- #
def count_gap(in_w, in_h, out_w, out_h):
    print(f"新圖寬{in_w} * 高{in_h}")
    print(f"外框寬{out_w} * 高{out_h}")
    global x_gap, y_gap
    x_gap = out_w - in_w
    y_gap = out_h - in_h


def resize(w, h, w_box, h_box, img):
    # 計算長、寬比例，取最小的，才不會讓resize後的圖片超過容器大小。
    times = min(w_box / w, h_box / h)
    global new_w, new_h
    new_w = int(w * times)
    new_h = int(h * times)
    # 將圖片依倍數重新縮放，調整圖片大小，以利後續讀取
    new_img = img.resize((new_w, new_h), Image.ANTIALIAS)
    print(new_w, new_h)
    count_gap(in_w=new_w, in_h=new_h, out_w=w_box, out_h=h_box)

    return ImageTk.PhotoImage(new_img)


# 顯示讓使用者選擇圖片，並儲存該路徑。Function of Select_Img
def select_img():
    image_path = dialog.askopenfilename(title="選擇檔案(Choose files)", filetypes=(("JPG", ".jpg"), ("PNG", ".png")))
    image = Image.open(image_path)
    print(image_path)
    img_w, img_h = image.size
    print(Image.ANTIALIAS)
    global new_image
    new_image = resize(w=img_w, h=img_h, w_box=WINDOW_W, h_box=WINDOW_H, img=image)
    # 重新依圖片大小更改canvas大小；/2 用以將圖片置中
    field_img.config(width=new_image.width(), height=new_image.height())
    canvas.config(width=new_image.width(), height=new_image.height(), bd=0)
    print(f"canvas {new_image.width()}, {new_image.height()}")
    canvas.create_image(new_image.width()//2, new_image.height()//2, image=new_image)

    # canvas.itemconfig(image=new_image)


# 移除照片，重新來過
def remove_img():
    canvas.delete("all")


# 儲存成ps檔，後續用photoshop等打開
def save_to_ps():
    filename = dialog.asksaveasfile(mode="w", title="Save To", defaultextension=".ps", filetypes=(("ps files", "*.ps"), ("All files", "*.*")))
    print(filename)
    if filename.name:
        canvas.update()
        canvas.postscript(file=filename.name, colormode='color')
        print(filename.name)


def add_watermark():
    global new_image, WATERMARK, new_w, new_h, font_size
    font_size = wm_font.get()
    WATERMARK = entry_watermark.get()
    x = new_w // 2
    y = new_h // 2
    canvas.create_text(x, y, text="", fill=FONT, tags="watermark")
    if option_var.get() == 0:
        canvas.delete("watermark")
        canvas.create_text(x, y, text=WATERMARK, fill=FONT, tags="watermark", font=("Arial", font_size, "bold"))
    elif option_var.get() == 1:
        x = new_w//2
        y = new_h - new_h + 10 + font_size
        canvas.delete("watermark")
        canvas.create_text(x, y, text=WATERMARK, fill=FONT, tags="watermark", font=("Arial",font_size, "bold"))
    elif option_var.get() == 2:
        x = new_w//2
        y = new_h - 10 - font_size
        canvas.delete("watermark")
        canvas.create_text(x, y, text=WATERMARK, fill=FONT, tags="watermark", font=("Arial", font_size, "bold"))




def watermark_clear():
    canvas.delete("watermark")


# ---------------------------------- UI setting -Main Window ---------------------------------- #
window = tk.Tk()
window.title("Image Watermarking")
window.minsize(width=WINDOW_W, height=WINDOW_H)


# ---------------------------------- UI setting - Field 1: Image ---------------------------------- #
field_img = tk.Frame(window, width=WINDOW_W, height=WINDOW_H, bd=0)
field_img.pack(side="left")
canvas = tk.Canvas(field_img, width=WINDOW_W, height=WINDOW_H, bg=BG_IMG_FIELD)
canvas.pack()


# ---------------------------------- UI setting - Field 2: Manipulate ---------------------------------- #
frame_file = tk.Frame(window)
frame_file.pack(side="right", padx=PADDING, pady=PADDING)
# bd=3 讓button變立體
btn_select = tk.Button(frame_file, text="Select Image", command=select_img, font=BTN_FONT, bd=3, bg=BTN_COLOR, fg=FONT, width=15)
btn_select.pack(pady=3)
btn_delete = tk.Button(frame_file, text="Cancel", command=remove_img, font=BTN_FONT, bd=3, bg="gray", fg=FONT, width=15)
btn_delete.pack(pady=3)
btn_save = tk.Button(frame_file, text="Save To .ps", command=save_to_ps, font=BTN_FONT, bd=3, bg=BTN_COLOR, fg=FONT, width=15)
btn_save.pack(pady=3)
btn_save = tk.Button(frame_file, text="Add Watermark", command=add_watermark, font=BTN_FONT, bd=3, bg=BTN_COLOR, fg=FONT, width=15)
btn_save.pack(pady=3)
entry_watermark = tk.Entry(frame_file)
entry_watermark.pack(pady=3)


# 設定watermark顯示方式
frame_option = tk.Frame(frame_file)
frame_option.pack()
option_var = tk.IntVar()
option1 = tk.Radiobutton(frame_option, text="top", variable=option_var, value=1)
option1.grid(column=1, row=1)
option2 = tk.Radiobutton(frame_option, text="center", variable=option_var, value=0)
option2.grid(column=2, row=1)
option3 = tk.Radiobutton(frame_option, text="bottom", variable=option_var, value=2)
option3.grid(column=3, row=1)

wm_font = tk.Scale(frame_option, label='Font Size', from_=10, to=30, orient=tk.HORIZONTAL, length=150, showvalue=1, tickinterval=20, resolution=1)
wm_font.grid(column=2, row=2)

btn_clear = tk.Button(frame_option, text="Clear All", command=watermark_clear, font=("Arial", 10), bd=3, bg="gray", fg=FONT, width=7)
btn_clear.grid(column=2, row=3)
window.mainloop()
