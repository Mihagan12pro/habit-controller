from repositories import habits_repository as habits_rep, users_repository as users_rep, progress_repository as progress_rep
import database as data_access

"""
Файл внедрения зависимостей
"""

database =  data_access.get_db()#Объект базы данных

users_repository = users_rep.UsersRepository(database = database)
habits_repository = habits_rep.HabitsRepository(database = database)
progress_repository = progress_rep.ProgressRepository(database = database)




