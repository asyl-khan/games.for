from logging import root
import tkinter as tk
import random
from tkinter import messagebox
import time

def exit_to_menu(root):
    root.destroy()

    print("1.Игры на память")
    print("2.Игры с реакцией")
    print("3.Игра с задачами")

    game_select = int(input("Выберите игру и его тип:"))

    if game_select == 1:
        memoryrizzer()
    elif game_select == 2:
        reaction()
    elif game_select == 3:
        zadachki()
    else:
        print("Такого значение нет")
        start()

def memoryrizzer1():

    root = tk.Tk()
    root.title("Simon Says")
    root.geometry("500x400")

    colors = ["Красный", "Синий", "Зелёный", "Жёлтый"]

    sequence = []
    score = 0

    label = tk.Label(root, text="Нажми Старт", font=("Arial", 18))
    label.pack(pady=20)

    score_label = tk.Label(root, text="Очки: 0", font=("Arial", 14))
    score_label.pack()

    entry = tk.Entry(root, font=("Arial", 16), state="disabled")
    entry.pack(pady=10)

    check_button = tk.Button(
        root,
        text="Отправить ответ",
        font=("Arial", 14),
     state="disabled"
    )
    check_button.pack(pady=10)

    # Показ последовательности
    def show_sequence():
        entry.config(state="disabled")
        check_button.config(state="disabled")

        text = "Запомни:\n" + " ".join(sequence)
        label.config(text=text)

        root.after(3000, hide_sequence)

    # Скрытие последовательности
    def hide_sequence():
        label.config(text="Теперь введи цвета которые запомнил!")

        entry.config(state="normal")

        entry.delete(0, tk.END)

        check_button.config(state="normal")

    # Новый раунд
    def next_round():
        sequence.append(random.choice(colors))

        entry.delete(0, tk.END)

        show_sequence()

    # Проверка ответа
    def check_answer():
        global score

        user_input = entry.get().split()

        if user_input == sequence:
            score += 1

            score_label.config(text=f"Очки: {score}")

            label.config(text="Верно!")

            entry.config(state="disabled")
            check_button.config(state="disabled")

            root.after(1000, next_round)

        else:
             label.config(
             text=f"Ошибка!\nПравильно:\n{' '.join(sequence)}"
             )

             entry.config(state="disabled")
             check_button.config(state="disabled")

    # Подключаем кнопку к функции
    check_button.config(command=check_answer)

    # Старт игры
    def start_game():
        global sequence
        global score

        sequence = []
        score = 0

        score_label.config(text="Очки: 0")

        next_round()

    start_button = tk.Button(
         root,
         text="Старт",
         font=("Arial", 14),
         command=start_game
         )
    start_button.pack(pady=10)

    exit_btn = tk.Button(
        root,
        text="Выйти в меню",
        font=("Arial", 12),
        command=lambda: exit_to_menu(root)
    )
    exit_btn.pack(pady=10)
    
    root.mainloop()

def memoryrizzer2():
    # Окно
    root = tk.Tk()
    root.title("Memory Game")

    # Символы
    symbols = ['🍎', '🍌', '🍇', '🍒', '🥝', '🍍', '🥑', '🍉']

    buttons = []
    cards = []

    # Используем словарь для хранения состояния, чтобы избежать проблем с global во вложенных функциях
    state = {
        'first_card': None,
        'second_card': None,
        'lock': False,
        'score': 0,
        'matched_pairs': 0
    }

    score_label = tk.Label(root, text="Очки: 0", font=("Arial", 16))
    score_label.grid(row=0, column=0, columnspan=4, pady=10)

    # Перезапуск игры
    def restart_game():
        state['first_card'] = None
        state['second_card'] = None
        state['lock'] = False
        state['matched_pairs'] = 0
        state['score'] = 0

        score_label.config(text="Очки: 0")
        
        nonlocal cards
        cards = symbols * 2
        random.shuffle(cards)

        for btn in buttons:
            btn.config(text="?", state="normal")

    # Проверка карточек
    def check_cards():
        f_idx = state['first_card']
        s_idx = state['second_card']

        if cards[f_idx] == cards[s_idx]:
            buttons[f_idx]["state"] = "disabled"
            buttons[s_idx]["state"] = "disabled"

            state['score'] += 10
            state['matched_pairs'] += 1

            score_label.config(text=f"Очки: {state['score']}")

            if state['matched_pairs'] == 8:
                messagebox.showinfo(
                    "Победа!",
                    f"Ты нашёл все пары!\nТвои очки: {state['score']}"
                )
                restart_game()
                return
        else:
            # Если не совпали, закрываем их обратно
            buttons[f_idx]["text"] = "?"
            buttons[s_idx]["text"] = "?"

            state['score'] -= 2
            score_label.config(text=f"Очки: {state['score']}")

        # В любом случае сбрасываем выделение и снимаем блокировку
        state['first_card'] = None
        state['second_card'] = None
        state['lock'] = False

    # Нажатие на карточку
    def click(index):
        if state['lock']:
            return
            
        if buttons[index]["text"] != "?":
            return
        
        buttons[index]["text"] = cards[index]

        if state['first_card'] is None:
            state['first_card'] = index
        elif state['second_card'] is None:
            state['second_card'] = index
            state['lock'] = True

            # Ждем 1 секунду, чтобы игрок успел увидеть вторую карточку
            root.after(1000, check_cards)

    exit_btn = tk.Button(
        root,
        text="Выйти в меню",
        font=("Arial", 12),
        command=lambda: exit_to_menu(root)
    )
    exit_btn.grid(row=5, column=0, columnspan=4, pady=10)

    # Создание кнопок
    for i in range(16):
        btn = tk.Button(
            root,
            text="?",
            width=8,
            height=4,
            font=("Arial", 16),
            command=lambda i=i: click(i)
        )
        
        btn.grid(row=(i // 4) + 1, column=i % 4, padx=5, pady=5)
        buttons.append(btn)

    # Запуск игры
    restart_game()
    root.mainloop()


def reaction1():
    root = tk.Tk()
    root.title("Тест реакции")
    root.geometry("400x400")
    root.configure(bg="#f0f0f0")

    # Переменные для хранения времени и состояния игры
    start_time = 0
    game_state = "idle"  # Может быть: idle (ожидание), waiting (ожидание зеленого), active (пора кликать), penalty (штраф)

    # Главная метка для инструкций и результатов
    info_label = tk.Label(
        root, 
        text="Нажми на ОГРАМЕЕЕЕЕНУЮ кнопку снизу чтобы начать", 
        font=("Arial", 14), 
        bg="#f0f0f0",
        wraplength=350
    )
    info_label.pack(pady=40)

    # Функция, которая делает кнопку снова активной после штрафа
    def end_penalty():
        nonlocal game_state
        if game_state == "penalty":
            game_state = "waiting"
            main_button.config(text="Жди...", bg="#ff4d4d", state="normal")
            info_label.config(text="Внимание... И сново не беги впереди поровоза!")

    # Функция, которая срабатывает, когда "таймер подошел" и пора кликать
    def trigger_click():
        nonlocal start_time, game_state
        # Проверяем, не нажал ли игрок фальстарт прямо перед триггером
        if game_state == "waiting":
            game_state = "active"
            main_button.config(text="КЛИКАЙ!!!", bg="#2ecc71")  # Зеленый цвет
            start_time = time.time()  # Фиксируем точное время старта

    # Функция обработки клика по главной кнопке
    def on_click():
        nonlocal start_time, game_state

        # Сценарий 1: Игра еще не запущена
        if game_state == "idle":
            game_state = "waiting"
            main_button.config(text="Жди...", bg="#ff4d4d")  # Красный цвет
            info_label.config(text="Готовься...")
            
            # Генерируем случайное время ожидания от 2000 до 5000 миллисекунд (2-5 сек)
            delay = random.randint(2000, 5000)
            root.after(delay, trigger_click)

        # Сценарий 2: Игрок нажал слишком рано (Фальстарт!)
        elif game_state == "waiting":
            game_state = "penalty"
            main_button.config(text="НАКАЗАНЬЕ!", bg="#7f8c8d", state="disabled")
            info_label.config(text="Не беги впереди поровоза.")
            # Через 1000 мс (1 сек) возвращаем игру в режим ожидания
            root.after(1000, end_penalty)

        # Сценарий 3: Успешный клик по зеленой кнопке!
        elif game_state == "active":
            end_time = time.time()  # Фиксируем время клика
            # Считаем разницу в секундах и переводим в миллисекунды
            reaction_time = int((end_time - start_time) * 1000)
            
            info_label.config(text=f"Твой результат: {reaction_time} мс(нажатие после запуска таймера)!")
            
            # Сбрасываем кнопку в начальное состояние
            game_state = "idle"
            main_button.config(text="Старт", bg="#3498db")

    exit_btn = tk.Button(
        root,
        text="Выйти в меню",
        font=("Arial", 12),
        command=lambda: exit_to_menu(root)
    )
    exit_btn.pack(pady=10)

    # Главная кнопка по центру
    main_button = tk.Button(
        root,
        text="Старт",
        font=("Arial", 18, "bold"),
        bg="#3498db",  # Синий цвет
        fg="white",
        width=15,
        height=4,
        command=on_click
    )
    main_button.pack(expand=True)

    root.mainloop()

def reaction_clicker():
    root = tk.Tk()
    root.title("Поймай кнопку!")
    root.geometry("500x500")
    root.configure(bg="#f0f0f0")

    # Игровые переменные
    score = 0
    target_score = 10
    game_active = False
    button_clicked = False
    timer_id = None  # Здесь будем хранить ID текущего таймера, чтобы его сбрасывать

    # Контейнер для меню настроек
    menu_frame = tk.Frame(root, bg="#f0f0f0")
    menu_frame.pack(pady=20)

    tk.Label(menu_frame, text="До скольки очков играем?", font=("Arial", 12), bg="#f0f0f0").pack()
    
    target_entry = tk.Entry(menu_frame, font=("Arial", 12), width=10, justify="center")
    target_entry.insert(0, "10")
    target_entry.pack(pady=5)

    # Панель счета
    score_label = tk.Label(root, text="Очки: 0 / Твоя цель в очках: 0", font=("Arial", 14, "bold"), bg="#f0f0f0")
    
    # Игровая кнопка
    click_button = tk.Button(
        root, 
        text="КЛИКАЙ!", 
        font=("Arial", 12, "bold"), 
        bg="#e74c3c", 
        fg="white",
        width=8,
        height=2
    )

    # Функция перемещения кнопки
    def move_button():
        nonlocal score, game_active, button_clicked, timer_id
        
        # 1. Первым делом отменяем старый запланированный таймер, если он есть
        if timer_id is not None:
            root.after_cancel(timer_id)
            timer_id = None

        if not game_active:
            return

        # Если раунд закончился, а игрок НЕ нажал на кнопку — штрафуем
        if not button_clicked:
            score -= 1
            score_label.config(text=f"Очки: {score} / Цель: {target_score}")

        if score >= target_score:
            game_active = False
            click_button.place_forget()
            messagebox.showinfo("Победа!", f"Отлично! Ты набрал {score} очков!")
            reset_to_menu()
            return

        # Сбрасываем флаг клика для нового раунда
        button_clicked = False

        # Координаты для прыжка кнопки
        max_x = root.winfo_width() - 100 if root.winfo_width() > 100 else 400
        max_y = root.winfo_height() - 100 if root.winfo_height() > 100 else 400
        
        x = random.randint(10, max(10, max_x))
        y = random.randint(60, max(60, max_y))

        click_button.place(x=x, y=y)

        # 2. Записываем новый таймер в переменную timer_id
        timer_id = root.after(1000, move_button)

    # Обработка успешного нажатия на кнопку
    def on_button_click():
        nonlocal score, button_clicked
        if not game_active or button_clicked:
            return
        
        button_clicked = True
        score += 1
        score_label.config(text=f"Очки: {score} / Цель: {target_score}")
        
        # Вызываем перемещение. Теперь оно само сбросит старый таймер секунды!
        move_button()

    click_button.config(command=on_button_click)

    # Запуск игры
    def start_game():
        nonlocal score, target_score, game_active, button_clicked, timer_id
        
        try:
            target_score = int(target_entry.get())
            if target_score <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введи целое число больше 0!")
            return

        score = 0
        game_active = True
        button_clicked = True 
        timer_id = None # Сбрасываем ID перед стартом

        menu_frame.pack_forget()
        start_btn.pack_forget()

        score_label.config(text=f"Очки: {score} / Цель: {target_score}")
        score_label.pack(pady=10)

        move_button()

    exit_btn = tk.Button(
        root,
        text="Выйти в меню",
        font=("Arial", 12),
        command=lambda: exit_to_menu(root)
    )
    exit_btn.pack(pady=10)

    # Кнопка СТАРТ в главном меню
    start_btn = tk.Button(root, text="Начать игру", font=("Arial", 14), bg="#2ecc71", fg="white", command=start_game)
    start_btn.pack(pady=10)

    # Возврат в меню после окончания
    def reset_to_menu():
        nonlocal timer_id
        if timer_id is not None:
            root.after_cancel(timer_id)
            timer_id = None
        score_label.pack_forget()
        menu_frame.pack(pady=20)
        start_btn.pack(pady=10)

    root.mainloop()

def zadachki():
    # Создаем графическое окно только при запуске этой игры
    root = tk.Tk()
    root.title("Математический тренажер")
    root.geometry("450x350")
    root.configure(bg="#f4f6f7")

    # Переменные для хранения текущего ответа и счета
    correct_answer = 0
    score = 0

    # Элементы интерфейса
    title_label = tk.Label(root, text="Реши пример!", font=("Arial", 16, "bold"), bg="#f4f6f7", fg="#2c3e50")
    title_label.pack(pady=15)

    score_label = tk.Label(root, text="Очки: 0", font=("Arial", 12), bg="#f4f6f7", fg="#7f8c8d")
    score_label.pack()

    primer_label = tk.Label(root, text="", font=("Arial", 24, "bold"), bg="#f4f6f7", fg="#2980b9")
    primer_label.pack(pady=20)

    entry = tk.Entry(root, font=("Arial", 16), justify="center", width=10)
    entry.pack(pady=10)
    entry.focus() # Автоматически ставим курсор в поле ввода

    result_label = tk.Label(root, text="", font=("Arial", 12), bg="#f4f6f7")
    result_label.pack(pady=10)

    # Функция генерации нового примера
    def generate_primer():
        nonlocal correct_answer
        num1 = random.randint(0, 10)
        num2 = random.randint(0, 10)
        num3 = random.randint(0, 10)
        
        op1 = random.choice(['+', '-'])
        op2 = random.choice(['+', '-'])
        
        primer_text = f"{num1} {op1} {num2} {op2} {num3}"
        correct_answer = eval(primer_text)
        
        primer_label.config(text=f"{primer_text} = ?")
        entry.delete(0, tk.END)

    # Функция проверки ответа
    def check_answer(event=None): # event нужен, чтобы работало нажатие на Enter
        nonlocal score
        user_input = entry.get().strip()
        
        try:
            user_answer = int(user_input)
            if user_answer == correct_answer:
                score += 1
                score_label.config(text=f"Очки: {score}")
                result_label.config(text="Правильно! 👍", fg="#2ecc71")
                # Через 1 секунду показываем новый пример
                root.after(1000, generate_primer)
                result_label.after(1000, lambda: result_label.config(text=""))
            else:
                result_label.config(text=f"Ошибка! Правильно: {correct_answer}", fg="#e74c3c")
                root.after(1500, generate_primer)
                result_label.after(1500, lambda: result_label.config(text=""))
        except ValueError:
            result_label.config(text="Введи число!", fg="#e67e22")

    # Кнопка проверки
    check_button = tk.Button(
        root, 
        text="Проверить", 
        font=("Arial", 12, "bold"), 
        bg="#3498db", 
        fg="white", 
        command=check_answer
    )
    check_button.pack(pady=10)

    exit_btn = tk.Button(
        root,
        text="Выйти в меню",
        font=("Arial", 12),
        command=lambda: exit_to_menu(root)
    )
    exit_btn.pack(pady=10)

    # Связываем клавишу Enter на клавиатуре с проверкой ответа (для удобства)
    root.bind('<Return>', check_answer)

    # Запускаем первый пример
    generate_primer()
    
    root.mainloop()

def memoryrizzer():
    print("1.Запомни цвета")
    print("2.Запомни фигуры")
    game_choose=int(input("Выберите игру:"))
    if game_choose==1:
        memoryrizzer1()
    elif game_choose==2:
        memoryrizzer2()
    else:
        print("Такого значение нет")
        memoryrizzer()

def reaction():
    print("1.Клик на скорость")
    print("2.Ввод мышью")
    game_choosen=int(input("Выберите игру:"))
    if game_choosen==1:
        reaction1()
    elif game_choosen==2:
        reaction_clicker()
    else:
        print("Такого значение нет")
        reaction()

def start():
    print("Данная консолное приложение представляет из себя помощник для тех у кого осложнение с моторикой,реакцией,памятью(введите число игры которую вы хотите поиграть)")
    print("1.Игры на память")
    print("2.Игры с реакцией")
    print("3.Игра с задачами")
    game_select=int(input("Выберите игру и его тип:"))
    if game_select==1:
        memoryrizzer()
    elif game_select==2:
        reaction()
    elif game_select==3:
        zadachki()
    else:
        print("Такого значение нет")
start()
