import tkinter
import time
import os
from tkinter import messagebox
from tkinter import filedialog
import hashlib

# Функция для чтения пароля из файла PSW.txt
def read_password(file_path):
    with open(file_path, 'r') as file:
        password = file.read().strip()
    return password

# Функция для хэширования пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Функция для сохранения хэшированного пароля в файл LOG.txt
def save_hashed_password(hashed_password, output_file):
    with open(output_file, 'w') as file:
        file.write(hashed_password)

# Функция, обрабатывающая пароль
def process_password(input_file, output_file):
    password = read_password(input_file)
    hashed_password = hash_password(password)
    save_hashed_password(hashed_password, output_file)

class application():
    def __init__(self):
        # Создание главного окна
        self.main = tkinter.Tk()
        self.create_log_file()
        self.main.title("Однозвенная ИС")
        self.main.geometry("700x300")
        self.main.resizable(False, False)
        self.main["bg"] = "#F5F5F5" 
        process_password("PSW.txt", "LOG.txt")
        self.create_log_file()

        # Интерфейс пользовательского режима
        tkinter.Label(self.main, text="Пользовательский режим:", bg="#F5F5F5", font=("Verdana", 12)).place(x=5, y=5)
        tkinter.Label(self.main, text="x = ", bg="#F5F5F5", font=("Verdana", 12)).place(x=30, y=50)
        self.entry_inp_x = tkinter.Entry(self.main, bg="#FFFACD", width=15, font=("Verdana", 10))
        self.entry_inp_x.place(x=58, y=55)
        self.label_no_x_entered = tkinter.Label(self.main, text="", bg="#F5F5F5", fg="#000000", font=("Verdana", 12))
        self.label_no_x_entered.place(x=30, y=30)
        self.find_y_button = tkinter.Button(self.main, text="Найти y", bg="#ADD8E6", fg="#000000", font=("Verdana", 12), command=self.calculate_y)
        self.find_y_button.place(x=200, y=48)
        self.label_y_res = tkinter.Label(self.main, text="", bg="#F5F5F5", fg="#000000", font=("Verdana", 12))
        self.label_y_res.place(x=10, y=120)
        self.formula = tkinter.Label(self.main, text="", bg="#F5F5F5", fg="#000000", font=("Verdana", 12))
        self.formula.place(x=10, y=90)

        # Интерфейс режима администратора
        tkinter.Label(self.main, text="Режим администратора:", bg="#F5F5F5", font=("Verdana", 12)).place(x=350, y=5)
        tkinter.Label(self.main, text="Логин:", bg="#F5F5F5", font=("Verdana", 12)).place(x=350, y=35)
        self.entry_login = tkinter.Entry(self.main, bg="#FFFACD", font=("Verdana", 10))
        self.entry_login.place(x=425, y=40)
        tkinter.Label(self.main, text="Пароль:", bg="#F5F5F5", font=("Verdana", 12)).place(x=350, y=65)
        self.entry_password = tkinter.Entry(self.main, bg="#FFFACD", show="*", font=("Verdana", 10))
        self.entry_password.place(x=425, y=70)
        self.login_button = tkinter.Button(self.main, text="Войти", bg="#ADD8E6", font=("Verdana", 12), command=self.check_login)
        self.login_button.place(x=475, y=100)

        # Создание окна настроек
        self.settings = tkinter.Toplevel(self.main)
        self.settings.withdraw()
        self.settings.title("Настройки")
        self.settings.geometry("800x500")
        self.settings.protocol("WM_DELETE_WINDOW", self.setting_mode_off)
        self.settings["bg"] = "#F5F5F5"  # Светлый фон

        # Интерфейс окна настроек
        tkinter.Label(self.settings, text="Выберите способ ввода X:", bg="#F5F5F5", fg="#000000", font=("Verdana", 12)).place(x=10, y=7)
        tkinter.Label(self.settings, bg="#F5F5F5", fg="#000000", text="Ввести данные вручную", font=("Verdana", 11)).place(x=10, y=30)
        tkinter.Label(self.settings, text="Введите количество строк:", bg="#F5F5F5", fg="#000000", font=("Verdana", 11)).place(x=10, y=60)
        tkinter.Label(self.settings, text="(до 10 значений)", bg="#F5F5F5", fg="#000000", font=("Verdana", 11)).place(x=50, y=80)
        tkinter.Label(self.settings, text="x", bg="#F5F5F5", fg="#000000", font=("Verdana", 11)).place(x=75, y=100)
        tkinter.Label(self.settings, text="y", bg="#F5F5F5", fg="#000000", font=("Verdana", 11)).place(x=175, y=100)
        self.entry_table_button = tkinter.Button(self.settings, text="Ввод", bg="#ADD8E6", font=("Verdana", 12), command=self.compare_formulas)
        self.entry_table_button.place(x=275, y=120)
        self.entry_row_count_label = tkinter.Entry(self.settings, bg="#FFFACD", width=5, font=("Verdana", 10))
        self.entry_row_count_label.place(x=245, y=63)
        self.entry_row_count_button = tkinter.Button(self.settings, text="Ввод", bg="#ADD8E6", font=("Verdana", 12), command=self.create_table)
        self.entry_row_count_button.place(x=300, y=55)
        self.save_table = tkinter.Button(self.settings, text="Сохранить", bg="#ADD8E6", font=("Verdana", 12), command=self.save_table_to_file)
        self.save_table.place(x=275, y=160)

        # Интерфейс загрузки данных из файла
        tkinter.Label(self.settings, bg="#F5F5F5", fg="#000000", text="Загрузить данные из файла", font=("Verdana", 11)).place(x=400, y=30)
        tkinter.Label(self.settings, bg="#F5F5F5", fg="#000000", text="Введите файл:", font=("Verdana", 11)).place(x=400, y=60)
        self.entry_file_name_lable = tkinter.Entry(self.settings, bg="#FFFACD", width=50, font=("Verdana", 10))
        self.entry_file_name_lable.place(x=400, y=90)
        self.entry_file_name_button = tkinter.Button(self.settings, text="Ввод", bg="#ADD8E6", font=("Verdana", 12), command=self.process_file_data)
        self.entry_file_name_button.place(x=740, y=120)

        self.entries = []

    def setting_mode_off(self):
        self.settings.withdraw()

    def start(self):
        self.main.mainloop()
    def formula_1(self, x):
        return 5.27 + 6.93 * x
    def formula_2(self, x):
        return (-6.41) + 9.21 * x
    def formula_3(self, x):
        return (-1.38) + 7.85 * x

    # Функция для подсчета y по выбранной формуле
    def calculate_y(self):
        x = self.entry_inp_x.get()
        if x == "":
            self.label_no_x_entered.configure(text = "Ошибка: X не введён", bg = "#FFDAB9", fg = "#000000")
        else:
            self.label_no_x_entered.configure(text = "")
            x = float(x)
            if hasattr(self, 'best_formula'):
                y = self.best_formula(x)
                y_formatted = f"{y:.2f}"
                if (x < 1) or (x > 10):
                    self.label_y_res.configure(text=f"y = {y_formatted}\nРезультаты получены с помощью экстраполяции", bg="#FFDAB9", fg="#000000")
                    self.log_data(x, y_formatted)
                else:
                    self.label_y_res.configure(text=f"y = {y_formatted}", bg="#FFDAB9", fg="#000000")
                    self.log_data(x, y_formatted)
            else:
                messagebox.showerror("Ошибка", "Данные для вычисления отсутствуют.")

    # Функция для очищения таблицы
    def clear_table(self):
        for entry in self.entries:
            entry[0].destroy()
            entry[1].destroy()

    # Функция создания таблицы
    def create_table(self):
        try:
            row_count = int(self.entry_row_count_label.get())
            if row_count > 10:
                raise ValueError("Количество строк не должно превышать 10.")
            elif row_count <= 0:
                raise ValueError("Количество строк должно быть положительным числом.")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
            return
        self.clear_table()
        self.entries = []
        for i in range(row_count):
            entry_x = tkinter.Entry(self.settings, bg="#FFF0F5", width=10)
            entry_x.place(x=50, y=125 + i * 30)
            entry_y = tkinter.Entry(self.settings, bg="#FFF0F5", width=10)
            entry_y.place(x=150, y=125 + i * 30)
            self.entries.append((entry_x, entry_y))

    # Функция для сохранения введенных значений
    def save_table_to_file(self):
        if self.entry_row_count_label.get() == "":
            messagebox.showerror("Ошибка", "Не достаточно данных.")
        else:
            file_index = 1
            while os.path.exists(f"table{file_index}.txt"):
                file_index += 1
            file_name = f"table{file_index}.txt"
            try:
                with open(file_name, 'w') as file:
                    for entry_x, entry_y in self.entries:
                        x_value = entry_x.get()
                        y_value = entry_y.get()
                        if x_value == "" or y_value == "":
                            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                            return
                        file.write(f"{x_value}\t{y_value}\n")
                messagebox.showinfo("Сохранение", f"Таблица успешно сохранена в файл {file_name}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")

    # Функция для обработки имени файла
    def process_file_data(self):
        file_path = self.entry_file_name_lable.get()
        if file_path:
            self.compare_formulas(file_path=file_path)
        else:
            messagebox.showerror("Ошибка", "Введите имя файла.")

    # Функция для получени значений x и y
    def get_data(self, file_path=None):
        x_values = []
        y_values = []
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        x_str, y_str = line.strip().split()
                        x = float(x_str)
                        y = float(y_str)
                        x_values.append(x)
                        y_values.append(y)
            except FileNotFoundError:
                messagebox.showerror("Ошибка", f"Файл {file_path} не найден.")
                return None, None
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный формат данных в файле. Убедитесь, что данные числовые.")
                return None, None
        else:
            if self.entry_row_count_label.get() == "":
                messagebox.showerror("Ошибка", "Введите данные.")
                return None, None
            else:
                try:
                    for entry_x, entry_y in self.entries:
                        x = float(entry_x.get())
                        y = float(entry_y.get())
                        x_values.append(x)
                        y_values.append(y)
                except ValueError:
                    messagebox.showerror("Ошибка", "Все значения должны быть числовыми.")
                    return None, None

        return x_values, y_values

    # Функця для выбора подходящего графика
    def compare_formulas(self, file_path=None):
        x_values, y_values = self.get_data(file_path)
        if x_values is None or y_values is None:
            return
        deviation_1 = self.calculate_deviation(self.formula_1, x_values, y_values)
        deviation_2 = self.calculate_deviation(self.formula_2, x_values, y_values)
        deviation_3 = self.calculate_deviation(self.formula_3, x_values, y_values)
        min_deviation = min(deviation_1, deviation_2, deviation_3)
        if min_deviation == deviation_1:
            best_formula = self.formula_1
            self.formula.configure(text= "Выбран формула 1 (красный)", bg="#FFDAB9", fg="#000000")
        elif min_deviation == deviation_2:
            best_formula = self.formula_2
            self.formula.configure(text= "Выбран формула 2 (зеленый)", bg="#FFDAB9", fg="#000000")
        else:
            best_formula = self.formula_3
            self.formula.configure(text= "Выбран формула 3 (черный)", bg="#FFDAB9", fg="#000000")
        self.best_formula = best_formula

    # Функция для вычисления отклонения
    def calculate_deviation(self, formula, x_values, y_values):
        deviation = 0
        for x, y in zip(x_values, y_values):
            y_calculated = formula(x)
            deviation += (y - y_calculated) ** 2  # Сумма квадратов отклонений
        return deviation

    #  Функция для создания списка входов
    def create_log_file(self):
        log_file_path = "login_list.txt"
        if not os.path.exists(log_file_path):
            with open(log_file_path, "w") as log_file:
                log_file.write("Входы в систему\n")
 #  Функция для записи введенных данных
    def log_data(self, x_data, y_data):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        with open("login_list.txt", "a") as log_file:
            if (x_data < 1) or (x_data > 10):
                log_file.write(f"{current_time} - Пользовательский режим: x={x_data}    y={y_data} - Результаты получены с помощью экстраполяции.\n")
            else:
                log_file.write(f"{current_time} - Пользовательский режим: x={x_data}    y={y_data}\n")

    #  Функция для записи данных о входе в файл
    def log_successful_login(self, username):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        with open("login_list.txt", "a") as log_file:
            log_file.write(f"{current_time} - Администратор {username} вошел в систему\n")

    # Фунция для проверки правильности логина и пароля
    def check_login(self):
        with open("logins.txt", "r") as file:
            logins = file.readlines()
        entered_login = self.entry_login.get()
        found = False
        for login in logins:
            login = login.strip()
            if entered_login == login:
                found = True
                break
        with open("LOG.txt", 'r') as file:
            password = file.read().strip()
        entered_password = hash_password(self.entry_password.get())
        if entered_password == password and found == True:
            self.log_successful_login(entered_login)
            self.settings.deiconify()
        else:
            messagebox.showerror("Ошибка входа", "Неверный логин или пароль")
 
# Запуск приложения
application_exemplar = application()
application_exemplar.start()
