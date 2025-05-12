from enum import Enum

class YesNoAnswerMarkupText(Enum):
    YES = "да"
    NO = "нет"

class MainMenuMarkupText(Enum):
    SEND_REPORT = '📝 Подать заявку'
    MY_REPORTS = '📊 Мои заявки'
    HELP = 'ℹ️ Справка'
    CONTACTS = '📞 Контакты'

class AdministratorMenuMarkupText(Enum):
    STATISTICS = '📊 Статистика'
    REPORTS = '📝 Заявки'
    USERS = '👥 Пользователи'
    SETTINGS = '⚙️ Настройки'

class ModeratorMenuMarkupsText(Enum):
     STATISTICS = '📊 Статистика'
     ACTIVE_REPORTS = '📝 Активные заявки'
     IN_PROGRESS_REPORTS = '✅ Заявки в работе'
     COMPLAINT = '❗️ Жалобы'

class ExecutorMenuMarkupsText(Enum):
     STATISTICS = '📊 Статистика'
     ACTIVE_REPORTS = '📝 Активные заявки'
     WORK_TIME = '📅 График работ '
     MODERATOR_CALL = '📞 Связь с модератором '

class LocationMarkupText(Enum):
    GET_LOCATION = '📍 Отправить геолокацию'