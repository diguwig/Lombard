from tkinter import *
from tkinter import ttk, messagebox


def show_main_window(user, conn, cursor):
    main_root = Toplevel()
    main_root.title(f"Панель управления ({user['role']})")
    main_root.geometry("800x650")
    main_root.configure(bg="#f0f0f0")

    # Хранилище ID для безопасной работы
    product_ids = []
    user_ids = []

    def fetch_products():
        cursor.execute("SELECT * FROM products")
        return cursor.fetchall()

    def fetch_users():
        cursor.execute("SELECT id, username, role FROM users")
        return cursor.fetchall()

    def refresh_products():
        listbox_products.delete(0, END)
        product_ids.clear()
        for row in fetch_products():
            product_ids.append(row[0])
            listbox_products.insert(END, f"ID:{row[0]} | {row[1]} | Кол-во:{row[2]} | Цена:{row[3]}р.")

    def refresh_users():
        listbox_users.delete(0, END)
        user_ids.clear()
        for row in fetch_users():
            user_ids.append(row[0])
            listbox_users.insert(END, f"ID:{row[0]} | {row[1]} | Роль:{row[2]}")

    def add_product():
        try:
            name = entry_name.get().strip()
            qty = int(entry_qty.get())
            price = float(entry_price.get())
            if not name or qty < 0 or price < 0:
                raise ValueError
            cursor.execute("INSERT INTO products(name, quantity, price) VALUES (?, ?, ?)", (name, qty, price))
            conn.commit()
            refresh_products()
            clear_product_fields()
            messagebox.showinfo("Успех", "Товар добавлен!")
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте данные (название, числовые значения >= 0)")

    def edit_product():
        try:
            idx = listbox_products.curselection()[0]
            pid = product_ids[idx]
            name = entry_name.get().strip()
            qty = int(entry_qty.get())
            price = float(entry_price.get())
            if not name or qty < 0 or price < 0:
                raise ValueError
            cursor.execute("UPDATE products SET name=?, quantity=?, price=? WHERE id=?", (name, qty, price, pid))
            conn.commit()
            refresh_products()
            clear_product_fields()
            messagebox.showinfo("Успех", "Товар обновлен!")
        except IndexError:
            messagebox.showwarning("Внимание", "Выберите товар для редактирования")
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте данные")

    def delete_product():
        try:
            idx = listbox_products.curselection()[0]
            pid = product_ids[idx]
            if messagebox.askyesno("Подтверждение", "Удалить товар?"):
                cursor.execute("DELETE FROM products WHERE id=?", (pid,))
                conn.commit()
                refresh_products()
                clear_product_fields()
        except IndexError:
            messagebox.showwarning("Внимание", "Выберите товар")

    def delete_user():
        if user['role'] != 'admin':
            messagebox.showerror("Доступ запрещен", "Только админ может удалять пользователей")
            return
        try:
            idx = listbox_users.curselection()[0]
            uid = user_ids[idx]
            if uid == user['id']:
                messagebox.showerror("Ошибка", "Нельзя удалить самого себя!")
                return
            if messagebox.askyesno("Подтверждение", "Удалить пользователя?"):
                cursor.execute("DELETE FROM users WHERE id=?", (uid,))
                conn.commit()
                refresh_users()
        except IndexError:
            messagebox.showwarning("Внимание", "Выберите пользователя")

    def clear_product_fields():
        entry_name.delete(0, END)
        entry_qty.delete(0, END)
        entry_price.delete(0, END)

    def on_product_select(event):
        try:
            idx = listbox_products.curselection()[0]
            row = fetch_products()[idx]
            clear_product_fields()
            entry_name.insert(0, row[1])
            entry_qty.insert(0, row[2])
            entry_price.insert(0, row[3])
        except IndexError:
            pass

    # === Вкладки ===
    notebook = ttk.Notebook(main_root)
    notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # --- Вкладка Товары ---
    tab_products = Frame(notebook, bg="#f0f0f0")
    notebook.add(tab_products, text="📦 Товары")

    frame_list = Frame(tab_products)
    frame_list.pack(fill=BOTH, expand=True, pady=10)

    scrollbar = Scrollbar(frame_list)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Исправлено имя класса Listbox
    listbox_products = Listbox(frame_list, yscrollcommand=scrollbar.set, font=("Consolas", 10))
    listbox_products.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(command=listbox_products.yview)
    listbox_products.bind('<ListboxSelect>', on_product_select)

    frame_form = LabelFrame(tab_products, text="Данные товара", padx=10, pady=10, bg="#f0f0f0")
    frame_form.pack(fill=X, pady=10)

    Label(frame_form, text="Название:", bg="#f0f0f0").grid(row=0, column=0, sticky=W)
    entry_name = Entry(frame_form, width=30)
    entry_name.grid(row=0, column=1, pady=5)

    Label(frame_form, text="Кол-во:", bg="#f0f0f0").grid(row=1, column=0, sticky=W)
    entry_qty = Entry(frame_form, width=30)
    entry_qty.grid(row=1, column=1, pady=5)

    Label(frame_form, text="Цена:", bg="#f0f0f0").grid(row=2, column=0, sticky=W)
    entry_price = Entry(frame_form, width=30)
    entry_price.grid(row=2, column=1, pady=5)

    frame_btn = Frame(tab_products, bg="#f0f0f0")
    frame_btn.pack(pady=10)

    # Исправлено имя класса Button
    Button(frame_btn, text="➕ Добавить", command=add_product, bg="#4CAF50", fg="white", width=12).pack(side=LEFT,
                                                                                                       padx=5)
    Button(frame_btn, text="✏️ Изменить", command=edit_product, bg="#2196F3", fg="white", width=12).pack(side=LEFT,
                                                                                                         padx=5)
    Button(frame_btn, text="🗑️ Удалить", command=delete_product, bg="#f44336", fg="white", width=12).pack(side=LEFT,
                                                                                                          padx=5)
    Button(frame_btn, text="🔄 Обновить", command=refresh_products, bg="#FF9800", fg="white", width=12).pack(side=LEFT,
                                                                                                            padx=5)

    # --- Вкладка Пользователи (Только Админ) ---
    if user['role'] == 'admin':
        tab_users = Frame(notebook, bg="#f0f0f0")
        notebook.add(tab_users, text="👥 Пользователи")

        listbox_users = Listbox(tab_users, font=("Consolas", 10))
        listbox_users.pack(fill=BOTH, expand=True, padx=10, pady=10)
        Button(tab_users, text="🗑️ Удалить пользователя", command=delete_user, bg="#f44336", fg="white").pack(pady=5)

    # Статус бар
    Label(main_root, text=f"Пользователь: {user['username']} | Роль: {user['role']} ",
          bg="#333", fg="white", pady=5).pack(fill=X, side=BOTTOM)

    refresh_products()
    if user['role'] == 'admin':
        refresh_users()

    return main_root
