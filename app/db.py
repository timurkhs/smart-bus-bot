import sqlite3
import time
import uuid
from datetime import datetime, timedelta
from enum import Enum

from programmConsts.const import CaseStatusGuids, SysRoleGuids
from models.caseModel import Case

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

    def get_case_count(self, status_id: str = None) -> int:
        """
        Возвращает количество записей в таблице Case с возможностью фильтрации по статусу
        
        :param status_id: ID статуса (из CaseStatusGuids) для фильтрации, необязательный
        :return: Количество записей (int)
        """
        with self.connection:
            if status_id:
                self.cursor.execute("SELECT COUNT(*) FROM `Case` WHERE `StatusId` = ?", (status_id,))
            else:
                self.cursor.execute("SELECT COUNT(*) FROM `Case`")
            return self.cursor.fetchone()[0]


    def create_case(
        self,
        code: str,
        description: str,
        addres: str,
        coordinator_id: str | None,
        owner_id: str | None,
        image: str | None,
        location: str | None,
        initiator_id: str,
        name: str
    ) -> str:
        """
        Создает новую запись в таблице Case (обращение на ремонт).
        """
        with self.connection:
            case_id = str(uuid.uuid4())
            status_id = CaseStatusGuids.NEW.value  # Статус по умолчанию - "Новый"
            
            self.cursor.execute("""
                INSERT INTO `Case` (
                    `Id`, `Code`, `Description`, `Addres`, `StatusId`,
                    `CoordinatorId`, `OwnerId`, `Image`, `Location`,
                    `InitiatorId`, `Name`
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                case_id, code, description, addres, status_id,
                coordinator_id, owner_id, image, location,
                initiator_id, name
            ))
            
            return case_id
    def get_user_id_by_telegram_id(self, telegram_id: int) -> str | None:
        """
        Возвращает UUID пользователя (Id из SysAdminUnit) по его Telegram ID.
        """
        with self.connection:
            self.cursor.execute(
                "SELECT `Id` FROM `SysAdminUnit` WHERE `TelegramId` = ?", 
                (telegram_id,)
            )
            result = self.cursor.fetchone()
            return result[0] if result else None
        
    def get_all_cases(self) -> list[Case]:
        """
        Получает все обращения из базы данных с подставленными именами из связанных таблиц.
        
        Returns:
            list[Case]: Список объектов Case с заполненными именами
        """
        with self.connection:
            self.cursor.execute("""
                SELECT 
                    c.Id,
                    c.Code,
                    c.Description,
                    c.Addres,
                    cs.Name AS status_name,
                    coord.Name AS coordinator_name,
                    owner.Name AS owner_name,
                    c.Image,
                    c.Location,
                    init.Name AS initiator_name,
                    c.Name
                FROM 
                    Case c
                LEFT JOIN CaseStatus cs ON c.StatusId = cs.Id
                LEFT JOIN SysAdminUnit coord ON c.CoordinatorId = coord.Id
                LEFT JOIN SysAdminUnit owner ON c.OwnerId = owner.Id
                LEFT JOIN SysAdminUnit init ON c.InitiatorId = init.Id
            """)
            
            cases = []
            for row in self.cursor.fetchall():
                case = Case(
                    id=row[0],
                    code=row[1],
                    description=row[2],
                    addres=row[3],
                    status_name=row[4],
                    coordinator_name=row[5],
                    owner_name=row[6],
                    image=row[7],
                    location=row[8],
                    initiator_name=row[9],
                    name=row[10]
                )
                cases.append(case)
                
            return cases


    def get_cases_by_initiator(self, initiator_id: str) -> list[Case]:
        """
        Получает обращения конкретного инициатора из базы данных с подставленными именами из связанных таблиц.
        
        Args:
            initiator_id: UUID инициатора, чьи заявки нужно получить
            
        Returns:
            list[Case]: Список объектов Case с заполненными именами
        """
        with self.connection:
            self.cursor.execute("""
                SELECT 
                    c.Id,
                    c.Code,
                    c.Description,
                    c.Addres,
                    cs.Name AS status_name,
                    coord.Name AS coordinator_name,
                    owner.Name AS owner_name,
                    c.Image,
                    c.Location,
                    init.Name AS initiator_name,
                    c.Name
                FROM 
                    "Case" c
                LEFT JOIN CaseStatus cs ON c.StatusId = cs.Id
                LEFT JOIN SysAdminUnit coord ON c.CoordinatorId = coord.Id
                LEFT JOIN SysAdminUnit owner ON c.OwnerId = owner.Id
                LEFT JOIN SysAdminUnit init ON c.InitiatorId = init.Id
                WHERE c.InitiatorId = ?
            """, (initiator_id,))
            
            cases = []
            for row in self.cursor.fetchall():
                case = Case(
                    id=row[0],
                    code=row[1],
                    description=row[2],
                    addres=row[3],
                    status_name=row[4],
                    coordinator_name=row[5],
                    owner_name=row[6],
                    image=row[7],
                    location=row[8],
                    initiator_name=row[9],
                    name=row[10]
                )
                cases.append(case)
                
            return cases
        
    def get_case_by_id(self, case_id: str) -> Case | None:
        """Получает полные данные о заявке по ID"""
        with self.connection:
            self.cursor.execute("""
                SELECT 
                    c.Id, c.Code, c.Description, c.Addres,
                    cs.Name AS status_name, coord.Name AS coordinator_name,
                    owner.Name AS owner_name, c.Image, c.Location,
                    init.Name AS initiator_name, c.Name
                FROM "Case" c
                LEFT JOIN CaseStatus cs ON c.StatusId = cs.Id
                LEFT JOIN SysAdminUnit coord ON c.CoordinatorId = coord.Id
                LEFT JOIN SysAdminUnit owner ON c.OwnerId = owner.Id
                LEFT JOIN SysAdminUnit init ON c.InitiatorId = init.Id
                WHERE c.Id = ?
            """, (case_id,))
            
            row = self.cursor.fetchone()
            if not row:
                return None
                
            return Case(
                id=row[0], code=row[1], description=row[2],
                addres=row[3], status_name=row[4], coordinator_name=row[5],
                owner_name=row[6], image=row[7], location=row[8],
                initiator_name=row[9], name=row[10]
        )