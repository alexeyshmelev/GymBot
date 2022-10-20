import os
import datetime as dt
import numpy as np
import mysql.connector
import logging
from typing import Dict
from telegram import __version__ as TG_VER


cnx = mysql.connector.connect(user='###your_user###', password='###your_password###',
                              host='mysql', # because we use container name as a host
                              database='sport_club_mod')
cursor = cnx.cursor()

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

############################################################################# bot code ####################################################################################

CHOOSING, SELECT_DATE, SELECT_GYM, SELECT_TIME, SELECT_MAINCOACH, SELECT_COACH, SELECT_SPORTSMEN, SELECT_TRAINER, INSERT_TRAINING = 0, 1, 2, 3, 4, 5, 6, 7, 8
SELECT_DEL_TRAINING, CHOOSE_COACH, CHANGE_TRAINING, DELETE_OR_ADD_COACH, SET_NEW_GYM_SCHEDULE, SET_FINISH_WORKING, SET_START_WORKING, UPDATE_GYM_SCHEDULE = 20, 21, 22, 23, 24, 25, 26, 27

all_available_commands = {
    'Sportsman' : [["Show training schedule"], ["View coaches", "View your doctor", "View your main coach"]],
    'Coach' : [["Show list of sportsmens"], ["Show training schedule"]],
    'Main Coach' : [["Schedule training"], ["Show training schedule"], ["Delete the training"], ["Change coaches in training"]],
    'Sport Doctor' : [["Check Sportsmen"], ["Show sportsmen's training schedule"]],
    'Manager' : [["Set gym schedule"], ["Recruitment"]]
}


def get_job_title_keyboard(job_title):
    if job_title == 'Sportsman':
        reply_keyboard = all_available_commands[job_title]
    elif job_title == 'Coach':
        reply_keyboard = all_available_commands[job_title]
    elif job_title == 'Main Coach':
        reply_keyboard = all_available_commands[job_title]
    elif job_title == 'Sport Doctor':
        reply_keyboard = all_available_commands[job_title]
    elif job_title == 'Manager':
        reply_keyboard = all_available_commands[job_title]

    
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    return markup


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    username = update.message.from_user["username"]
    mysql_query = ("select tablename from ( "
                "select 'Coach' as tablename, tgname from Coach "
                "union all "
                "select 'Sportsman' as tablename, tgname from Sportsmen "
                "union all "
                "select 'Main Coach' as tablename, tgname from MainCoach "
                "union all "
                "select 'Sport Doctor' as tablename, tgname from SportDoctor "
                f") x where tgname = '{username}'")
    cursor.execute(mysql_query)

    for job_title in cursor:
        pass
    context.user_data['role'] = job_title[0]

    if username == 'ami_deamon': # manager account
        markup = get_job_title_keyboard('Manager')
        await update.message.reply_text(f"Welcome to our exclusive superduper gym that is managed by Dimas and Alex! \nYou were signed in as Manager", reply_markup=markup)
    else:
        markup = get_job_title_keyboard(job_title[0])
        await update.message.reply_text(f"Welcome to our exclusive superduper gym that is managed by Dimas and Alex! \nYou were signed in as {job_title[0]}", reply_markup=markup)

    return CHOOSING
    
async def base_command_performer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    req = update.message.text
    # For coaches
    if req == "Show list of sportsmens":
        await show_list_of_sportsmen(update)
    if req == "Schedule training":
        await select_date(update, context)
        return SELECT_GYM
    if req == "Delete the training":
        await get_training_for_delete(update, context)
        return SELECT_DEL_TRAINING
    if req == "Change coaches in training":
        await get_training_for_change(update, context)
        return DELETE_OR_ADD_COACH
    # For sportsmen
    if req == "View coaches":
        await view_coaches(update)
    if req == "View your main coach":
        await view_main_coach(update)
    if req == "View your doctor":
        await view_doctor(update)
    if req == "Show training schedule":
        await show_training_schedule(update, context)
    # For doctor
    if req == "Check Sportsmen":
        await check_sportsmen_for_doctor(update)
    if req == "Show sportsmen's training schedule":
        await view_schedule_for_doctor(update)
    # For manager
    if req == "Set gym schedule":
        await set_gym_schedule(update, context)
        return SET_START_WORKING
    if req == "Recruitment":
        await choose_recruit(update, context)
        return SET_START_WORKING


async def choose_recruit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    job_titles = ['Sportsmen', 'MainCoach', 'Coach', 'Sport Doctor']
    keyboard = [[InlineKeyboardButton(i, callback_data=i)] for i in job_titles]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"Who do you want to add?", reply_markup=reply_markup)



async def set_gym_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mysql_query = (f"SELECT Number FROM Gym")
    cursor.execute(mysql_query)
    numbersGym = []
    for i in cursor:
        numbersGym.append(i[0])

    keyboard = [[InlineKeyboardButton(i, callback_data=i)] for i in numbersGym]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"What gym schedule do you want change?", reply_markup=reply_markup)
    

async def set_gym_new_start_working(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    context.user_data["gym_number"] = query.data
    await query.edit_message_text(text=f"Selected gym: {query.data}")

    hours = [(dt.time(7+i, 0, 0)) for i in range(7)]
    keyboard = [[InlineKeyboardButton(i.strftime('%H:%M'), callback_data=i.strftime('%H:%M'))] for i in hours]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(f"Select new time of start working:", reply_markup=reply_markup)

    return SET_FINISH_WORKING


async def set_gym_new_finish_working(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    context.user_data["start_time"] = query.data
    await query.edit_message_text(text=f"Selected start working time: {query.data}")

    hours = [(dt.time(16 + i, 0, 0)) for i in range(7)]
    keyboard = [[InlineKeyboardButton(i.strftime('%H:%M'), callback_data=i.strftime('%H:%M'))] for i in hours]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(f"Select new time of start working:", reply_markup=reply_markup)
    
    return UPDATE_GYM_SCHEDULE
    
async def update_gym_new_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    context.user_data["finish_time"] = query.data
    await query.edit_message_text(text=f"Selected finish working time: {query.data}")

    mysql_query = (f"UPDATE Gym SET StartTimeWorking = '{context.user_data['start_time']}:00', FinishTimeWorking = '{context.user_data['finish_time']}:00' WHERE Gym.Number = {context.user_data['gym_number']}")
    cursor.execute(mysql_query)

    await query.message.reply_text(f"Schedule of working in the gym {context.user_data['gym_number']} was changed")
    cnx.commit()
    return ConversationHandler.END


def insert_training_sql(data):
    global cursor
    for s in data['selected_sportsman'].split('&'):
        if data['selected_trainer'] != 'NULL' and data['selected_main_coach'] != 'NULL':
            mysql_query = (f"INSERT INTO `Training` (`idTraining`, `Gym_Number`, `StartTime`, `FinishTime`, `TrainerInGym_idTrainer`, `Sportsmen_tgname`, `MainCoach_tgname`) VALUES (NULL, '{data['selected_gym']}', '{data['selected_date'] +' '+ data['selected_time'].split(' ')[0]}:00', '{data['selected_date'] +' '+ data['selected_time'].split(' ')[2]}:00', '{data['selected_trainer']}', '{s}', '{data['selected_main_coach']}')")
        elif data['selected_trainer'] == 'NULL' and data['selected_main_coach'] != 'NULL':
            mysql_query = (f"INSERT INTO `Training` (`idTraining`, `Gym_Number`, `StartTime`, `FinishTime`, `TrainerInGym_idTrainer`, `Sportsmen_tgname`, `MainCoach_tgname`) VALUES (NULL, '{data['selected_gym']}', '{data['selected_date'] +' '+ data['selected_time'].split(' ')[0]}:00', '{data['selected_date'] +' '+ data['selected_time'].split(' ')[2]}:00', NULL, '{s}', '{data['selected_main_coach']}')")
        elif data['selected_trainer'] != 'NULL' and data['selected_main_coach'] == 'NULL':
            mysql_query = (f"INSERT INTO `Training` (`idTraining`, `Gym_Number`, `StartTime`, `FinishTime`, `TrainerInGym_idTrainer`, `Sportsmen_tgname`, `MainCoach_tgname`) VALUES (NULL, '{data['selected_gym']}', '{data['selected_date'] +' '+ data['selected_time'].split(' ')[0]}:00', '{data['selected_date'] +' '+ data['selected_time'].split(' ')[2]}:00', '{data['selected_trainer']}', '{s}', NULL)")
        elif data['selected_trainer'] == 'NULL' and data['selected_main_coach'] == 'NULL':
            mysql_query = (f"INSERT INTO `Training` (`idTraining`, `Gym_Number`, `StartTime`, `FinishTime`, `TrainerInGym_idTrainer`, `Sportsmen_tgname`, `MainCoach_tgname`) VALUES (NULL, '{data['selected_gym']}', '{data['selected_date'] +' '+ data['selected_time'].split(' ')[0]}:00', '{data['selected_date'] +' '+ data['selected_time'].split(' ')[2]}:00', NULL, '{s}', NULL)")
        cursor.execute(mysql_query)
    cnx.commit()
    ids = []
    for s in data['selected_sportsman'].split('&'):
        if data['selected_trainer'] != 'NULL' and data['selected_main_coach'] != 'NULL':
            mysql_query = (f"SELECT idTraining from Training WHERE Gym_Number = '{data['selected_gym']}' and StartTime = '{data['selected_date'] +' '+ data['selected_time'].split(' ')[0]}:00' and FinishTime = '{data['selected_date'] +' '+ data['selected_time'].split(' ')[2]}:00' and TrainerInGym_idTrainer = '{data['selected_trainer']}' and Sportsmen_tgname = '{s}' and MainCoach_tgname = '{data['selected_main_coach']}'")
        elif data['selected_trainer'] == 'NULL' and data['selected_main_coach'] != 'NULL':
            mysql_query = (f"SELECT idTraining from Training WHERE Gym_Number = '{data['selected_gym']}' and StartTime = '{data['selected_date'] +' '+ data['selected_time'].split(' ')[0]}:00' and FinishTime = '{data['selected_date'] +' '+ data['selected_time'].split(' ')[2]}:00' and TrainerInGym_idTrainer IS NULL and Sportsmen_tgname = '{s}' and MainCoach_tgname = '{data['selected_main_coach']}'")
        elif data['selected_trainer'] != 'NULL' and data['selected_main_coach'] == 'NULL':
            mysql_query = (f"SELECT idTraining from Training WHERE Gym_Number = '{data['selected_gym']}' and StartTime = '{data['selected_date'] +' '+ data['selected_time'].split(' ')[0]}:00' and FinishTime = '{data['selected_date'] +' '+ data['selected_time'].split(' ')[2]}:00' and TrainerInGym_idTrainer = '{data['selected_trainer']}' and Sportsmen_tgname = '{s}' and MainCoach_tgname IS NULL")
        elif data['selected_trainer'] == 'NULL' and data['selected_main_coach'] == 'NULL':
            mysql_query = (f"SELECT idTraining from Training WHERE Gym_Number = '{data['selected_gym']}' and StartTime = '{data['selected_date'] +' '+ data['selected_time'].split(' ')[0]}:00' and FinishTime = '{data['selected_date'] +' '+ data['selected_time'].split(' ')[2]}:00' and TrainerInGym_idTrainer IS NULL and Sportsmen_tgname = '{s}' and MainCoach_tgname IS NULL")
        cursor.execute(mysql_query)
        for i in cursor:
            ids.append(i[0])
    if data['selected_coach'] != 'NULL':
        for i in ids:
            mysql_query = (f"INSERT INTO `Coach_Training` (`Coach_tgname`, `Training_idTraining`) VALUES ('{data['selected_coach']}', '{i}')")
            cursor.execute(mysql_query)
    cnx.commit()

    
async def show_training_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user["username"]
    if context.user_data['role'] == 'Sportsman':
        mysql_query = (f"SELECT * FROM ((SELECT Training.Gym_Number, Training.StartTime, Training.FinishTime, MainCoach.Name as MainCoach, Coach.Name AS Coach FROM Training JOIN MainCoach JOIN Coach_Training JOIN Coach ON Training.Sportsmen_tgname='{username}' and Training.MainCoach_tgname=MainCoach.tgname and Coach_Training.Training_idTraining=Training.idTraining and Coach_Training.Coach_tgname=Coach.tgname WHERE Training.StartTime > NOW()) UNION ALL (SELECT Training.Gym_Number, Training.StartTime, Training.FinishTime, MainCoach.Name as MainCoach, null AS Coach FROM Training JOIN MainCoach ON Training.Sportsmen_tgname='{username}' and (Training.MainCoach_tgname=MainCoach.tgname OR Training.MainCoach_tgname=null) WHERE Training.StartTime > NOW() and Training.idTraining NOT IN (SELECT Training_idTraining FROM Coach_Training)) UNION ALL (SELECT Training.Gym_Number, Training.StartTime, Training.FinishTime, null as MainCoach, Coach.Name AS Coach FROM Training JOIN Coach_Training JOIN Coach ON Training.Sportsmen_tgname='{username}' and Coach_Training.Training_idTraining=Training.idTraining and Coach_Training.Coach_tgname=Coach.tgname WHERE Training.MainCoach_tgname IS NULL and Training.StartTime > NOW())) x ORDER BY x.StartTime")
        cursor.execute(mysql_query)
        training = []
        fmt1 = '%d %B %H:%M'
        fmt2 = '- %H:%M'
        for i in cursor:
            training.append(f'\nGym number: {i[0]}\n' + ' '.join([i[1].strftime(fmt1), i[2].strftime(fmt2)]) + "\n" + f"Main coach: {i[3] if i[3] else '---'}\n" + f"Coach: {i[4] if i[4] else '---'}")

        training = '\n'.join(training)
        
        await update.message.reply_text(f"Your trainings are: \n{training}")

    if context.user_data['role'] == 'Main Coach':
        mysql_query = (f"SELECT Training.Gym_Number, Training.StartTime, Training.FinishTime, Sportsmen.Name AS SportsmenName FROM Training JOIN Sportsmen ON Training.MainCoach_tgname='{username}' and Training.Sportsmen_tgname = Sportsmen.tgname WHERE Training.StartTime > NOW()")
        cursor.execute(mysql_query)
        training = []
        fmt1 = '%d %B %H:%M'
        fmt2 = '- %H:%M'
        buf = -1
        for i in cursor:
            if buf != i[1]:
                training.append(f'\nGym number: {i[0]}\n' + ' '.join([i[1].strftime(fmt1), i[2].strftime(fmt2)]) + "\n" + f"Sportsmen: {i[3]}; ")
                buf = i[1]
            else:
                training[-1] = training[-1] + f"{i[3]}; "


        training = '\n'.join(training)
        
        await update.message.reply_text(f"Your trainings are: \n{training}")


async def view_coaches(update: Update):
    username = update.message.from_user["username"]
    coaches = []

    mysql_query = (f"SELECT Coach.Name FROM Coach JOIN MainCoach JOIN Sportsmen ON Sportsmen.tgname='{username}' and MainCoach.tgname=Sportsmen.MainCoach_tgname and Coach.MainCoach_tgname=Sportsmen.MainCoach_tgname")
    cursor.execute(mysql_query)
    for i in cursor:
        coaches.append(i[0])

    coaches = '\n'.join(coaches)

    await update.message.reply_text(f"Your coaches are: \n{coaches}")


async def view_main_coach(update: Update):
    username = update.message.from_user["username"]

    mysql_query = (f"SELECT MainCoach.Name FROM Sportsmen JOIN MainCoach ON Sportsmen.tgname='{username}' and Sportsmen.MainCoach_tgname=MainCoach.tgname")
    cursor.execute(mysql_query)
    for i in cursor:
        main_coach = i[0]

    await update.message.reply_text(f"Your main coach is: \n{main_coach}")


async def view_doctor(update: Update):
    username = update.message.from_user["username"]

    mysql_query = (f"SELECT SportDoctor.Name FROM Sportsmen JOIN SportDoctor ON Sportsmen.tgname='{username}' and Sportsmen.SportDoctor_tgname=SportDoctor.tgname")
    cursor.execute(mysql_query)
    for i in cursor:
        doctor = i[0]
    
    await update.message.reply_text(f"Your doctor is: \n{doctor}")


async def show_list_of_sportsmen(update: Update):
    username = update.message.from_user["username"]

    mysql_query = (f"SELECT Name FROM Sportsmen WHERE MainCoach_tgname IN (SELECT Coach.MainCoach_tgname FROM Coach WHERE tgname='{username}')")
    cursor.execute(mysql_query)
    sportsmen = []
    for i in cursor:
        sportsmen.append(i[0])

    sportsmen = '\n'.join(sportsmen)

    await update.message.reply_text(f"Your sportsmen are:\n{sportsmen}")


async def get_training_for_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user["username"]
    mysql_query = (f"SELECT Training.idTraining, Training.Gym_Number, Training.StartTime, Training.FinishTime, Sportsmen.Name FROM Training JOIN Sportsmen WHERE Training.Sportsmen_tgname = Sportsmen.tgname AND Training.MainCoach_tgname = '{username}'")
    cursor.execute(mysql_query)
    training = []
    ids = []

    fmt1 = '%d %B %H:%M'
    fmt2 = '- %H:%M'
    for i in cursor:
        training.append(f'\n{i[0]}) Gym number: {i[1]}\n' + ' '.join([i[2].strftime(fmt1), i[3].strftime(fmt2)]) + "\n" + f"Sportsmen: {i[4]}")
        ids.append(i[0])
    
    training = '\n'.join(training)
    await update.message.reply_text(f"Your trainings are: \n{training}")

    keyboard = [[InlineKeyboardButton(i, callback_data=i)] for i in ids]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"Select training for delete:", reply_markup=reply_markup)


async def delete_training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    mysql_query = (f"DELETE FROM Training WHERE Training.idTraining = {query.data}")
    cursor.execute(mysql_query)
    cnx.commit()

    await query.edit_message_text(text=f"Training is deleted")

    return ConversationHandler.END


async def get_training_for_change(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user["username"]
    mysql_query = (f"SELECT * FROM ((SELECT Training.idTraining as idTraining, Training.Gym_Number, Training.StartTime, Training.FinishTime, Sportsmen.Name as SportsmenName, null AS Coach FROM Training JOIN Sportsmen WHERE Training.Sportsmen_tgname = Sportsmen.tgname AND Training.MainCoach_tgname = '{username}') UNION ALL (SELECT Training.idTraining as idTraining, Training.Gym_Number, Training.StartTime, Training.FinishTime, Sportsmen.Name as SportsmenName, Coach.Name as CoachName FROM Training JOIN Sportsmen JOIN Coach_Training JOIN Coach ON Training.idTraining = Coach_Training.Training_idTraining AND Coach_Training.Coach_tgname = Coach.tgname WHERE Training.Sportsmen_tgname = Sportsmen.tgname AND Training.MainCoach_tgname = '{username}')) x ORDER BY x.idTraining")
    cursor.execute(mysql_query)
    training = []
    ids = []

    fmt1 = '%d %B %H:%M'
    fmt2 = '- %H:%M'
    buf = -1
    for i in cursor:
        if i[0] == buf:
            training[-1] = training[-1] + f"{i[5]}; "
        else:
            training.append(f'\n{i[0]}) Gym number: {i[1]}\n' + ' '.join([i[2].strftime(fmt1), i[3].strftime(fmt2)]) + "\n" + f"Sportsmen: {i[4]}" + "\n" + f"Coaches: ")
            ids.append(i[0])
            buf = i[0]
    
    training = '\n'.join(training)
    await update.message.reply_text(f"Your trainings are: \n{training}")

    keyboard = [[InlineKeyboardButton(i, callback_data=i)] for i in ids]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"Select training for change:", reply_markup=reply_markup)


async def delete_or_add_coach(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()
    context.user_data["id_training"] = query.data
    await query.edit_message_text(text=f"Selected training: {query.data}")
    
    keyboard = [[InlineKeyboardButton("Delete", callback_data="Delete")], [InlineKeyboardButton("Add", callback_data="Add")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(f"Do you want delete or add coach?", reply_markup=reply_markup) 
    return CHOOSE_COACH


async def choose_coach(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()
    context.user_data["add_or_delete"] = query.data
    await query.edit_message_text(text=f"You chose: {query.data} coach")
    
    if context.user_data["add_or_delete"] == "Add":

        mysql_query = (f"SELECT tgname, Name FROM Coach WHERE MainCoach_tgname = (SELECT MainCoach_tgname FROM Training WHERE idTraining = {context.user_data['id_training']}) AND tgname NOT IN (SELECT Coach_tgname FROM Coach_Training WHERE Training_idTraining = {context.user_data['id_training']})")
        cursor.execute(mysql_query)
        coaches = []
        tgnames = []

        for i in cursor:
            tgnames.append(i[0])
            coaches.append(i[1])

        keyboard = [[InlineKeyboardButton(coaches[i], callback_data=tgnames[i])] for i in range(len(tgnames))]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(f"Select Coach to add in Training:", reply_markup=reply_markup)

    if context.user_data["add_or_delete"] == "Delete":

        mysql_query = (f"SELECT tgname, Name FROM Coach WHERE MainCoach_tgname = (SELECT MainCoach_tgname FROM Training WHERE idTraining = {context.user_data['id_training']}) AND tgname IN (SELECT Coach_tgname FROM Coach_Training WHERE Training_idTraining = {context.user_data['id_training']})")
        cursor.execute(mysql_query)
        coaches = []
        tgnames = []

        for i in cursor:
            tgnames.append(i[0])
            coaches.append(i[1])

        keyboard = [[InlineKeyboardButton(coaches[i], callback_data=tgnames[i])] for i in range(len(tgnames))]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(f"Select Coach to delete in Training:", reply_markup=reply_markup)

    return CHANGE_TRAINING


async def change_training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    if context.user_data["add_or_delete"] == "Add":
        mysql_query = (f"INSERT INTO Coach_Training (Coach_tgname, Training_idTraining) VALUES ('{query.data}', '{context.user_data['id_training']}')")
        cursor.execute(mysql_query)
        cnx.commit()

        await query.edit_message_text(text=f"Coach was added to the training")

    if context.user_data["add_or_delete"] == "Delete":
        mysql_query = (f"DELETE FROM Coach_Training WHERE Coach_Training.Coach_tgname = '{query.data}' AND Coach_Training.Training_idTraining = {context.user_data['id_training']}")
        cursor.execute(mysql_query)
        cnx.commit()

        await query.edit_message_text(text=f"Coach was deleted from the training")

    return ConversationHandler.END

# FOR DOCTOR
async def check_sportsmen_for_doctor(update: Update):
    username = update.message.from_user["username"]

    mysql_query = (f"SELECT Name FROM Sportsmen WHERE SportDoctor_tgname = '{username}'")
    cursor.execute(mysql_query)
    sportsmen = []
    for i in cursor:
        sportsmen.append(i[0])

    sportsmen = '\n'.join(sportsmen)
    
    await update.message.reply_text(f"Your sportsmen are: \n{sportsmen}")


async def view_schedule_for_doctor(update: Update):
    username = update.message.from_user["username"]

    mysql_query = (f"SELECT Training.Gym_Number, Training.StartTime, Training.FinishTime, Sportsmen.Name FROM Training JOIN Sportsmen WHERE Training.Sportsmen_tgname = Sportsmen.tgname AND Sportsmen.SportDoctor_tgname = '{username}' ORDER BY Training.StartTime")
    cursor.execute(mysql_query)
    training = []

    fmt1 = '%d %B %H:%M'
    fmt2 = '- %H:%M'
    flag = True
    for i in cursor:
        if flag or bufdate != i[1]:
            training.append(f'\nGym number: {i[0]}\n' + ' '.join([i[1].strftime(fmt1), i[2].strftime(fmt2)]) + "\n" + f"Sportsmen: {i[3]}; ")
            bufdate = i[1]
        else:
            training[-1] = training[-1] + f"{i[3]}; "
        flag = False
        
    training = '\n'.join(training)
    await update.message.reply_text(f"Your trainings are: \n{training}")
    

async def select_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["username"] = update.message.from_user["username"]
    days = [(dt.date.today() + dt.timedelta(days=i)) for i in range(7)]
    
    keyboard = [[InlineKeyboardButton(i.strftime('%-d %B %Y'), callback_data='$'.join([i.strftime('%-d %B %Y'), i.strftime('%Y-%m-%d')]))] for i in days]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"Select date:", reply_markup=reply_markup)


async def select_gyms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query

    await query.answer()
    await query.edit_message_text(text=f"Selected date: {query.data.split('$')[0]}")

    context.user_data["selected_date"] = query.data.split('$')[1]

    mysql_query = (f"SELECT DISTINCT Gym_Number, StartTime, FinishTime FROM Training WHERE DATE(StartTime)='{context.user_data['selected_date']}'")
    cursor.execute(mysql_query)
    trainings_times = []
    for i in cursor:
        trainings_times.append(i)

    mysql_query = (f"SELECT * FROM Gym")
    cursor.execute(mysql_query)
    gyms_times = []
    for i in cursor:
        gyms_times.append(i)

    mysql_query = (f"SELECT Gym_Number FROM TrainerInGym")
    cursor.execute(mysql_query)
    num_trainers_in_each_gym = {i[0]:0 for i in gyms_times}
    for i in cursor:
        num_trainers_in_each_gym[i[0]] += 1 

    gyms = []
    for i in gyms_times:
        gyms.append(i[0])

    busy_slots = []
    
    for g in gyms_times:
        num_working_hours = (g[2] - g[1]).seconds // 3600
        num_training_hours = 0
        for t in trainings_times:
            if t[0] == g[0]:
                num_training_hours += 1
        busy_slots.append(f'{g[0]}: {num_training_hours}/{(num_trainers_in_each_gym[g[0]] + 1) * num_working_hours}')
        if num_training_hours == (num_trainers_in_each_gym[g[0]] + 1) * num_working_hours:
            gyms.remove(g[0])

    busy_slots = '\n'.join(busy_slots)
    
    keyboard = [[InlineKeyboardButton(i, callback_data=i)] for i in gyms]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(f"Select gym (below is current workload):\n{busy_slots}", reply_markup=reply_markup)
    return SELECT_SPORTSMEN


async def select_sportsmen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()
    await query.edit_message_text(text=f"Selected gym: {query.data}")

    context.user_data["selected_gym"] = int(query.data)
    
        
    mysql_query = (f"SELECT Sportsmen.Name, Sportsmen.tgname FROM Sportsmen WHERE Sportsmen.MainCoach_tgname = '{context.user_data['username']}'")
    cursor.execute(mysql_query)
    sportsmen = []
    sportsmen_tgs = []
    for i in cursor:
        sportsmen.append(i[0])
        sportsmen_tgs.append(i[1])
    sportsmen.insert(0, 'Select all')
    tgs_and_names = []
    for i in range(len(sportsmen)):
        if sportsmen[i] != 'Select all':
            tgs_and_names.append(f"{sportsmen[i]}:{sportsmen_tgs[i-1]}")
        else:
            tgs_and_names.append(f"{sportsmen[i]}:{'&'.join(sportsmen_tgs)}")

    keyboard = [[InlineKeyboardButton(n, callback_data=tgs_and_names[i])] for i, n in enumerate(sportsmen)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(f"Select sportsmen:", reply_markup=reply_markup)
    return SELECT_TRAINER

def select_times_part(q, context):
    if context.user_data['selected_trainer'] == 'NULL':
        mysql_query = (f"SELECT DISTINCT DATE_FORMAT(StartTime, '%H:%i'), DATE_FORMAT(FinishTime, '%H:%i'), TrainerInGym_idTrainer FROM Training WHERE DATE(StartTime)='{context.user_data['selected_date']}' and Gym_number='{context.user_data['selected_gym']}' AND TrainerInGym_idTrainer IS NULL ORDER BY TrainerInGym_idTrainer")
    else:
        mysql_query = (f"SELECT DISTINCT DATE_FORMAT(StartTime, '%H:%i'), DATE_FORMAT(FinishTime, '%H:%i'), TrainerInGym_idTrainer FROM Training WHERE DATE(StartTime)='{context.user_data['selected_date']}' and Gym_number='{context.user_data['selected_gym']}' AND TrainerInGym_idTrainer IN ({context.user_data['selected_trainer']}) ORDER BY TrainerInGym_idTrainer")
    print(mysql_query)
    cursor.execute(mysql_query)
    trainings_times = []
    for i in cursor:
        trainings_times.append(i)

    mysql_query = (f"SELECT TrainerInGym.idTrainer FROM `TrainerInGym` WHERE Gym_Number = '{context.user_data['selected_gym']}' and Trainer_Type = '{q}'")
    cursor.execute(mysql_query)
    trainer_ids = []
    for i in cursor:
        trainer_ids.append(i[0])

    if len(trainer_ids) == 0:
        trainer_ids.append(None)

    mysql_query = (f"SELECT StartTimeWorking, FinishTimeWorking FROM Gym WHERE Number={context.user_data['selected_gym']}")
    cursor.execute(mysql_query)
    for i in cursor:
        gym_time = i

    num_working_hours = (gym_time[1] - gym_time[0]).seconds // 3600
    slots_start = [(dt.datetime.min + gym_time[0] + dt.timedelta(hours=i)).time().strftime('%H:%M') for i in range(num_working_hours)]
    slots_end = [(dt.datetime.min + gym_time[0] + dt.timedelta(hours=i)).time().strftime('%H:%M') for i in range(1, num_working_hours + 1)]

    slots_start_copy = slots_start.copy()
    slots_end_copy = slots_end.copy()

    id_for_time = []

    for i, st in enumerate(slots_start):
        used_trainers = []
        counter = 0
        for t in trainings_times:
            if t[0] == st:
                counter += 1
                used_trainers.append(t[2])
        if counter == len(trainer_ids):
            slots_start_copy.remove(slots_start[i])
            slots_end_copy.remove(slots_end[i])
        else:
            for id in trainer_ids:
                if id not in used_trainers:
                    id_for_time.append(id)
                    break
                
    slots = [slots_start_copy[i] + ' - ' + slots_end_copy[i] for i in range(len(slots_start_copy))]

    id_and_times = []
    for i in range(len(slots)):
        id_and_times.append(f"{id_for_time[i]}&{slots[i]}")

    return id_and_times, slots

async def select_trainers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data["selected_sportsman"] = query.data.split(':')[1]
    if query.data.split(':')[0] != 'Select all':
        await query.edit_message_text(text=f"Selected sportsman: {query.data.split(':')[0]}")

        mysql_query = (f"SELECT TrainerInGym.idTrainer, TrainerInGym.Trainer_Type FROM `TrainerInGym` WHERE Gym_Number = '{context.user_data['selected_gym']}'")
        cursor.execute(mysql_query)
        trainers_in_gyms = []
        for i in cursor:
            trainers_in_gyms.append(i)

        mysql_query = (f"SELECT DISTINCT Training.StartTime, Training.TrainerInGym_idTrainer FROM Training WHERE Gym_Number = '{context.user_data['selected_gym']}' and DATE(Training.StartTime) = '{context.user_data['selected_date']}'")
        cursor.execute(mysql_query)
        num_trainings_for_trainers = {i[0]:0 for i in trainers_in_gyms}
        num_trainings_for_trainers['NULL'] = 0
        for i in cursor:
            num_trainings_for_trainers[i[1] if i[1] else 'NULL'] += 1

        mysql_query = (f"SELECT StartTimeWorking, FinishTimeWorking FROM Gym WHERE Number = '{context.user_data['selected_gym']}'")
        cursor.execute(mysql_query)
        for i in cursor:
            g = i
            
        num_working_hours = (g[1] - g[0]).seconds // 3600

        trainers_ids = num_trainings_for_trainers.keys()

        for k in trainers_ids:
            if num_trainings_for_trainers[k] == num_working_hours:
                del num_trainings_for_trainers[k]

        good_trainers = {i:'No trainer' for i in list(num_trainings_for_trainers.keys())}

        for k in num_trainings_for_trainers.keys():
            for i in trainers_in_gyms:
                if i[0] == k:
                    good_trainers[k] = i[1]

        num_trainings_for_trainers_unique = {i:[0, 0, []] for i in list(dict.fromkeys(list(good_trainers.values())))}
        for k in good_trainers.keys():
            num_trainings_for_trainers_unique[good_trainers[k]][1] += num_working_hours
            num_trainings_for_trainers_unique[good_trainers[k]][0] += num_trainings_for_trainers[k]
            num_trainings_for_trainers_unique[good_trainers[k]][2].append(str(k))


        workload = []
        for k in num_trainings_for_trainers_unique.keys():
            workload.append(f'{k}: {num_trainings_for_trainers_unique[k][0]}/{num_trainings_for_trainers_unique[k][1]}')

        ids_and_names = []
        for k in num_trainings_for_trainers_unique.keys():
            tmp = '_'.join(num_trainings_for_trainers_unique[k][2])
            ids_and_names.append(f'{tmp}:{k}')

        workload = '\n'.join(workload)

        keyboard = [[InlineKeyboardButton(n, callback_data=ids_and_names[::-1][i])] for i, n in enumerate(list(num_trainings_for_trainers_unique.keys())[::-1])]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(f"Select trainer (below is corrent workload):\n{workload}", reply_markup=reply_markup)
        
        return SELECT_TIME

    else:
        await query.edit_message_text(text=f"All sportsmen will be invited to the training")
        context.user_data["selected_trainer"] = 'NULL'
        id_and_times, slots = select_times_part('No trainer', context)

        keyboard = [[InlineKeyboardButton(n, callback_data=id_and_times[i])] for i, n in enumerate(slots)]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(f"Select time:", reply_markup=reply_markup)
        return SELECT_MAINCOACH

    
async def select_times(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()
    if (q := query.data.split(':')[1]) == 'No trainer':
        await query.edit_message_text(text=f"No trainer was selected")
        context.user_data["selected_trainer"] = 'NULL'
    else:
        await query.edit_message_text(text=f"Selected trainer: {query.data.split(':')[1]}")
        context.user_data["selected_trainer"] = ', '.join(query.data.split(':')[0].split('_'))

    id_and_times, slots = select_times_part(q, context)

    keyboard = [[InlineKeyboardButton(n, callback_data=id_and_times[i])] for i, n in enumerate(slots)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(f"Select time:", reply_markup=reply_markup)
    return SELECT_MAINCOACH


async def select_main_coach(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()
    await query.edit_message_text(text=f"Selected time: {query.data.split('&')[1]}")

    context.user_data["selected_time"] = query.data.split('&')[1]
    if context.user_data.get("selected_trainer") != 'NULL':
        context.user_data["selected_trainer"] = int(query.data.split('&')[0])

    keyboard = [[InlineKeyboardButton(i, callback_data=i)] for i in ["Yes", "No"]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(f"Do you want to come to the training?", reply_markup=reply_markup)
    return SELECT_COACH


async def select_coach(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = context.user_data["username"]

    query = update.callback_query

    await query.answer()
    await query.edit_message_text(text=f"You decided {'' if query.data == 'Yes' else 'not '}to come to the training")

    context.user_data["selected_main_coach"] = username if query.data == 'Yes' else 'NULL'

    mysql_query = (f"SELECT Coach.Name, Coach.tgname FROM Coach WHERE Coach.MainCoach_tgname = '{username}'")
    cursor.execute(mysql_query)
    coaches = []
    coaches_tgs = []
    for i in cursor:
        coaches.append(i[0])
        coaches_tgs.append(i[1])
    tgs_and_names = []
    if query.data == 'Yes':
        coaches.insert(0, 'No coach')
    for i in range(len(coaches)):
        if coaches[i] != 'No coach':
            tgs_and_names.append(f"{coaches[i]}:{coaches_tgs[i-1] if query.data == 'Yes' else coaches_tgs[i]}")
        else:
            tgs_and_names.append(f"{coaches[i]}:NULL")
    keyboard = [[InlineKeyboardButton(n, callback_data=tgs_and_names[i])] for i, n in enumerate(coaches)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(f"Select coach:", reply_markup=reply_markup)
    return INSERT_TRAINING


async def insert_training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = context.user_data["username"]
    query = update.callback_query

    await query.answer()
    context.user_data["selected_coach"] =  query.data.split(':')[1]
    if query.data.split(':')[0] != 'No coach':
        await query.edit_message_text(text=f"Selected coach: {query.data.split(':')[0]}")
    else:
        await query.edit_message_text(text=f"No coaches will be invited to the training")

    insert_training_sql(context.user_data)
    await query.message.reply_text(text=f"Your training was recorded")
    context.user_data.clear()
    return ConversationHandler.END


async def log_out(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"You were successfully logged out")
    return ConversationHandler.END



def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("###YOUR_TOKEN###").build()

    # application.add_handler(CallbackQueryHandler(button))


    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [MessageHandler(filters.Regex(f"^({'|'.join([k for i in all_available_commands.values() for j in i for k in j])})$"), base_command_performer)], # check here
            SELECT_GYM: [CallbackQueryHandler(select_gyms)],
            SELECT_TIME: [CallbackQueryHandler(select_times)],
            SELECT_MAINCOACH: [CallbackQueryHandler(select_main_coach)],
            SELECT_COACH: [CallbackQueryHandler(select_coach)],
            SELECT_SPORTSMEN: [CallbackQueryHandler(select_sportsmen)],
            SELECT_TRAINER: [CallbackQueryHandler(select_trainers)],
            INSERT_TRAINING: [CallbackQueryHandler(insert_training)],

            SELECT_DEL_TRAINING: [CallbackQueryHandler(delete_training)],
            
            DELETE_OR_ADD_COACH: [CallbackQueryHandler(delete_or_add_coach)],
            CHOOSE_COACH: [CallbackQueryHandler(choose_coach)],
            CHANGE_TRAINING: [CallbackQueryHandler(change_training)],
            
            SET_START_WORKING: [CallbackQueryHandler(set_gym_new_start_working)],
            SET_FINISH_WORKING: [CallbackQueryHandler(set_gym_new_finish_working)],
            UPDATE_GYM_SCHEDULE: [CallbackQueryHandler(update_gym_new_schedule)],

        },
        fallbacks=[CommandHandler("log_out", log_out)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
