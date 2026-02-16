import socket
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox


class PortScannerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Professional Port Scanner - Kavya Seth")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):

        title = tk.Label(self.root, text="Multi-Threaded TCP Port Scanner",
                         font=("Arial", 16, "bold"))
        title.pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Target IP / Host:").grid(row=0, column=0, padx=5)
        self.target_entry = tk.Entry(frame, width=20)
        self.target_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Start Port:").grid(row=0, column=2, padx=5)
        self.start_port_entry = tk.Entry(frame, width=10)
        self.start_port_entry.grid(row=0, column=3, padx=5)

        tk.Label(frame, text="End Port:").grid(row=0, column=4, padx=5)
        self.end_port_entry = tk.Entry(frame, width=10)
        self.end_port_entry.grid(row=0, column=5, padx=5)

        scan_button = tk.Button(self.root, text="Start Scan",
                                command=self.start_scan,
                                bg="black", fg="white", width=15)
        scan_button.pack(pady=10)

        self.result_box = tk.Text(self.root, height=18, width=85)
        self.result_box.pack()

        scrollbar = ttk.Scrollbar(self.root, command=self.result_box.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_box.config(yscrollcommand=scrollbar.set)

    def scan_port(self, target, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((target, port))
            if result == 0:
                self.result_box.insert(tk.END, f"[OPEN] Port {port}\n")
            s.close()
        except:
            pass

    def start_scan(self):

        target_input = self.target_entry.get()
        start_port = self.start_port_entry.get()
        end_port = self.end_port_entry.get()

        if not target_input or not start_port or not end_port:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            target = socket.gethostbyname(target_input)
            start_port = int(start_port)
            end_port = int(end_port)
        except:
            messagebox.showerror("Error", "Invalid input.")
            return

        self.result_box.delete(1.0, tk.END)
        self.result_box.insert(tk.END, f"Scanning {target}...\n\n")

        start_time = time.time()

        def run_scan():
            for port in range(start_port, end_port + 1):
                threading.Thread(target=self.scan_port,
                                 args=(target, port)).start()

            end_time = time.time()
            self.result_box.insert(tk.END,
                                   f"\nScan Completed in {end_time - start_time:.2f} seconds\n")

        threading.Thread(target=run_scan).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = PortScannerGUI(root)
    root.mainloop()
