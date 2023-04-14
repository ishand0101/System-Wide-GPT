import requests
import keyboard as kb
import clipboard
import requests
import time
from urllib.parse import quote
import pygetwindow as gw
import tkinter as tk

highlighted_text = ""

def get_active_window_title():
    active_window = gw.getActiveWindow()
    return active_window.title


def use_text():
    active_window_title = get_active_window_title()
    active_window = gw.getWindowsWithTitle(active_window_title)[0]
    active_window.restore()
    time.sleep(.2)
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


hotkey_enabled = {
    'two_emojis': True,
    'replace_line': True,
    'multiple_questions': True,
    # Add other hotkeys here
}


# Functions to enable and disable hotkeys
def enable_hotkey(hotkey_name):
    if hotkey_name == 'two_emojis':
        kb.add_hotkey('ctrl + alt + shift + r', two_emojis)
    elif hotkey_name == 'replace_line':
        kb.add_hotkey('ctrl + alt + shift + e', replace_line)
    elif hotkey_name == 'multiple_questions':
        kb.add_hotkey('ctrl + alt + shift + q', send_text_mq)
        kb.add_hotkey('ctrl + alt + shift + w', send_query_mq)
    # Add other hotkey enable conditions here


def disable_hotkey(hotkey_name):
    if hotkey_name == 'two_emojis':
        kb.remove_hotkey('ctrl + alt + shift + r')
    elif hotkey_name == 'replace_line':
        kb.remove_hotkey('ctrl + alt + shift + e')
    elif hotkey_name == 'multiple_questions':
        kb.remove_hotkey('ctrl + alt + shift + q')
        kb.remove_hotkey('ctrl + alt + shift + w')
    # Add other hotkey disable conditions here


def toggle_hotkey(hotkey_name):
    if hotkey_enabled[hotkey_name]:
        disable_hotkey(hotkey_name)
    else:
        enable_hotkey(hotkey_name)
    hotkey_enabled[hotkey_name] = not hotkey_enabled[hotkey_name]
    

# Initialize the hotkeys
for hotkey_name in hotkey_enabled:
    if hotkey_enabled[hotkey_name]:
        enable_hotkey(hotkey_name)

window = tk.Tk()
window.title("AI")

btn_two_emojis = tk.Button(window, text="Toggle two_emojis hotkey", command=lambda: toggle_hotkey('two_emojis'))
btn_replace_line = tk.Button(window, text="Toggle replace_line hotkey", command=lambda: toggle_hotkey('replace_line'))
btn_multiple_questions = tk.Button(window, text="Toggle multiple_questions hotkeys", command=lambda: toggle_hotkey('multiple_questions'))

btn_two_emojis.pack()
btn_replace_line.pack()
btn_multiple_questions.pack()

window.mainloop()