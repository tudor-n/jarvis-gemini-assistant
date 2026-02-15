import time, os, random, threading, psutil, re
import customtkinter as ctk
import tkinter as tk
from voice_input import VoiceInput
from voice_output import VoiceOutput
from ai_brain import AIBrain
from project_manager import ProjectManager
from dotenv import load_dotenv
from spotify_control import SpotifyControl
import sys
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class JARVIS:
    def __init__(self, gui_update_callback, on_speak_start, on_speak_stop, clear_console_callback):
        load_dotenv(get_resource_path(".env"))
        self.pm = ProjectManager()
        self.spotify = SpotifyControl()
        self.gui_callback = gui_update_callback
        self.on_speak_start = on_speak_start
        self.on_speak_stop = on_speak_stop
        self.clear_func = clear_console_callback 
        
        pico_api_key = os.getenv("PICO_API_KEY")
        if not pico_api_key: raise ValueError("PICO_API_KEY not found.")
            
        self.voice_in = VoiceInput(pico_api_key.strip())
        self.voice_out = VoiceOutput()
        
        self.follow_up_duration, self.idle_timeout = 12.0, 30.0
        self.last_interaction = self.last_idle_action = time.time()
        
        tools = [
            self.pm.create_project, self.pm.list_projects, self.pm.get_project,
            self.pm.create_task, self.pm.list_tasks, self.pm.complete_task,
            self.pm.delete_project, self.pm.add_characteristic, self.pm.get_characteristics,
            self.pm.delete_task, self.pm.add_description, self.pm.update_task_priority,
            self.pm.add_category, self.pm.delete_characteristic,
            self.clear_console_tool,
            self.spotify.play_song, 
            self.spotify.pause_music, 
            self.spotify.next_track
        ]
        
        self.brain = AIBrain(tools_list=tools)
        self.running = True

    def log(self, message): self.gui_callback(message)

    def _clean_text_for_speech(self, text):
        text = text.replace("*", "")
        text = re.sub(r'\bIII\b', '3', text)
        text = re.sub(r'\bII\b', '2', text)
        text = re.sub(r'\bIV\b', '4', text)
        text = text.replace("_", " ").replace("#", "")
        return text

    def speak_and_animate(self, text):
        if not text: return
        clean_text = self._clean_text_for_speech(text)
        self.on_speak_start()
        self.voice_out.speak(clean_text)
        self.on_speak_stop()

    def clear_console_tool(self):
        self.clear_func()
        return "Console cleared, Sir."

    def run(self):
        self.log("SYSTEM | INITIALIZING INTERFACE")
        time.sleep(1.2)
        self.speak_and_animate("JARVIS online. Good to see you, Sir.")
        self.log("JARVIS | Good to see you, Sir.")
        
        while self.running:
            current_time = time.time()
            try:
                if (current_time - self.last_idle_action > self.idle_timeout):
                    self.last_idle_action = time.time() 
                    thought = self.brain.think("SYSTEM: The cooldown has elapsed, the user isn't interacting directly anymore so you should: Give witty remarks or suggestions, you can use the projects/tasks in the database for them( don't use random projects, only use what's in the database). (Plain text, if listing: no markdown or roman numerals.)")
                    self.log(f"JARVIS | {thought}") 
                    self.speak_and_animate(thought)
                
                if self.voice_in.wait_for_wake_word():
                    self.log("SYSTEM | LISTENING")
                    self.speak_and_animate("I'm here, Sir.")
                    
                    while self.running:
                        cmd = self.voice_in.listen_for_command()
                        
                        if cmd:
                            self.process_command(cmd)
                            self.last_interaction = time.time()
                            self.last_idle_action = time.time()
                        else:
                            if (time.time() - self.last_interaction > self.follow_up_duration):
                                self.log("SYSTEM | GOING TO SLEEP")
                                break 
                                
            except Exception as e:
                self.log(f"ERROR | {str(e)}")
            
            time.sleep(0.05)

    def process_command(self, command):
        self.log(f"USER | {command}")
        prompt = f"USER_REQUEST: {command}. (Reply in plain text, when listing project things use IDs not numbers and not roman numerals and no asterisks. You can also add some flair: funny comments, preferences, or general personality.)"
        response = self.brain.think(prompt)
        self.log(f"JARVIS | {response}") 
        self.speak_and_animate(response)

class JarvisGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.bg_color = "#1A1A1A" 
        self.geometry("400x680") 
        self.overrideredirect(True)
        self.attributes("-alpha", 0.0, "-topmost", True)
        self.configure(fg_color=self.bg_color)
        
        icon_path = get_resource_path("jarvisicon.ico")
        if os.path.exists(icon_path):
             self.after(200, lambda: self.iconbitmap(icon_path))

        
        self.is_speaking, self.orb_radius, self.pulse_growing = False, 0, True
        self.is_booting = True 

        self.history = []
        self.history_index = -1

        self.setup_ui()
        
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.do_move)
        self.bind("<Enter>", self.on_hover_enter)
        self.bind("<Leave>", self.on_hover_leave)

        self.draw_orb()
        self.after(500, self.boot_sequence)
        self.update_status_bar()

        self.jarvis = JARVIS(self.update_console, self.start_orb_pulse, self.stop_orb_pulse, self.clear_console)
        threading.Thread(target=self.jarvis.run, daemon=True).start()

    def clear_console(self):
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")
        self.update_console("SYSTEM | CONSOLE PURGED. READY.")

    def navigate_history(self, event):
        if not self.history: return
        if event.keysym == "Up":
            self.history_index = min(self.history_index + 1, len(self.history) - 1)
        elif event.keysym == "Down":
            self.history_index = max(self.history_index - 1, -1)
        
        self.input_entry.delete(0, "end")
        if self.history_index != -1:
            self.input_entry.insert(0, self.history[len(self.history) - 1 - self.history_index])

    def setup_ui(self):
        self.close_btn = ctk.CTkButton(self, text="×", width=25, height=25, fg_color="transparent", 
                                       text_color="#555555", hover_color="#A12525", command=self.quit_app)
        self.close_btn.place(x=370, y=5)

        self.min_btn = ctk.CTkButton(self, text="—", width=25, height=25, fg_color="transparent", 
                                     text_color="#555555", hover_color="#444444", command=self.minimize_app)
        self.min_btn.place(x=340, y=5)

        self.status_bar = ctk.CTkLabel(self, text="INITIALIZING...", font=("Verdana", 10), text_color="#008B8B")
        self.status_bar.pack(side="bottom", fill="x", pady=(0, 5))

        self.orb_canvas = tk.Canvas(self, width=100, height=100, bg=self.bg_color, highlightthickness=0)
        self.orb_canvas.pack(pady=(35, 0))

        self.system_label = ctk.CTkLabel(self, text="", font=("Orbitron", 20, "bold"), text_color="#00D4FF")
        self.system_label.pack(pady=(2, 5))

        self.input_entry = ctk.CTkEntry(self, placeholder_text="Command...", width=360, height=38, 
                                        fg_color="#0D0D0D", border_color="#00D4FF", 
                                        font=("Segoe UI Semibold", 13), text_color="#FFFFFF")
        self.input_entry._entry.configure(insertwidth=0, insertontime=0, selectbackground="#0D0D0D", selectforeground="#00D4FF")
        self.input_entry.pack(side="bottom", pady=(0, 15))
        
        self.input_entry.bind("<Return>", lambda e: self.send_text_command())
        self.input_entry.bind("<Up>", self.navigate_history)
        self.input_entry.bind("<Down>", self.navigate_history)

        self.console = ctk.CTkTextbox(self, width=360, fg_color="#0D0D0D", border_width=0, 
                                      font=("Segoe UI Semibold", 12), wrap="word")
        self.console._textbox.configure(insertwidth=0, insertontime=0, selectbackground="#0D0D0D", selectforeground="#00D4FF")
        self.console.pack(padx=20, pady=5, fill="both", expand=True)
        
        self.console.tag_config("user_label", foreground="#E0E0E0") 
        self.console.tag_config("jarvis_label", foreground="#00D4FF") 
        self.console.tag_config("system_label", foreground="#008B8B") 

    def on_hover_enter(self, event):
        self.attributes("-alpha", 0.95)
        if not self.is_booting: self.trigger_glitch(iterations=3)

    def on_hover_leave(self, event): self.attributes("-alpha", 0.70)

    def trigger_glitch(self, iterations=3):
        if iterations <= 0:
            self.system_label.configure(text="J.A.R.V.I.S.")
            return
        chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        scrambled = "".join(random.choice(chars) for _ in range(11))
        self.system_label.configure(text=scrambled)
        self.after(30, lambda: self.trigger_glitch(iterations - 1))

    def boot_sequence(self):
        curr_alpha = self.attributes("-alpha")
        if curr_alpha < 0.70:
            self.attributes("-alpha", curr_alpha + 0.05)
            self.after(40, self.boot_sequence)
            return
        self.orb_radius = 15
        self.draw_orb()
        full_text = "J.A.R.V.I.S."
        def type_char(i=0):
            if i <= len(full_text):
                self.system_label.configure(text=full_text[:i])
                self.after(80, lambda: type_char(i+1))
            else: self.is_booting = False 
        type_char()

    def update_status_bar(self):
        cpu, ram = psutil.cpu_percent(), psutil.virtual_memory().percent
        self.status_bar.configure(text=f"CPU {cpu}% | RAM {ram}% | LINK ACTIVE")
        self.after(2000, self.update_status_bar)

    def start_move(self, event): self.x, self.y = event.x, event.y
    def do_move(self, event):
        x, y = self.winfo_x() + (event.x - self.x), self.winfo_y() + (event.y - self.y)
        self.geometry(f"+{x}+{y}")

    def send_text_command(self):
        text = self.input_entry.get()
        if text.strip():
            self.history.append(text)
            self.history_index = -1
            self.input_entry.delete(0, "end")
            current_time = time.time()
            self.jarvis.last_interaction = self.jarvis.last_idle_action = current_time
            threading.Thread(target=self.jarvis.process_command, args=(text,), daemon=True).start()

    def update_console(self, message): self.after(0, lambda: self._safe_update(message))
    
    def _safe_update(self, message): 
        self.console.configure(state="normal")
        if "USER |" in message: self.console.insert("end", f"\n{message}\n", "user_label")
        elif "JARVIS |" in message: self.console.insert("end", f"\n{message}\n", "jarvis_label")
        else: self.console.insert("end", f"\n{message}\n", "system_label")
        self.console.see("end")
        self.console.configure(state="disabled")

    def draw_orb(self):
        self.orb_canvas.delete("all")
        cx, cy = 50, 50
        self.orb_canvas.create_oval(cx-self.orb_radius, cy-self.orb_radius, cx+self.orb_radius, cy+self.orb_radius, outline="#00D4FF", width=1.5)
        r_inner = self.orb_radius * 0.5
        self.orb_canvas.create_oval(cx-r_inner, cy-r_inner, cx+r_inner, cy+r_inner, fill="#00D4FF", outline="#00D4FF")

    def animate_pulse(self):
        if not self.is_speaking: self.orb_radius = 15; self.draw_orb(); return
        self.orb_radius += 1.5 if self.pulse_growing else -1.5
        if self.orb_radius > 35: self.pulse_growing = False
        elif self.orb_radius < 15: self.pulse_growing = True
        self.draw_orb()
        self.after(30, self.animate_pulse)

    def start_orb_pulse(self):
        if not self.is_speaking: self.is_speaking = True; self.animate_pulse()
    def stop_orb_pulse(self): self.is_speaking = False

    def quit_app(self): self.jarvis.running = False; self.destroy()
    def minimize_app(self): self.withdraw(); self.after(10, self._set_min)
    def _set_min(self): self.overrideredirect(False); self.iconify(); self.bind("<Map>", self.on_restore)
    def on_restore(self, e):
        if self.state() == 'normal': self.withdraw(); self.overrideredirect(True); self.after(50, self.deiconify); self.unbind("<Map>")

if __name__ == "__main__":
    app = JarvisGUI()
    app.mainloop()