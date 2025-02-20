'''
Python version: 3.10.12
serial version:     3.5
tkinter version:    8.6
csv version:        1.0
'''
import serial
import tkinter as tk
from tkinter import filedialog, messagebox
import csv
from serial.tools import list_ports

# Inisialisasi koneksi serial dengan Arduino
ser = None  # Global variable untuk koneksi serial
save_path = None  # Global variable untuk menyimpan lokasi penyimpanan file

def connect_serial(port):
    """
    Menghubungkan ke port serial yang dipilih oleh pengguna.
    
    Args:
    port (str): Nama port serial yang dipilih.
    
    Returns:
    None
    """
    global ser
    ser = serial.Serial(port, 9600)
    ser.flush()

def start_measurement():
    """
    Memulai pengukuran dengan mengirimkan kondisi dan durasi ke Arduino,
    lalu membaca data dari serial dan menyimpannya ke file CSV.
    
    Returns:
    None
    """
    global save_path  # Deklarasi global save_path di sini
    if ser:
        if save_path is None:
            messagebox.showerror("Error", "Pilih lokasi penyimpanan terlebih dahulu!")
            return
        kondisi = int(condition_var.get())
        durDel = int(del_duration_entry.get())
        durSamp = int(samp_duration_entry.get())
        durPur = int(pur_duration_entry.get())
        
        # Kirim kondisi dan durasi ke Arduino
        ser.write(f"{kondisi}\n".encode())
        ser.write(f"{durDel}\n".encode())
        ser.write(f"{durSamp}\n".encode())
        ser.write(f"{durPur}\n".encode())
        
        # Baca data dari serial dan simpan ke file CSV
        with open(save_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            header = ['MQ2', 'MQ3', 'MQ4', 'MQ5', 'MQ6', 'MQ7', 'MQ8', 'MQ9', 'MQ135', 'Temperature', 'Humidity']
            writer.writerow(header)
            
            # Variabel untuk menandai pengukuran selesai
            measurement_finished = False
            
            # Jumlah data maksimum yang ingin Anda simpan
            max_data_count = (durDel + durSamp + durPur) * 10  # Atur sesuai kebutuhan Anda
            
            # Hitung jumlah data yang sudah disimpan
            data_count = 0
            
            # Loop terus menerus sampai pengukuran selesai
            while not measurement_finished:
                line = ser.readline().decode().strip()
                print(line)
                values = line.split(',')
                writer.writerow(values)
                
                # Periksa apakah sudah mencapai jumlah data maksimum
                data_count += 1
                if data_count >= max_data_count:
                    measurement_finished = True
            
            # Setelah pengukuran selesai
            ser.close()
            messagebox.showinfo("Info", "Data sudah disimpan")
            
            # Reset GUI untuk input baru
            del_duration_entry.delete(0, tk.END)
            samp_duration_entry.delete(0, tk.END)
            pur_duration_entry.delete(0, tk.END)
            
            # Reset path penyimpanan
            save_path = None  # Mengatur save_path ke None setelah penggunaan

def select_save_location():
    """
    Memilih lokasi penyimpanan file CSV.
    
    Returns:
    None
    """
    global save_path
    save_path = filedialog.asksaveasfilename(defaultextension=".csv")
    if save_path:
        messagebox.showinfo("Info", f"Lokasi penyimpanan file dipilih: {save_path}")

def clean_enose():
    """
    Membersihkan E-Nose dengan mengirimkan perintah ke Arduino.
    
    Returns:
    None
    """
    if ser:
        kondisi = 1
        ser.write(f"{kondisi}\n".encode())
        messagebox.showinfo("Info", "E-Nose sudah dibersihkan")
    ser.close()

def quit_application():
    """
    Menutup aplikasi dan memutuskan koneksi serial.
    
    Returns:
    None
    """
    if ser:
        ser.close()
    root.destroy()

def update_ports():
    """
    Memperbarui daftar port serial yang tersedia.
    
    Returns:
    None
    """
    ports = list_ports.comports()
    port_list = [port.device for port in ports]
    port_var.set(port_list[0] if port_list else '')
    port_menu['menu'].delete(0, 'end')
    for port in port_list:
        port_menu['menu'].add_command(label=port, command=tk._setit(port_var, port))

# GUI setup
root = tk.Tk()
root.title("Electronic Nose GUI")

# Port selection
port_label = tk.Label(root, text="Pilih Port:")
port_label.grid(row=0, column=0, sticky="w")

port_var = tk.StringVar()
port_menu = tk.OptionMenu(root, port_var, '')
port_menu.grid(row=0, column=1, sticky="w")

update_ports_button = tk.Button(root, text="Update Ports", command=update_ports)
update_ports_button.grid(row=0, column=2)

# Condition selection
condition_label = tk.Label(root, text="Pilih Kondisi:")
condition_label.grid(row=1, column=0, sticky="w")

condition_var = tk.StringVar()
condition_dropdown = tk.OptionMenu(root, condition_var, "0", "1")
condition_dropdown.grid(row=1, column=1, sticky="w")

# Duration inputs
del_duration_label = tk.Label(root, text="Durasi Baseline (detik):")
del_duration_label.grid(row=2, column=0, sticky="w")

del_duration_entry = tk.Entry(root)
del_duration_entry.grid(row=2, column=1, sticky="w")

samp_duration_label = tk.Label(root, text="Durasi Sampel (detik):")
samp_duration_label.grid(row=3, column=0, sticky="w")

samp_duration_entry = tk.Entry(root)
samp_duration_entry.grid(row=3, column=1, sticky="w")

pur_duration_label = tk.Label(root, text="Durasi Pengosongan (detik):")
pur_duration_label.grid(row=4, column=0, sticky="w")

pur_duration_entry = tk.Entry(root)
pur_duration_entry.grid(row=4, column=1, sticky="w")

# Buttons
select_save_button = tk.Button(root, text="Pilih Lokasi Simpan", command=select_save_location)
select_save_button.grid(row=5, column=0, columnspan=2, pady=10)

start_button = tk.Button(root, text="Start", command=start_measurement)
start_button.grid(row=6, column=0, columnspan=2, pady=10)

clean_button = tk.Button(root, text="Clean E-Nose", command=clean_enose)
clean_button.grid(row=7, column=0, columnspan=2, pady=10)

quit_button = tk.Button(root, text="Quit", command=quit_application)
quit_button.grid(row=8, column=0, columnspan=2)

# Connect to serial port
connect_serial_button = tk.Button(root, text="Connect", command=lambda: connect_serial(port_var.get()))
connect_serial_button.grid(row=0, column=3)

# Update port list on startup
update_ports()

root.mainloop()