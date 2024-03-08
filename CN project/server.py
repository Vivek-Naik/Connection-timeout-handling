import socket
import threading
import tkinter as tk
from tkinter import Text, END, Label, Entry, Button
from datetime import datetime, timedelta

class UDPServerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("UDP Server with GUI")
        self.host = "localhost"
        self.port = 5000
        self.timeout_var = tk.StringVar()
        self.timeout_var.set("10")  # Default timeout value
        self.server_socket = None
        self.is_running = False
        self.last_received_time = datetime.now()
        self.restart_button_enabled = tk.BooleanVar()
        self.restart_button_enabled.set(False)

        self.label_host = Label(master, text="Server Host:")
        self.label_host.pack()

        self.label_host_value = Label(master, text=self.host)
        self.label_host_value.pack()

        self.label_port = Label(master, text="Server Port:")
        self.label_port.pack()

        self.label_port_value = Label(master, text=str(self.port))
        self.label_port_value.pack()

        self.label_timeout = Label(master, text="Timeout (seconds):")
        self.label_timeout.pack()

        self.entry_timeout = Entry(master, textvariable=self.timeout_var)
        self.entry_timeout.pack()

        self.text_area = Text(master, height=10, width=40)
        self.text_area.pack()

        self.start_button = Button(master, text="Start Server", command=self.start_server)
        self.start_button.pack()

        self.restart_button = Button(master, text="Restart Server", command=self.restart_server, state=tk.DISABLED)
        self.restart_button.pack()

    def start_server(self):
        if not self.is_running:
            self.is_running = True
            self.host = self.label_host_value.cget("text")
            self.port = int(self.label_port_value.cget("text"))
            timeout_duration = int(self.timeout_var.get())

            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.settimeout(timeout_duration)

            self.text_area.delete(1.0, END)
            self.text_area.insert(tk.END, f"Server is listening on {self.host}:{self.port} with a timeout of {timeout_duration} seconds\n")

            self.restart_button.config(state=tk.DISABLED)  # Disable the restart button

            def receive_messages():
                while self.is_running:
                    try:
                        data, client_address = self.server_socket.recvfrom(1024)
                        message = data.decode('utf-8')
                        self.text_area.insert(tk.END, f"Received message from {client_address}: {message}\n")
                        self.last_received_time = datetime.now()  # Update the last received time
                    except socket.timeout:
                        current_time = datetime.now()
                        time_difference = current_time - self.last_received_time
                        if time_difference.total_seconds() > timeout_duration:
                            self.text_area.insert(tk.END, f"Connection timed out. No messages received in the last {timeout_duration} seconds.\n")
                            self.restart_button.config(state=tk.NORMAL)  # Enable the restart button
                            self.restart_button_enabled.set(True)  # Set the restart flag to True
                            break  # Exit the loop if timeout exceeds
                    except Exception as e:
                        self.text_area.insert(tk.END, f"Error: {str(e)}\n")

            server_thread = threading.Thread(target=receive_messages)
            server_thread.start()

    def restart_server(self):
        if self.restart_button_enabled.get():
            self.is_running = False
            self.server_socket.close()
            self.restart_button.config(state=tk.DISABLED)  # Disable the restart button
            self.restart_button_enabled.set(False)  # Reset the restart flag to False
            self.start_server()  # Restart the server

    def stop_server(self):
        self.is_running = False
        if self.server_socket:
            self.server_socket.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    udp_server_gui = UDPServerGUI(root)
    root.protocol("WM_DELETE_WINDOW", udp_server_gui.stop_server)
    root.mainloop()
