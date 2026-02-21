import datetime
import json
import os
import time
import threading

class Event:
    def __init__(self, id, title, description, date, time, notification_minutes):
        self.id = id
        self.title = title
        self.description = description
        self.date = date
        self.time = time
        self.notification_minutes = notification_minutes
    
    def get_datetime(self):
        dt_str = f"{self.date} {self.time}"
        return datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M")

class CalendarApp:
    def __init__(self, storage_file="events.json"):
        self.storage_file = storage_file
        self.events = []
        self.next_id = 1
        self.running = True
        self.load_events()
        
    def load_events(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.events = []
                    for event_data in data['events']:
                        event = Event(
                            event_data['id'],
                            event_data['title'],
                            event_data['description'],
                            event_data['date'],
                            event_data['time'],
                            event_data['notification_minutes']
                        )
                        self.events.append(event)
                    self.next_id = data.get('next_id', 1)
            except:
                print("Ошибка при загрузке событий. Создан новый список.")
                self.events = []
                self.next_id = 1
        else:
            self.events = []
            self.next_id = 1
    
    def save_events(self):
        events_list = []
        for event in self.events:
            events_list.append({
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'date': event.date,
                'time': event.time,
                'notification_minutes': event.notification_minutes
            })
        
        data = {
            'events': events_list,
            'next_id': self.next_id
        }
        
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_event(self):
        print("\n" + "="*50)
        print("ДОБАВЛЕНИЕ НОВОГО СОБЫТИЯ")
        print("="*50)
        
        title = input("Название события: ").strip()
        if not title:
            print("Название не может быть пустым!")
            return
        
        description = input("Описание (необязательно): ").strip()
        
        while True:
            date_str = input("Дата (ГГГГ-ММ-ДД): ").strip()
            try:
                datetime.datetime.strptime(date_str, "%Y-%m-%d")
                break
            except ValueError:
                print("Неверный формат даты. Используйте ГГГГ-ММ-ДД")
        
        while True:
            time_str = input("Время (ЧЧ:ММ): ").strip()
            try:
                datetime.datetime.strptime(time_str, "%H:%M")
                break
            except ValueError:
                print("Неверный формат времени. Используйте ЧЧ:ММ")
        
        while True:
            try:
                notification = int(input("Уведомить за (минут до события): "))
                if notification >= 0:
                    break
                else:
                    print("Введите положительное число")
            except ValueError:
                print("Введите целое число")
        
        event = Event(
            self.next_id,
            title,
            description,
            date_str,
            time_str,
            notification
        )
        
        self.events.append(event)
        self.next_id += 1
        self.save_events()
        print(f"\n✓ Событие '{title}' успешно добавлено!")
    
    def list_events(self):
        if not self.events:
            print("\nНет запланированных событий.")
            return
        
        print("\n" + "="*50)
        print("СПИСОК ВСЕХ СОБЫТИЙ")
        print("="*50)
        
        sorted_events = sorted(self.events, key=lambda e: e.get_datetime())
        
        for event in sorted_events:
            print(f"\nID: {event.id}")
            print(f" Время события: {event.date} {event.time}")
            print(f" Заголовок: {event.title}")
            if event.description:
                print(f" Описание: {event.description}")
            print(f" Уведомление за {event.notification_minutes} мин.")
            print("-"*30)
    
    def check_notifications(self):
        while self.running:
            now = datetime.datetime.now()
            
            for event in self.events:
                event_dt = event.get_datetime()
                notification_time = event_dt - datetime.timedelta(minutes=event.notification_minutes)
                
                if notification_time <= now < event_dt:
                    time_diff = (event_dt - now).total_seconds() / 60
                    if time_diff <= event.notification_minutes:
                        self.show_notification(event, time_diff)
            
            time.sleep(60)
    
    def show_notification(self, event, minutes_until):
        if minutes_until >= 1:
            minutes_str = f"{int(minutes_until)} мин."
        else:
            minutes_str = "менее 1 мин."
        
        print("\n" + "="*50)
        print(" УВЕДОМЛЕНИЕ О СОБЫТИИ ")
        print("="*50)
        print(f"Событие: {event.title}")
        if event.description:
            print(f"Описание: {event.description}")
        print(f"Время: {event.date} {event.time}")
        print(f"До начала: {minutes_str}")
        print("="*50 + "\n")
    
    def display_menu(self):
        print("\n" + "="*50)
        print("КАЛЕНДАРЬ СОБЫТИЙ")
        print("="*50)
        print("1. Просмотреть все события")
        print("2. Добавить событие")
        print("3. Выйти")
        print("="*50)
    
    def run(self):
        notification_thread = threading.Thread(target=self.check_notifications)
        notification_thread.daemon = True
        notification_thread.start()
        
        print("\nДобро пожаловать в Календарь событий!")
        print("Приложение будет уведомлять вас о предстоящих событиях.")
        
        while True:
            self.display_menu()
            
            choice = input("\nВыберите действие (1-3): ").strip()
            
            if choice == '1':
                self.list_events()
            elif choice == '2':
                self.add_event()
            elif choice == '3':
                print("\nДо свидания!")
                self.running = False
                break
            else:
                print("\nНеверный выбор. Пожалуйста, выберите 1-3.")
            
            if choice != '3':
                input("\nНажмите Enter для продолжения...")

def main():
    app = CalendarApp()
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\nПриложение остановлено пользователем.")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")

if __name__ == "__main__":
    main()