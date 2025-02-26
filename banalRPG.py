import random
import json
import os

# Глобальные переменные
player = {
    "name": "Герой",
    "hp": 100,
    "damage": 10,
    "inventory": [],
    "location": "Лес"
}

# Локации
locations = {
    "Лес": {
        "description": "Вы находитесь в темном лесу. Слышны шорохи и шелест листвы.",
        "items": ["Меч", "Зелье здоровья"],
        "monsters": ["Волк", "Гоблин"],
        "directions": {"север": "Пещера", "восток": "Город"}
    },
    "Пещера": {
        "description": "Вы вошли в пещеру. Здесь холодно и сыро.",
        "items": ["Ключ", "Щит"],
        "monsters": ["Скелет", "Бандит"],
        "directions": {"юг": "Лес", "восток": "Логово Дракона"}
    },
    "Город": {
        "description": "Вы в городе. Здесь много людей и магазинов.",
        "items": ["Золото", "Еда"],
        "monsters": [],
        "directions": {"запад": "Лес", "север": "Храм"}
    },
    "Логово Дракона": {
        "description": "Вы достигли логова дракона. Здесь жарко, а воздух пропитан запахом серы.",
        "items": ["Магический артефакт"],
        "monsters": ["Дракон"],
        "directions": {"запад": "Пещера"}
    }
}

# Монстры
monsters = {
    "Волк": {"hp": 20, "damage": 5},
    "Гоблин": {"hp": 30, "damage": 8},
    "Скелет": {"hp": 40, "damage": 10},
    "Бандит": {"hp": 50, "damage": 12},
    "Дракон": {"hp": 100, "damage": 20}
}

# Функции
def save_game():
    """Сохраняет состояние игры."""
    with open("savegame.json", "w") as f:
        json.dump(player, f)
    print("Игра успешно сохранена.")

def load_game():
    """Загружает сохраненное состояние игры."""
    global player
    if os.path.exists("savegame.json"):
        with open("savegame.json", "r") as f:
            player = json.load(f)
        print("Игра успешно загружена.")
    else:
        print("Сохраненная игра не найдена.")

def show_inventory():
    """Показывает инвентарь игрока."""
    print("Инвентарь:")
    if not player["inventory"]:
        print("Пусто")
    else:
        for item in player["inventory"]:
            print(f"- {item}")

def move(direction):
    """Перемещает игрока между локациями."""
    current_location = locations[player["location"]]
    if direction in current_location["directions"]:
        player["location"] = current_location["directions"][direction]
        print(f"Вы переместились в {player['location']}.")
    else:
        print("Вы не можете пойти в эту сторону.")

def pick_item(item):
    """Добавляет предмет в инвентарь."""
    player["inventory"].append(item)
    print(f"Вы подобрали {item}.")

def battle(monster_name):
    """Обрабатывает бой с монстром."""
    monster = monsters[monster_name]
    print(f"Вы встретили {monster_name}!")
    while player["hp"] > 0 and monster["hp"] > 0:
        print(f"Ваше здоровье: {player['hp']} | Здоровье {monster_name}: {monster['hp']}")
        action = input("Выберите действие (атака/защита/использовать предмет): ").lower()
        if action == "атака":
            damage = random.randint(1, player["damage"])
            monster["hp"] -= damage
            print(f"Вы нанесли {damage} урона {monster_name}.")
        elif action == "защита":
            print("Вы защищаетесь.")
        elif action == "использовать предмет":
            item = input("Какой предмет вы хотите использовать? ")
            if item in player["inventory"]:
                if item == "Зелье здоровья":
                    player["hp"] += 20
                    print("Вы восстановили 20 HP.")
                    player["inventory"].remove(item)
                else:
                    print("Этот предмет нельзя использовать в бою.")
            else:
                print("У вас нет такого предмета.")
        else:
            print("Неверное действие.")

        if monster["hp"] > 0:
            damage = random.randint(1, monster["damage"])
            player["hp"] -= damage
            print(f"{monster_name} нанес вам {damage} урона.")

    if player["hp"] <= 0:
        print("Вы погибли. Игра окончена.")
        exit()
    else:
        print(f"Вы победили {monster_name}!")
        reward = random.choice(["Золото", "Опыт", "Редкий предмет"])
        print(f"Вы получили {reward}.")

def main():
    """Основная функция игры."""
    print("Добро пожаловать в текстовую RPG!")
    while True:
        location = locations[player["location"]]
        print("\n" + location["description"])
        if location["items"]:
            print(f"На земле вы видите: {', '.join(location['items'])}")
            action = input("Хотите подобрать предмет? (да/нет): ").lower()
            if action == "да":
                pick_item(location["items"].pop(0))
        if location["monsters"]:
            if random.random() < 0.5:  # Вероятность встречи монстра
                battle(random.choice(location["monsters"]))
        print("Куда вы хотите пойти?")
        for direction, loc in location["directions"].items():
            print(f"{direction.capitalize()} - {loc}")
        direction = input("Введите направление: ").lower()
        move(direction)

if __name__ == "__main__":
    if os.path.exists("savegame.json"):
        load = input("Загрузить сохраненную игру? (да/нет): ").lower()
        if load == "да":
            load_game()
    main()
