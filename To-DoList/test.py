import unittest
from todo import TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.manager = TaskManager()
    
    #Создаём задачу с title Тест и description Описание
    def test_add_task(self):
        task = self.manager.add_task("Тест", "Описание")
        self.assertEqual(task.title, "Тест")
        self.assertEqual(task.description, "Описание")
        self.assertEqual(len(self.manager.get_all_tasks()), 1)
    
    #Получаем таск по его id -> task = self.manager.get_task(1)
    def test_get_task(self):
        self.manager.add_task("Тест")
        task = self.manager.get_task(1)
        self.assertIsNotNone(task)
        self.assertEqual(task.title, "Тест")
        self.assertIsNone(self.manager.get_task(999))

    #Изменяем конкретный таск полученный по id. Меняем title и description -> result = self.manager.update_task(1, "Новое название", "Новое описание")
    def test_update_task(self):
        self.manager.add_task("Старое название")
        result = self.manager.update_task(1, "Новое название", "Новое описание")
        self.assertTrue(result)
        
        #Проверка нового таска
        task = self.manager.get_task(1)
        self.assertEqual(task.title, "Новое название")
        self.assertEqual(task.description, "Новое описание")
        
        #Проверка на попытку обновления несуществущей задачи
        result = self.manager.update_task(999, "Название")
        self.assertFalse(result)
    
    #Получаем таск по его id -> удаляем, также проверяем на несуществующую задачу
    def test_delete_task(self):
        self.manager.add_task("Задача")
        self.assertEqual(len(self.manager.get_all_tasks()), 1)
        
        result = self.manager.delete_task(1)
        self.assertTrue(result)
        self.assertEqual(len(self.manager.get_all_tasks()), 0)
        
        result = self.manager.delete_task(999)
        self.assertFalse(result)
    
    #Выполняем полученный таск методом mark_completed(1), проверка на выполненную задчу -> self.assertTrue(self.manager.get_task(1).completed), Проверка на попытку выполнить несуществующую задачу -> result = self.manager.mark_completed(999)
    def test_mark_completed(self):
        self.manager.add_task("Задача")
        
        result = self.manager.mark_completed(1)
        self.assertTrue(result)
        self.assertTrue(self.manager.get_task(1).completed)
        
        result = self.manager.mark_completed(999)
        self.assertFalse(result)
    
    # Создание задачи -> Пометка как выполненная -> пометка как не выполненная. Проверки на несуществующую задачу и на выполненную задачу -> self.assertFalse(self.manager.get_task(1).completed) и result = self.manager.mark_incomplete(999)
    def test_mark_incomplete(self):
        self.manager.add_task("Задача")
        self.manager.mark_completed(1)
        
        result = self.manager.mark_incomplete(1)
        self.assertTrue(result)
        self.assertFalse(self.manager.get_task(1).completed)
        
        result = self.manager.mark_incomplete(999)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()

#запуск: py -m unittest test.py -v

