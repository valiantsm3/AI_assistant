import tkinter as tk
from tkinter import scrolledtext, messagebox, Toplevel, Label, Entry, Button
import threading
import sys
from main import main_process, speak  # Import main logic
import pyttsx3
import pywhatkit
from datetime import datetime

# Initialize text-to-speech engine
engine = pyttsx3.init()
assistant_thread = None  # Global thread reference

# GUI Setup
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("500x650")
root.configure(bg="#1e1e1e")  # Dark theme background

# Styling
btn_style = {"font": ("Arial", 12), "bg": "#0078D7", "fg": "white", "width": 25, "pady": 5}
label_style = {"font": ("Arial", 11), "bg": "#1e1e1e", "fg": "white"}
entry_style = {"font": ("Arial", 12), "width": 30, "bg": "#2e2e2e", "fg": "white"}

# Output Box
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, bg="#2e2e2e", fg="white", font=("Arial", 10))
output_box.pack(pady=10)

class RedirectOutput:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        root.after(0, lambda: self.text_widget.insert(tk.END, text))
        root.after(0, lambda: self.text_widget.yview(tk.END))

    def flush(self):
        pass

sys.stdout = RedirectOutput(output_box)

def update_output(text):
    root.after(0, lambda: output_box.insert(tk.END, text + "\n"))
    root.after(0, lambda: output_box.yview(tk.END))

def gui_speak(text):
    update_output("Assistant: " + text)
    if not engine._inLoop:
        speak(text)

def start_assistant():
    global assistant_thread
    if start_assistant.activated:
        return
    start_assistant.activated = True
    assistant_thread = threading.Thread(target=run_assistant)
    assistant_thread.start()

start_assistant.activated = False

def stop_assistant():
    global assistant_thread
    gui_speak("Stopping assistant.")
    start_assistant.activated = False
    if assistant_thread and assistant_thread.is_alive():
        assistant_thread.join(timeout=2)  # Wait for thread to finish
    root.quit()

def run_assistant():
    try:
        main_process()
    except Exception as e:
        root.after(0, lambda: update_output(f"Error: {e}"))

def handle_whatsapp_command():
    def send_whatsapp():
        phone_number = number_entry.get().strip()
        message = message_entry.get().strip()

        if not phone_number.startswith("+"):
            messagebox.showwarning("Input Error", "Please enter a valid number with country code (e.g., +1234567890).")
            return
        if not message:
            messagebox.showwarning("Input Error", "Message cannot be empty!")
            return

        try:
            now = datetime.now()
            hour = now.hour
            minute = now.minute + 1  # Schedule one minute ahead
            if minute >= 60:
                hour += 1
                minute = 0

            try:
                pywhatkit.sendwhatmsg(phone_number, message, time_hour=hour, time_min=minute, wait_time=5, tab_close=True, close_time=30)
                gui_speak(f"WhatsApp message sent to {phone_number}.")
            except Exception as e:
                messagebox.showerror("Error", f"PyWhatKit failed: {e}")
                gui_speak("Failed to send WhatsApp message.")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")
            gui_speak("An unexpected error occurred.")
        finally:
            whatsapp_window.destroy()
            gui_speak("Resuming voice assistant.")
            start_assistant()  # Automatically reactivate the assistant

    whatsapp_window = Toplevel(root)
    whatsapp_window.title("Send WhatsApp Message")
    whatsapp_window.geometry("350x200")
    whatsapp_window.configure(bg="#1e1e1e")
    Label(whatsapp_window, text="Enter recipient's number (with country code):", **label_style).pack()
    number_entry = Entry(whatsapp_window, **entry_style)
    number_entry.pack()
    Label(whatsapp_window, text="Enter your message:", **label_style).pack()
    message_entry = Entry(whatsapp_window, **entry_style)
    message_entry.pack()
    Button(whatsapp_window, text="Send", command=send_whatsapp, **btn_style).pack(pady=10)

# Buttons
start_button = tk.Button(root, text="Start Assistant", command=start_assistant, **btn_style)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Assistant", command=stop_assistant, **btn_style)
stop_button.pack(pady=5)

whatsapp_button = tk.Button(root, text="Send WhatsApp Message", command=handle_whatsapp_command, **btn_style)
whatsapp_button.pack(pady=5)

# Ensure threads stop when GUI is closed
def on_closing():
    stop_assistant()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()