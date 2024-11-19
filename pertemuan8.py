from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk
import sqlite3

# Fungsi untuk membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS nilai_siswa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_siswa TEXT,
        biologi INTEGER,
        fisika INTEGER,
        inggris INTEGER,
        prediksi_fakultas TEXT)''')
    conn.commit()
    conn.close()

def fetch_data():
    try:
        conn = sqlite3.connect('nilai_siswa.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nilai_siswa")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Kesalahan: {e}")
        return []

def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()
    conn.close()

def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()
    conn.close()

def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Diketahui"

def submit():
    try:
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")
        if not (0 <= biologi <= 100) or not (0 <= fisika <= 100) or not (0 <= inggris <= 100):
            raise ValueError("Nilai harus antara 0 dan 100.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        save_to_database(nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")

def update():
    try:
        if not selected_record_id.get():
            raise ValueError("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")
        if not (0 <= biologi <= 100) or not (0 <= fisika <= 100) or not (0 <= inggris <= 100):
            raise ValueError("Nilai harus antara 0 dan 100.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def delete():
    try:
        if not selected_record_id.get():
            raise ValueError("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())
        delete_database(record_id)
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

def populate_table():
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_data():
        tree.insert('', 'end', values=row)

def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()
        if not selected_item:
            raise IndexError("Tidak ada data yang dipilih.")
        
        selected_row = tree.item(selected_item[0])['values']
        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")
root.configure(bg="#FFC0CB")  # Warna pink

# Variabel tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()

style = ttk.Style()
style.configure("Treeview", background="#FFE4E1", foreground="black", fieldbackground="#FFC0CB")
style.configure("Treeview.Heading", background="#FF69B4", foreground="white")

Label(root, text="Nama Siswa", bg="#FFC0CB").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi", bg="#FFC0CB").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika", bg="#FFC0CB").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris", bg="#FFC0CB").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

Button(root, text="Add", bg="#FF69B4", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", bg="#FF69B4", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", bg="#FF69B4", command=delete).grid(row=4, column=2, pady=10)

columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center')

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

populate_table()

root.mainloop()
