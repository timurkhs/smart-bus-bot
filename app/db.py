import sqlite3
import time
import uuid
from datetime import datetime, timedelta
from enum import Enum

from programmConsts.const import CaseStatusGuids, SysRoleGuids

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
            acces = 1
            blocedTime = 0
            startBlockedData = None

            self.cursor.execute("""INSERT INTO `SysAdminUnit` 
                                    (`Id`, `TelegramId`,`Name`, `RegistrationDate`, `CountReport`, 
                                    `CountApprovalRecord`, `Acces`, `BlocedTime`, `StartBlockedDate`, `Notification`) 
                                    VALUES (?,?,?,?,?,?,?,?,?,? )""", (id, telegramId, 
                                                                        user_name, registrationDate, 
                                                                        countReport, countApprocalRecord,
                                                                        acces, blocedTime, 
                                                                        startBlockedData, notification))
            self.assign_role_to_user(id)

            return id

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
            if acces == 0 or (
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
                    SET BlocedTime = 0, StartBlockedDate = NULL, Acces = 1
                    WHERE TelegramId = ?
                """, (telegramId,))
                
            return True
    
    #Выдача роли пользователю.
    def assign_role_to_user(self, user_id, role_id=None):
        if role_id is None:
            role_id = SysRoleGuids.USER.value
        
        with self.connection:
            return self.cursor.execute("""INSERT INTO `SysAdminUnitInRole` 
                            (`Id`, `SysAdminUnitId`, `SysRoleId`) 
                            VALUES (?, ?, ?)""", 
                            (str(uuid.uuid4()), user_id, role_id))


    #Получить роли пользователя по его telegrammId
    def get_user_role_ids(self, telegramId):
        with self.connection:
            self.cursor.execute("""
                SELECT r.Id
                FROM SysAdminUnit u
                JOIN SysAdminUnitInRole ur ON u.Id = ur.SysAdminUnitId
                JOIN SysRole r ON ur.SysRoleId = r.Id
                WHERE u.TelegramId = ?
            """, (telegramId,))
            
            return [row[0] for row in self.cursor.fetchall()]
        
    from datetime import datetime, timedelta

    
    #выполняет блокировку пользователя
    def block_user(self, id, days_to_block):
        if days_to_block <= 0:
            raise ValueError("Дни блокировки должны быть положительным числом")
        
        with self.connection:
            # Конвертируем дни в секунды
            seconds_to_block = days_to_block * 24 * 60 * 60
            block_start_date = datetime.now()
            
            # Обновляем запись пользователя
            self.cursor.execute("""
                UPDATE SysAdminUnit
                SET Acces = 0,
                    BlocedTime = ?,
                    StartBlockedDate = ?
                WHERE Id = ?
            """, (seconds_to_block, block_start_date, id))
            
            # Проверяем, был ли обновлен пользователь
            return self.cursor.rowcount > 0


