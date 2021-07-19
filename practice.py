#Семестровое задание
#Шиленков Алексей ИУ7-15Б
#первая инструкция
reg_instructions = """ 
    Для начала введите название книг и фамилию с именем автора.
    Вводить стоит в форме, предоставленной ниже:

        "Название книги" by Фамилия, И.

    Для окончания записи вам следует ввести END
    Для вывода данного сообщения вы можете ввести HELP

    Ограничения: Название книги и строчка автора не должны превышать 60 символов
    """
#вторая инструкция
instruction = """
    Доступные команды:

            BORROW - взятие книги из библиотеки
                >: BORROW "Название"

            RETURN - возврат книги в библиотеку
                >: RETURN "Название"

            SHELVE - выдача последовательности команд для правильного
                     расстановки книг на полке
                >: SHELVE

            END - конец работы со списком
                >: END

            HELP - вывести данное руководство
                >: HELP
    """
#--------------------------------------------------------------------------------------
#Code
#кэш для работы
database = []

def Help(flag_info):
    # команда для возврата подсказки
    if flag_info == 'main':
        print(instruction) # вторая
    if flag_info == 'register':
        print(reg_instructions) # первая

def register():
    # регистрация книг
    # переменная ввода
    answer = '' 
    while(answer != 'END'):
        # ввод
        answer = input()
        if answer == "END":
            print("Регистрация завершена")
        elif answer == 'HELP':
            # Вывод инструкции
            Help('register') 
        else:
            # ячейка, которая принимает значения парсинга строки, принимает 0 если ввод неверный
            cell = parse(answer)
            if cell is 0:
                print("Вы ввели неверно, пожалуйста, повторите ввод.")
            else:
                # проверка на длину
                if len(cell[0]) > 60: print('Слишком большая длина названия')
                elif len(cell[1]) > 60: print('Слишком большая длина ФИО автора')
                else: database.append(cell)

def sort(inp):
    # ключ сортировки
    return not inp[2], inp[1], inp[0], inp[3]

def sorting():
    # сортировка TimSort (намного быстрее quicksort)
    database.sort(key=sort)
        
def parse(answer):
    # форматирование строки
    if answer[0] is '"' and '" by ' in answer:
        #удаляем первую кавычку
        answer = answer[1:]
        #разделяй и властвуй
        name,author = answer.split('" by ')
        # название, автор, наличие книги в реальном времени, наличие на полке
        box = [name, author, True , True]
        return box
    else:
        return 0
        
def commands(command):
    # команды для работы с книгами
    tail = command[1]
    command = command[0]
    if command == "BORROW":
        Borrow(tail)
    elif command == "RETURN":
        Return(tail)
    else:
        print("Такой команды нет")


def Borrow(tail):
    # команда для взятия книг
    catched = False
    for cell in database:
        if cell[0] == tail:
            #есть ли книга на руках
            if cell[2]:
                cell[2] = False
                cell[3] = False
            else:
                print("Эту книгу уже взяли")
            catched = True
            break
    if not catched:
        print("Такой книги нет в базе")

def Return(tail):
    # команда для возврата книг
    catched = False
    for cell in database:
        if cell[0] == tail:
            if not cell[2]:
                cell[2] = True
            else:
                print("Книга была возвращена")
            catched = True
            break
    if not catched:
        print("Такой книги нет в базе")
            
def Shelve():
    # команда для воспроизведения последовательности команд пользователю
    sorting()
    ending = False
    count = 0
    # определяем до какой строки идти
    for cell in database:
        if cell[2] == True:
            count += 1
    for iteration in range(count):
        if not database[iteration][3]:
            ending = True
            if iteration == 0:
                print('Put "' + database[iteration][0] + '" first')
            else:
                print('Put "' + database[iteration][0] + '" after "' + database[iteration-1][0] + '"')
            database[iteration][3] = True
    if ending:
        print("END")

def main():
    #Основное тело, принцип вызова функций тот же
    command = ''
    while (command != 'END'):
        command = input()
        if command == "HELP":
            Help('main')
        elif command == "SHELVE":
            #Сортирует и выводит последовательность
            Shelve()
        elif command == "END":
            print('Программа завершена')
        else:
            #Парсинг команд
            command = command.split('"')[:-1]
            if len(command) == 2:
                command[0] = command[0][:-1]
                commands(command)
            else:
                print("Неправильный синтаксис")
   
# вывод помощи
Help('register')
# регистрация книг в базу
register()
Help('main')
# тело функции, основная, управляющая
main()
