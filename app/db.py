import sqlite3
import time
import uuid
from datetime import datetime, timedelta


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
    
    # Выполняет добавление пользователя в таблицу SysAdminUnit.
    def add_user(self, telegramId, user_name, notification):
        with self.connection:
            id = str(uuid.uuid4())
            registrationDate = datetime.now()
            countReport = 0
            countApprocalRecord = 0
            acces = True
            blocedTime = 0
            startBlockedData = None

            return self.cursor.execute("""INSERT INTO `SysAdminUnit` 
                                       (`Id`, `TelegramId`,`Name`, `RegistrationDate`, `CountReport`, 
                                       `CountApprovalRecord`, `Acces`, `BlocedTime`, `StartBlockedDate`, `Notification`) 
                                       VALUES (?,?,?,?,?,?,?,?,?,? )""", (id, telegramId, 
                                                                          user_name, registrationDate, 
                                                                          countReport, countApprocalRecord,
                                                                          acces, blocedTime, 
                                                                          startBlockedData, notification))
    # Выполняет проверку на существование пользователя.
    def user_exist(self, telegramId):
        with self.connection: 
            result = self.cursor.execute("SELECT * FROM `SysAdminUnit` WHERE `TelegramId` = ?", (telegramId,)).fetchall()
            return bool(len(result))
    
    #Проверка на доступ пользователя к БД.
    def check_user_access(self, telegramId):
        with self.connection:
            # Получаем данные пользователя
            self.cursor.execute("""
                SELECT Acces, BlocedTime, StartBlockedDate 
                FROM SysAdminUnit 
                WHERE TelegramId = ?
            """, (telegramId,))
            
            result = self.cursor.fetchone()
            
            if not result:
                return False  # Пользователь не найден
                
            acces, bloced_time, start_blocked_date = result
            
            # Если доступ явно запрещен (Acces=False) или время блокировки еще не истекло
            if not acces or (
                bloced_time > 0 
                and start_blocked_date is not None 
                and datetime.now() < start_blocked_date + timedelta(seconds=bloced_time)
            ):
                return False
                
            # Если дошли сюда — доступ разрешен
            # Если была блокировка, но время истекло — снимаем её
            if bloced_time > 0 and start_blocked_date is not None:
                self.cursor.execute("""
                    UPDATE SysAdminUnit 
                    SET BlocedTime = 0, StartBlockedDate = NULL 
                    WHERE TelegramId = ?
                """, (telegramId,))
                
            return True
    
    

