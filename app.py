import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import sys

# ===== exiftoolのパス取得 =====
def get_exiftool_path():
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "exiftool.exe")
    return os.path.join(os.path.dirname(__file__), "exiftool.exe")

# ===== フォルダ選択 =====
def select_source():
    path = filedialog.askdirectory()
    if path:
        src_var.set(path)

def select_output():
    path = filedialog.askdirectory()
    if path:
        out_var.set(path)

def convert_relpath(path):
    return os.path.relpath(path, os.path.dirname(os.path.abspath(__file__)))

# ===== 実行 =====
def run():
    src = src_var.get()
    out = out_var.get()
    date_format = radio_date_format.get()
    copy_or_move = radio_copy_move.get()

    if not src or not out:
        messagebox.showerror("Error", "フォルダを指定してください")
        return

    cmd = [
        get_exiftool_path(),
        "-r", "-P",
        "-ext", "jpg", "-ext", "jpeg", "-ext", "png", "-ext", "heic",
        "-ext", "mp4", "-ext", "mov",
        "-Directory<DateTimeOriginal", "-d", f"{out}{date_format}",
        "-Directory<ModifyDate", "-d", f"{out}{date_format}",
        "-Directory<FileModifyDate", "-d", f"{out}{date_format}",
    ]

    if copy_or_move == "copy":
        cmd.extend(["-o", ".",])

    cmd.extend([src]) # src, src2 TODO: 複数フォルダ対応 これで実行できることは確認済み

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        log_box.insert(tk.END, " ".join(result.args) + "\n" + result.stdout + "\n" + result.stderr)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ===== GUI =====
root = tk.Tk()
root.title("Media Organizer")
root.geometry("400x400")

# source input
src_var = tk.StringVar()
src_frame = ttk.Frame(root)
src_frame.pack(pady=10)
ttk.Entry(src_frame, textvariable=src_var, width=40).pack(side="left")
ttk.Button(src_frame, text="Select Source", command=select_source).pack(side="left")

# out input
out_var = tk.StringVar()
out_frame = ttk.Frame(root)
out_frame.pack(pady=10)
ttk.Entry(out_frame, textvariable=out_var, width=40).pack(side="left")
ttk.Button(out_frame, text="Select Output", command=select_output).pack(side="left")

# date format
radio_date_format = tk.StringVar(value="/%Y/%m")
date_format_frame = ttk.Frame(root)
date_format_frame.pack(pady=10)
ttk.Radiobutton(
    date_format_frame,
    text="/年",
    variable=radio_date_format,
    value="/%Y"
).pack(side="left", padx=10)
ttk.Radiobutton(
    date_format_frame,
    text="/年/月",
    variable=radio_date_format,
    value="/%Y/%m"
).pack(side="left", padx=10)
ttk.Radiobutton(
    date_format_frame,
    text="/年/月/日",
    variable=radio_date_format,
    value="/%Y/%m/%d"
).pack(side="left", padx=10)

# copy / move
radio_copy_move = tk.StringVar(value="copy")
copy_move_frame = ttk.Frame(root)
copy_move_frame.pack(pady=10)
ttk.Radiobutton(
    copy_move_frame,
    text="Copy",
    variable=radio_copy_move,
    value="copy"
).pack(side="left", padx=10)
ttk.Radiobutton(
    copy_move_frame,
    text="Move",
    variable=radio_copy_move,
    value="move"
).pack(side="left", padx=10)

# run button
ttk.Button(root, text="Run", style="Big.TButton", command=run).pack(pady=10)

# log
log_box = tk.Text(root, height=10)
log_box.pack(fill=tk.BOTH, expand=True)

root.mainloop()