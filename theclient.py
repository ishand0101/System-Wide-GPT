import requests
import keyboard as kb
import clipboard
import requests
import time
from urllib.parse import quote
import pygetwindow as gw
import tkinter as tk
import pystray
from PIL import Image

highlighted_text = ""

def get_active_window_title():
    active_window = gw.getActiveWindow()
    return active_window.title


def use_text():
    active_window_title = get_active_window_title()
    active_window = gw.getWindowsWithTitle(active_window_title)[0]
    active_window.restore()
    time.sleep(0.2)
    clipboard.copy(" ")
    time.sleep(0.2)
    kb.press('shift')
    kb.press('home')
    kb.release('home')
    kb.release('shift')
    time.sleep(0.1)
    kb.press('ctrl')
    kb.press('c')
    kb.release('c')
    kb.release('ctrl')
    time.sleep(0.5)
    copied_text = clipboard.paste()
    time.sleep(0.1)
    print(copied_text)
    return copied_text


def two_emojis():
    stringquery = use_text()
    encoded_query = quote(stringquery)
    response = requests.get("http://127.0.0.1:5000/generate-emojis/" + encoded_query)
    full_return = response.text
    clipboard.copy(" ") 
    time.sleep(0.1)  
    clipboard.copy(full_return)
    time.sleep(0.5)
    active_window_title = get_active_window_title()
    active_window = gw.getWindowsWithTitle(active_window_title)[0]
    active_window.restore()
    time.sleep(0.5)
    kb.press('ctrl')
    kb.press('v')
    kb.release('v')
    kb.release('ctrl')
    time.sleep(0.5)
    print(full_return)
    clipboard.copy(" ")
    time.sleep(0.2)


def replace_line():
    stringquery = use_text()
    print(f"stringquery: {stringquery}")
    encoded_query = quote(stringquery)
    response = requests.get("http://127.0.0.1:5000/generate-text/" + encoded_query)
    response_text = response.text
    clipboard.copy(" ") 
    time.sleep(0.2) 
    clipboard.copy(response_text)
    time.sleep(0.5)
    kb.press('ctrl')
    kb.press('v')
    kb.release('v')
    kb.release('ctrl')
    time.sleep(0.5)
    clipboard.copy(" ")
    time.sleep(0.2)


def send_text_mq():
    global highlighted_text
    highlighted_text = use_text()
    print(f"Text saved: {highlighted_text}")


def send_query_mq():
    global highlighted_text
    current_highlighted = use_text()
    string_query_combined = highlighted_text + "(THIS IS THE BARRER BETWEEN TEXT FOR CONTEXT AND THE QUERY)" + current_highlighted
    encoded_query = quote(string_query_combined)
    response = requests.get("http://127.0.0.1:5000/generate-multiple-response/" + encoded_query)
    response_text = response.text
    clipboard.copy(" ") 
    time.sleep(0.2) 
    clipboard.copy(response_text)
    time.sleep(0.5)
    kb.press('ctrl')
    kb.press('v')
    kb.release('v')
    kb.release('ctrl')
    time.sleep(0.5)
    clipboard.copy(" ")
    time.sleep(0.2)


hotkey_disabled_start = {
    'two_emojis': False,
    'replace_line': False,
    'multiple_questions': False,
    # Add other hotkeys here
}


# Functions to enable and disable hotkeys
def enable_hotkey(hotkey_name):
    if hotkey_name == 'two_emojis':
        kb.add_hotkey('ctrl + alt + shift + e', two_emojis)
    elif hotkey_name == 'replace_line':
        kb.add_hotkey('ctrl + alt + shift + r', replace_line)
    elif hotkey_name == 'multiple_questions':
        kb.add_hotkey('ctrl + alt + shift + q', send_text_mq)
        kb.add_hotkey('ctrl + alt + shift + a', send_query_mq)
    # Add other hotkey enable conditions here


def disable_hotkey(hotkey_name):
    if hotkey_name == 'two_emojis':
        kb.remove_hotkey('ctrl + alt + shift + e')
    elif hotkey_name == 'replace_line':
        kb.remove_hotkey('ctrl + alt + shift + r')
    elif hotkey_name == 'multiple_questions':
        kb.remove_hotkey('ctrl + alt + shift + q')
        kb.remove_hotkey('ctrl + alt + shift + a')
    # Add other hotkey disable conditions here


def toggle_hotkey(hotkey_name):
    if hotkey_disabled_start[hotkey_name]:
        enable_hotkey(hotkey_name)
    else:
        disable_hotkey(hotkey_name)
    hotkey_disabled_start[hotkey_name] = not hotkey_disabled_start[hotkey_name]
    
# Initialize the hotkeys
for hotkey_name in hotkey_disabled_start:
    if not hotkey_disabled_start[hotkey_name]:
        enable_hotkey(hotkey_name)

window = tk.Tk()
window.title("AI")
window.iconbitmap("C:\\Users\\Ishan\\Desktop\\system-wide gpt\\unknown(2).ico")

label = tk.Label(window, text="Hotkey Controller", font=("Arial", 16))
label.pack(pady=10)

btn_two_emojis = tk.Button(window, text="Toggle two_emojis hotkey", command=lambda: toggle_hotkey('two_emojis'))
btn_replace_line = tk.Button(window, text="Toggle replace_line hotkey", command=lambda: toggle_hotkey('replace_line'))
btn_multiple_questions = tk.Button(window, text="Toggle multiple_questions hotkeys", command=lambda: toggle_hotkey('multiple_questions'))

btn_two_emojis.pack(pady=5)
btn_replace_line.pack(pady=5)
btn_multiple_questions.pack(pady=5)

label_textbox = tk.Label(window, text="Paste text to save for later:", font=("Arial", 12))
label_textbox.pack(pady=5)
text_box = tk.Text(window, wrap=tk.WORD, height=10, width=40)
text_box.pack(pady=5)

def create_tray_icon():
    icon = Image.open("C:\\Users\\Ishan\\Desktop\\system-wide gpt\\unknown(2).png")

    def on_activate(icon, item):
        toggle_hotkey(item.text)
        item.checked = not item.checked

    def show_window(icon, item):
        icon.stop()  # Stop the tray icon
        window.deiconify()  # Show the Tkinter window

    menu_items = (
        pystray.MenuItem('Toggle two_emojis hotkey', on_activate, checked=lambda item: hotkey_disabled_start['two_emojis']),
        pystray.MenuItem('Toggle replace_line hotkey', on_activate, checked=lambda item: hotkey_disabled_start['replace_line']),
        pystray.MenuItem('Toggle multiple_questions hotkeys', on_activate, checked=lambda item: hotkey_disabled_start['multiple_questions']),
        pystray.MenuItem('Show Window', show_window),
        pystray.MenuItem('Exit', lambda icon, item: icon.stop())
    )
    tray_icon = pystray.Icon("name", icon, "AI Hotkey Controller", menu_items)
    tray_icon.run()    

def on_close():
    window.iconify()  # Use iconify instead of withdraw
    create_tray_icon()

def show_window():
    window.deiconify()
    
window.protocol("WM_DELETE_WINDOW", on_close)

window.mainloop()