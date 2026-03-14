import tkinter as tk
from tkinter import messagebox, simpledialog


class CyberClubApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Управление компьютерным клубом")
        self.geometry("400x300")
        self.users = {
            "admin": {"password": "123", "role": "admin"},
            "manager": {"password": "123", "role": "manager"}
        }
        self.computers = {
            "1": {"status": "free", "client": ""},
            "2": {"status": "free", "client": ""},
            "3": {"status": "free", "client": ""},
            "4": {"status": "occupied", "client": "Иван Иванов"},
            "5": {"status": "reserved", "client": "Алексей Петров"}
        }
        self.current_user = None
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label="Авторизация", command=self.login_window)
        file_menu.add_command(label="Выход", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Закрыть программу", command=self.quit)
        computer_menu = tk.Menu(menu_bar, tearoff=False)
        computer_menu.add_command(label="Посмотреть свободные ПК", command=self.view_free_computers)
        computer_menu.add_command(label="Забронировать ПК", command=self.reserve_computer)
        computer_menu.add_command(label="Освободить ПК", command=self.release_computer)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        menu_bar.add_cascade(label="Компьютер", menu=computer_menu)

    def login_window(self):
        if not hasattr(self, 'login_frame') or not self.login_frame.winfo_exists():
            self.login_frame = tk.Toplevel(self)
            self.login_frame.title("Авторизация сотрудника")
            tk.Label(self.login_frame, text="Логин сотрудника:").grid(row=0, column=0)
            username_entry = tk.Entry(self.login_frame)
            username_entry.grid(row=0, column=1)
            tk.Label(self.login_frame, text="Пароль сотрудника:").grid(row=1, column=0)
            password_entry = tk.Entry(self.login_frame, show="*")
            password_entry.grid(row=1, column=1)
            tk.Button(
                self.login_frame,
                text="Войти",
                command=lambda: self.authenticate(username_entry.get().strip(), password_entry.get())
            ).grid(row=2, columnspan=2)

    def authenticate(self, username, password):
        user_data = self.users.get(username)
        if user_data and user_data["password"] == password:
            self.current_user = {"username": username, "role": user_data["role"]}
            messagebox.showinfo("Успешно", f"Сотрудник '{username}' вошёл в систему.")
            self.login_frame.destroy()
        else:
            messagebox.showerror("Ошибка", "Неправильный логин или пароль.")

    def logout(self):
        if self.current_user:
            result = messagebox.askyesno("Подтверждение выхода", "Вы точно хотите выйти из системы?")
            if result:
                self.current_user = None
                messagebox.showinfo("Выход", "Сотрудник вышел из системы.")
        else:
            messagebox.showwarning("Предупреждение", "Нет активного сотрудника.")

    def view_free_computers(self):
        free_computers = [pc for pc, info in self.computers.items() if info["status"] == "free"]
        if free_computers:
            messagebox.showinfo("Свободные компьютеры", "\n".join(free_computers))
        else:
            messagebox.showinfo("Свободные компьютеры", "Сейчас нет свободных компьютеров.")

    def reserve_computer(self):
        if self.check_access('manager'):
            client_name = simpledialog.askstring("Клиент", "ФИО клиента:")
            if client_name and len(client_name.strip()):
                selected_pc = simpledialog.askstring("Выбор компьютера",
                                                     "Какой компьютер забронировать (например PC_1)?")
                if selected_pc in self.computers:
                    if self.computers[selected_pc]["status"] == "free":
                        self.computers[selected_pc] = {"status": "reserved", "client": client_name}
                        messagebox.showinfo("Готово",
                                            f"Компьютер {selected_pc} зарезервирован для клиента {client_name}.")
                    else:
                        messagebox.showerror("Ошибка", f"Компьютер {selected_pc} занят или уже зарезервирован.")
                else:
                    messagebox.showerror("Ошибка", "Такого компьютера нет в клубе.")
            else:
                messagebox.showerror("Ошибка", "ФИО клиента не указано.")

    def release_computer(self):
        if self.check_access('manager'):
            selected_pc = simpledialog.askstring("Освобождение компьютера",
                                                 "Какой компьютер освободить (например PC_1)?")
            if selected_pc in self.computers:
                current_status = self.computers[selected_pc]["status"]
                if current_status != "free":
                    self.computers[selected_pc] = {"status": "free", "client": ""}
                    messagebox.showinfo("Готово", f"Компьютер {selected_pc} освобождён.")
                else:
                    messagebox.showerror("Ошибка", f"Компьютер {selected_pc} уже свободен.")
            else:
                messagebox.showerror("Ошибка", "Такого компьютера нет в клубе.")

    def check_access(self, required_role='manager'):
        if not self.current_user:
            messagebox.showwarning("Внимание", "Необходимо войти в систему.")
            return False
        elif self.current_user['role'] != required_role:
            messagebox.showwarning("Отказано", "Недостаточно прав для выполнения операции.")
            return False
        return True


if __name__ == "__main__":
    app = CyberClubApp()
    app.mainloop()
