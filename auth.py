import sqlite3
import hashlib
from tkinter import *
from tkinter import messagebox, ttk
from interface import show_main_window
from main import init_db  # Импортируем функцию инициализации БД

# Инициализируем БД при запуске
init_db()

# Подключение к БД (живет пока работает приложение)
conn = sqlite3.connect('warehouse.db')
cursor = conn.cursor()


def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login():
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if not username or not password:
        messagebox.showwarning("Внимание", "Заполните все поля!")
        return

    hashed_password = hash_pass(password)
    cursor.execute("SELECT id, username, role FROM users WHERE username=? AND password=?",
                   (username, hashed_password))
    user_data = cursor.fetchone()

    if user_data:
        user = {"id": user_data[0], "username": user_data[1], "role": user_data[2]}
        root.destroy()  # Закрываем окно входа
        show_main_window(user, conn, cursor)  # Открываем главное окно
    else:
        messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль.")


def register():
    username = entry_reg_username.get().strip()
    password = entry_reg_password.get().strip()
    role = reg_role_var.get()

    if not username or not password:
        messagebox.showwarning("Внимание", "Заполните все поля!")
        return

    if len(password) < 4:
        messagebox.showerror("Ошибка", "Пароль должен быть не менее 4 символов")
        return

    hashed_password = hash_pass(password)
    try:
        cursor.execute("INSERT INTO users(username, password, role) VALUES (?, ?, ?)",
                       (username, hashed_password, role))
        conn.commit()
        messagebox.showinfo("Успех", "Пользователь зарегистрирован! Теперь войдите.")
        show_login_frame()
    except sqlite3.IntegrityError:
        messagebox.showerror("Ошибка", "Такой пользователь уже существует!")


def show_login_frame():
    reg_frame.pack_forget()
    login_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)


def show_register_frame():
    login_frame.pack_forget()
    reg_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)


# === Настройка главного окна ===
root = Tk()
root.title("Складская система - Авторизация")
root.geometry("400x450")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Стили
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc")

# === Frame Входа ===
login_frame = Frame(root, bg="#f0f0f0")
Label(login_frame, text="🔐 Вход в систему", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=15)
Label(login_frame, text="Имя пользователя:", bg="#f0f0f0").pack(anchor=W)
entry_username = Entry(login_frame, width=30, font=("Arial", 10))
entry_username.pack(pady=5)
Label(login_frame, text="Пароль:", bg="#f0f0f0").pack(anchor=W)
entry_password = Entry(login_frame, show="*", width=30, font=("Arial", 10))
entry_password.pack(pady=5)

Button(login_frame, text="Войти", command=login, width=20, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(
    pady=15)
Button(login_frame, text="Нет аккаунта? Регистрация", command=show_register_frame, bg="#2196F3", fg="white",
       width=20).pack()

# === Frame Регистрации ===
reg_frame = Frame(root, bg="#f0f0f0")
Label(reg_frame, text="📝 Регистрация", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=15)
Label(reg_frame, text="Имя пользователя:", bg="#f0f0f0").pack(anchor=W)
entry_reg_username = Entry(reg_frame, width=30, font=("Arial", 10))
entry_reg_username.pack(pady=5)
Label(reg_frame, text="Пароль:", bg="#f0f0f0").pack(anchor=W)
entry_reg_password = Entry(reg_frame, show="*", width=30, font=("Arial", 10))
entry_reg_password.pack(pady=5)

Label(reg_frame, text="Роль:", bg="#f0f0f0").pack(anchor=W)
reg_role_var = StringVar(value="employee")
role_combo = ttk.Combobox(reg_frame, textvariable=reg_role_var, values=["employee", "admin"], state="readonly",
                          width=27)
role_combo.pack(pady=5)

Button(reg_frame, text="Зарегистрироваться", command=register, width=20, bg="#4CAF50", fg="white",
       font=("Arial", 10, "bold")).pack(pady=15)
Button(reg_frame, text="Назад ко входу", command=show_login_frame, bg="#FF9800", fg="white", width=20).pack()

# Запуск окна входа
login_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

root.mainloop()
conn.close()
