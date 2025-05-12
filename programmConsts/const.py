from enum import Enum

class CaseStatusGuids(Enum):
    """GUID статусов кейсов"""
    NEW = "91e27415-08ea-4078-b376-3655abbfa284"  #новая 
    UNDER_REVIEW = "5b6a3553-6d60-4b55-9fa5-8ce094d95009" #На рассмотрении
    ACCEPTED = "12ad9fa2-dac8-46dd-b01f-7ea309e1f150" #принята в работу
    IN_PROGRESS = "6e4c9f6a-7c06-4d21-8620-3f0bf8bd15e5" #в процессе ремонта
    POSTPONED = "b05bf8fc-cc2d-40c1-908f-defde4d213d4" #отложена
    COMPLETED = "944bd95c-47ce-4bf9-943b-6a9e45f6a761" #выполнена
    REJECTED = "0bc7387e-5c13-460b-8dca-4cdc1a8a9b2c" #отклонена

class SysRoleGuids(Enum):
    """GUID ролей пользователей"""
    ADMINISTRATOR = "57252a05-b288-4e13-8dfc-183c89295d40" # Администратор
    MODERATOR = "42c07419-7367-414e-89c8-c4dd37e3017a" # Модератор заявок
    USER = "e82ea4bb-6d94-4b01-a321-5aa915204a04" # Пользователь
    EXECUTOR = "cd40e20c-d646-4eb6-99bf-4f9348cdc854" # Подрядчик

class ConfigurationConst(Enum):
    """Конфигурационные константы"""
    EMPTY_LOCATION = "Адрес не указан пользователем"