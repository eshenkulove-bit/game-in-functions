import random


def get_valid_number(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка Введи целое число")


def play_round(max_attempts=10):
    secret_number = random.randint(1, 100)
    attempts = 0

    print("Игра Угадай число")
    print("Я загадал число от 1 до 100")
    print("У тебя есть", max_attempts, "попыток")

    while attempts < max_attempts:
        guess = get_valid_number("Введи число: ")
        attempts += 1

        if guess == secret_number:
            print("Угадал")
            print("Число было", secret_number)
            print("Попыток потрачено", attempts)
            return True
        elif guess < secret_number:
            print("Мое число больше")
        else:
            print("Мое число меньше")

        remaining = max_attempts - attempts
        if remaining > 0:
            print("Осталось попыток", remaining)

    print("Все попытки закончились")
    print("Загаданное число было", secret_number)
    return False


def main():
    play_again = "да"

    while play_again == "да":
        play_round()
        play_again = input("Сыграем еще раз да нет: ").strip().lower()

    print("Спасибо за игру")


if __name__ == "__main__":
    main()