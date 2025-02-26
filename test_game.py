import unittest
import os
import json
from unittest.mock import patch, mock_open
from banalRPG.py import player, locations, move, pick_item, battle, save_game, load_game  # Замените banalRPG.py на имя файла игры, если переименуете его

class TestGame(unittest.TestCase):
    def setUp(self):
        # Сбрасываем состояние игрока перед каждым тестом
        player.update({
            "name": "Герой",
            "hp": 100,
            "damage": 10,
            "inventory": [],
            "location": "Лес"
        })

    # Тесты перемещения
    def test_move_valid_direction(self):
        move("север")
        self.assertEqual(player["location"], "Пещера")

    def test_move_invalid_direction(self):
        with patch('builtins.print') as mocked_print:
            move("юг")
            mocked_print.assert_called_with("Вы не можете пойти в эту сторону.")

    # Тесты подбора предметов
    def test_pick_item(self):
        initial_items = locations["Лес"]["items"].copy()
        pick_item(initial_items[0])
        self.assertIn(initial_items[0], player["inventory"])
        self.assertEqual(len(locations["Лес"]["items"]), len(initial_items)-1)

    # Тесты системы сохранения/загрузки
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"hp": 50}')
    def test_load_game(self, mock_file, mock_exists):
        load_game()
        self.assertEqual(player["hp"], 50)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_game(self, mock_file):
        save_game()
        mock_file().write.assert_called_with(json.dumps(player))

    # Тесты боевой системы (с моком случайных чисел)
    @patch('random.randint', side_effect=[5, 3])  # Игрок наносит 5 урона, монстр 3
    def test_battle_win(self, mock_random):
        with patch('builtins.input', side_effect=['атака']):
            battle("Волк")
            self.assertGreater(player["hp"], 0)

    @patch('random.randint', side_effect=[1, 20])  # Монстр убивает игрока
    def test_battle_lose(self, mock_random):
        with patch('builtins.input', side_effect=['атака']), \
             self.assertRaises(SystemExit):
            battle("Дракон")

    # Тест использования предмета в бою
    def test_use_item_in_battle(self):
        player["inventory"] = ["Зелье здоровья"]
        with patch('builtins.input', side_effect=['использовать предмет', 'Зелье здоровья']):
            battle("Волк")
            self.assertEqual(player["hp"], 120)
            self.assertNotIn("Зелье здоровья", player["inventory"])

if __name__ == '__main__':
    unittest.main()
