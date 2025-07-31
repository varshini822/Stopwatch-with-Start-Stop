import tkinter as tk
from tkinter import ttk, messagebox
import time
import platform

if platform.system() == "Windows":
    import winsound

class EnhancedStopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⏱️ Enhanced Stopwatch")
        self.root.geometry("500x520")
        self.root.resizable(False, False)

        self.is_dark = False
        self.running = False
        self.start_time = 0
        self.elapsed = 0
        self.laps = []

        self.build_ui()
        self.apply_theme()

    def build_ui(self):
        self.style = ttk.Style(self.root)
        self.style.configure("TButton", font=("Segoe UI", 12), padding=6)

        # Header
        self.title_label = tk.Label(self.root, text="⏱️ Stopwatch", font=("Arial", 26, "bold"))
        self.title_label.pack(pady=10)

        # Timer Display
        self.time_display = tk.Label(self.root, text="00:00:00.00", font=("Courier New", 36), width=15)
        self.time_display.pack(pady=10)

        # Button Frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.start_btn = ttk.Button(btn_frame, text="▶ Start", command=self.start)
        self.start_btn.grid(row=0, column=0, padx=8)

        self.stop_btn = ttk.Button(btn_frame, text="⏹ Stop", command=self.stop, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=8)

        self.reset_btn = ttk.Button(btn_frame, text="🔁 Reset", command=self.reset, state="disabled")
        self.reset_btn.grid(row=0, column=2, padx=8)

        self.lap_btn = ttk.Button(btn_frame, text="📍 Lap", command=self.save_lap, state="disabled")
        self.lap_btn.grid(row=0, column=3, padx=8)

        # Lap Listbox
        lap_frame = tk.Frame(self.root)
        lap_frame.pack(pady=10)
        self.lap_box = tk.Listbox(lap_frame, font=("Consolas", 12), width=45, height=8, bd=2, relief=tk.GROOVE)
        self.lap_box.pack()

        # Theme toggle
        self.theme_btn = ttk.Button(self.root, text="🌙 Dark Mode", command=self.toggle_theme)
        self.theme_btn.pack(pady=10)

        # Footer
        self.footer_label = tk.Label(self.root, text="Made with 💖 in Python", font=("Arial", 10))
        self.footer_label.pack(side=tk.BOTTOM, pady=5)

    def update_timer(self):
        if self.running:
            now = time.time()
            elapsed_time = now - self.start_time + self.elapsed
            mins, secs = divmod(elapsed_time, 60)
            hours, mins = divmod(mins, 60)
            ms = int((elapsed_time - int(elapsed_time)) * 100)
            time_str = f"{int(hours):02}:{int(mins):02}:{int(secs):02}.{ms:02}"
            self.time_display.config(text=time_str)
            self.root.after(50, self.update_timer)

    def start(self):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.update_timer()
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
            self.reset_btn.config(state="normal")
            self.lap_btn.config(state="normal")

    def stop(self):
        if self.running:
            self.running = False
            self.elapsed += time.time() - self.start_time
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            self.lap_btn.config(state="disabled")
            self.play_beep()

    def reset(self):
        if not self.running:
            self.elapsed = 0
            self.time_display.config(text="00:00:00.00")
            self.lap_box.delete(0, tk.END)
            self.laps.clear()
            self.reset_btn.config(state="disabled")

    def save_lap(self):
        now = time.time()
        elapsed_time = now - self.start_time + self.elapsed
        mins, secs = divmod(elapsed_time, 60)
        hours, mins = divmod(mins, 60)
        ms = int((elapsed_time - int(elapsed_time)) * 100)
        time_str = f"{int(hours):02}:{int(mins):02}:{int(secs):02}.{ms:02}"
        self.laps.append(time_str)
        self.lap_box.insert(tk.END, f"Lap {len(self.laps)} — {time_str}")
        self.lap_box.insert(tk.END, "-"*40)

        # Optional: Save to a file
        # with open("laps.txt", "a") as file:
        #     file.write(f"Lap {len(self.laps)} - {time_str}\n")

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark:
            bg = "#2e2e2e"
            fg = "#f0f0f0"
            self.root.configure(bg=bg)
            self.title_label.config(bg=bg, fg=fg)
            self.time_display.config(bg="#1c1c1c", fg="#00ffcc")
            self.lap_box.config(bg="#1a1a1a", fg="#0f0")
            self.footer_label.config(bg=bg, fg="#888")
            self.theme_btn.config(text="☀️ Light Mode")
        else:
            bg = "#f0f8ff"
            fg = "#000"
            self.root.configure(bg=bg)
            self.title_label.config(bg=bg, fg=fg)
            self.time_display.config(bg=bg, fg="#000080")
            self.lap_box.config(bg="#fff", fg="#000")
            self.footer_label.config(bg=bg, fg="#444")
            self.theme_btn.config(text="🌙 Dark Mode")

    def play_beep(self):
        try:
            if platform.system() == "Windows":
                winsound.Beep(1000, 200)
            else:
                self.root.bell()
        except:
            pass

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedStopwatchApp(root)
    root.mainloop()
