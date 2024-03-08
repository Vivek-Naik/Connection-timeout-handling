import socket
import tkinter as tk
from tkinter import Entry, Button, messagebox
from threading import Thread

class UDPClientGUI:
    def __init__(self, master, server_host, server_port):
        self.master = master
        self.master.title("UDP Client with GUI")
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.timeout_duration = 10  # Set the timeout duration (in seconds)
        
        self.master.geometry("400x200")
        
        self.entry_server_host = Entry(master)
        self.entry_server_host.insert(0, self.server_host)
        self.entry_server_host.grid(row=0, column=1)

        self.label_server_host = tk.Label(master, text="Server Host:")
        self.label_server_host.grid(row=0, column=0)

        self.entry_server_port = Entry(master)
        self.entry_server_port.insert(0, str(self.server_port))
        self.entry_server_port.grid(row=1, column=1)

        self.label_server_port = tk.Label(master, text="Server Port:")
        self.label_server_port.grid(row=1, column=0)

        self.entry_message = Entry(master)
        self.entry_message.grid(row=2, column=1)
        
        self.label_message = tk.Label(master, text="Message:")
        self.label_message.grid(row=2, column=0)

        self.send_button = Button(master, text="Send Message", command=self.send_message)
        self.send_button.grid(row=3, column=1)

        self.quit_button = Button(master, text="Quit", command=self.quit_application)
        self.quit_button.grid(row=4, column=1)

    def send_message(self):
        server_host = self.entry_server_host.get()
        server_port = int(self.entry_server_port.get())
        message = self.entry_message.get()

        try:
            self.client_socket.sendto(message.encode('utf-8'), (server_host, server_port))
            print(f"Message sent to {server_host}:{server_port}: {message}")

            # Start a thread to listen for server response or timeout
            response_thread = Thread(target=self.wait_for_response, args=(server_host, server_port))
            response_thread.start()
        except Exception as e:
            print(f"Error sending message: {e}")

    def wait_for_response(self, server_host, server_port):
        try:
            data, _ = self.client_socket.recvfrom(1024)
            response = data.decode('utf-8')
            print(f"Received response from {server_host}:{server_port}: {response}")
        except socket.timeout:
            messagebox.showinfo("Connection Timeout", "Connection timed out. Server did not respond within the specified time.")
        except Exception as e:
            print(f"Error receiving response: {e}")

    def quit_application(self):
        self.client_socket.close()
        self.master.destroy()

if __name__ == "__main__":
    default_server_host = "localhost"
    default_server_port = 5000

    root = tk.Tk()
    udp_client_gui = UDPClientGUI(root, default_server_host, default_server_port)
    root.mainloop()
