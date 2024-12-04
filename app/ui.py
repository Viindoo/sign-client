import threading
import traceback
import logging
import tkinter as tk
from tkinter import messagebox

import version
from app import update
from app.web_api import server_service

root = tk.Tk()
updater = update.Updater({'update_url': 'https://api.github.com/repos/Viindoo/sign-client/releases/latest'})
_logger = logging.getLogger(__name__)


class ViinSignUI:
    def __init__(self, data=None):
        data = data or {}
        self._root = root
        self.window_width = data.get('window_width', 500)
        self.window_height = data.get('window_height', 300)
        self.min_width = data.get('min_width', self.window_width)
        self.min_height = data.get('min_width', self.window_height)

    def _render_window(self):
        screen_width = self._root.winfo_screenwidth()
        root.minsize(self.min_width, self.min_height)

        x = (screen_width // 2) - (self.window_width // 2)
        y = 100
        root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        root.title(f"Viindoo Sign Client")

        # add the label to show version at bottom left
        version_text = f"Version: {version.__version__}"
        version_label = tk.Label(root, text=version_text, font=("Arial", 8), anchor="w")
        version_label.place(relx=0, rely=1, x=10, y=-10, anchor='sw')

        if server_service.is_started:
            text = "API is started"
        else:
            text = "API is stopped"
        label = tk.Label(root, text=text)
        label.pack(pady=20)

        def _toggle_api():
            if server_service.is_started:
                server_service.stop_api_service()
                btn_stop_start.config(text="Start")
                label.config(text="API is stopped")
            else:
                server_service.start_api_service()
                btn_stop_start.config(text="Stop")
                label.config(text="API is started")

        btn_stop_start = tk.Button(
            root, text="Stop" if server_service.is_started else "Start",
            command=_toggle_api
        )
        btn_stop_start.pack(pady=5)

        def _check_for_update():
            try:
                is_need_update, data = updater.get_updating_data()
            except Exception as e:
                messagebox.showerror('error', str(e))
                return

            if not is_need_update:
                messagebox.showinfo('Information', 'You have installed the latest version')
            else:
                message = f"New version: {data['version']}\n" +\
                          f"Description: {data['description']}\n" +\
                          f"Do you want to update?"
                if messagebox.askokcancel("Check for update", message):
                    self._update_with_progress_ui(data)
        btn_check_for_update = tk.Button(text="Check for update", command=_check_for_update)
        btn_check_for_update.pack(pady=5)

    def _update_with_progress_ui(self, updating_data):
        progress_window = tk.Toplevel(self._root)
        progress_window.title("Updating...")
        progress_window.geometry("300x150")

        progress_label = tk.Label(progress_window, text="Updating... Please wait.")
        progress_label.pack(pady=10)

        def update_progress_message(message):
            progress_label.config(text=message)
            progress_window.update_idletasks()

        def run_update():
            try:
                updater.update(updating_data, callback=update_progress_message)
                update_progress_message("Update completed successfully!")
                messagebox.showinfo("Update", "The update has been completed. Please restart this app to finish.")
            except Exception as e:
                update_progress_message(f"Update failed: {str(e)}")
                messagebox.showerror("Update", f"Update failed: {str(e)}")
                _logger.error(traceback.format_exc())
            finally:
                progress_window.destroy()

        threading.Thread(target=run_update).start()

    def start_ui(self, on_close=None):
        self._render_window()
        def close():
            if on_close:
                on_close()
            root.destroy()
        root.protocol('WM_DELETE_WINDOW', close)
        root.mainloop()
