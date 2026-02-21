import unittest
import datetime
import json
import os
import tempfile
from main import CalendarApp, Event

class TestCalendar(unittest.TestCase):
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.app = CalendarApp(self.temp_file.name)
    
    def tearDown(self):
        os.unlink(self.temp_file.name)
    
    #1. Тест создаия события
    def test_1_create_event(self):
        event = Event(1, "Тест", "Описание", "2026-02-21", "15:30", 30)
        self.assertEqual(event.title, "Тест")
        self.assertEqual(event.description, "Описание")
        self.assertEqual(event.date, "2026-02-21")
        self.assertEqual(event.time, "15:30")
        self.assertEqual(event.notification_minutes, 30)
        
        dt = event.get_datetime()
        self.assertEqual(dt.year, 2026)
        self.assertEqual(dt.month, 2)
        self.assertEqual(dt.day, 21)
        self.assertEqual(dt.hour, 15)
        self.assertEqual(dt.minute, 30)
    
    #2. Тест добавления события
    def test_2_add_event(self):
        self.app.events.append(Event(1, "Встреча", "", "2026-02-21", "15:00", 15))
        self.app.next_id = 2
        self.app.save_events()
        
        self.assertEqual(len(self.app.events), 1)
        self.assertEqual(self.app.events[0].title, "Встреча")
        self.assertEqual(self.app.next_id, 2)
    
    #3. Тест загрузки событий
    def test_3_load_events(self):
        data = {
            'events': [{
                'id': 1,
                'title': 'Загруженное',
                'description': '',
                'date': '2026-02-21',
                'time': '14:00',
                'notification_minutes': 45
            }],
            'next_id': 2
        }
        
        with open(self.temp_file.name, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        
        app2 = CalendarApp(self.temp_file.name)
        
        self.assertEqual(len(app2.events), 1)
        self.assertEqual(app2.events[0].title, "Загруженное")
        self.assertEqual(app2.next_id, 2)
    
    #4. Тест на пустое событие
    def test_4_empty_events(self):
        self.assertEqual(len(self.app.events), 0)
        self.app.list_events() 
    
    #5. Тест проверки уведомлений
    def test_5_notification_time(self):
        now = datetime.datetime.now()
        event_time = now + datetime.timedelta(minutes=30)
        
        event = Event(1, "Тест", "", 
                     event_time.strftime("%Y-%m-%d"),
                     event_time.strftime("%H:%M"), 
                     15)
        
        event_dt = event.get_datetime()
        notification_time = event_dt - datetime.timedelta(minutes=15)
        
        self.assertLess(notification_time, event_dt)
        self.assertEqual(event.notification_minutes, 15)
    
    #1. Тест сортировки событий
    def test_6_sort_events(self):
        self.app.events = [
            Event(1, "Позднее", "", "2026-02-21", "09:00", 10),
            Event(2, "Раннее", "", "2025-02-21", "12:00", 30),
            Event(3, "Среднее", "", "2025-02-21", "18:00", 20)
        ]
        
        sorted_events = sorted(self.app.events, key=lambda e: e.get_datetime())
        
        self.assertEqual(sorted_events[0].title, "Раннее")
        self.assertEqual(sorted_events[1].title, "Среднее")
        self.assertEqual(sorted_events[2].title, "Позднее")

if __name__ == '__main__':
    print("\n" + "="*50)
    print("ЗАПУСК ТЕСТОВ")
    print("="*50)
    unittest.main(argv=[''], verbosity=2, exit=False)
    print("="*50)