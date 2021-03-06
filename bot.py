
"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:

Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from db import DB
import sqlite3
import logging
import os
import re
from telegram import User, TelegramObject
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, DictPersistence, BasePersistence, Dispatcher)
from dotenv import load_dotenv
load_dotenv()


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


START, CITY, LOCALITY, PINCODE,  MODEOFCONTACT, MAILID, PHONE_NUMBER, REQUIREMENTS, BOARD, STANDARD, MEDIUM, SUBJECTS, DEAL_TYPE, CONFIRM, FINALQUESTION, CANCEL = range(16)

MODE_OF_CONTACT_OPTIONS = ['Phone', 'MailID']
REQUIREMENTS_OPTIONS = ['Need book', 'Have book']
BOARD_OPTIONS = ['CBSE', 'ICSE', 'State Board']
DEAL_OPTIONS = ['Buy', 'Sell', 'Donate', 'Exchange']
YES_NO_OPTIONS = ['Yes', 'No']
MEDIUM_OPTIONS = ['English','Hindi','Kannada']
#MessageHandler(Filters.regex(re.compile('BOARD_OPTIONS', re.IGNORECASE), callback)

def start(update, context):
    """Send a message when the command /start is issued."""
    user = update.message.from_user
    update.message.reply_text(
        f'''
	Hello! {user.first_name} 
	Welcome to Sumrux's book exchange campaign #BackToStudies 
	Thank you for choosing us to help you.  
	This is a free service by Sumrux for academic books during Covid-19 recovery. 
	Let us know the details of the books you are looking for/the books you have. 
	We will find the right people for your books and connect them to you. 
	You have complete freedom to talk to them and finalize the deal. You can buy/sell/donate/exchange the books. 
	To know how it works visit 
	Https://www.sumrux.com/know-backtostudies

	Let us get you started. 
	We need your locality to find the closest match.
        Please enter your city.
        ''')
    return CITY

def city(update, context):
    context.user_data['City'] = update.message.text
    user = update.message.from_user
    regex = r"^[a-z A-Z]+$"

    if(re.search(regex, context.user_data['City'])):
        logger.info("City of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            ''' 
		We do need some more information to help you find a suitable bookmatch.
		Please enter your locality.''',
            reply_markup=ReplyKeyboardRemove())

    else:
        update.message.reply_text(
            'Please enter a valid City Name.', reply_markup=ReplyKeyboardRemove())
        user = update.message.from_user
        context.user_data['City'] = update.message.text
        return CITY

    return LOCALITY

def locality(update, context):
    context.user_data['Locality'] = update.message.text
    user = update.message.from_user
    regex = r"^[a-z A-Z]+$"

    if(re.search(regex, context.user_data['Locality'])):
        logger.info("Locality of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            'Please enter your pincode.',
            reply_markup=ReplyKeyboardRemove())

    else:
        update.message.reply_text(
            'Please enter a valid Locality Name', reply_markup=ReplyKeyboardRemove())
        context.user_data['Locality'] = update.message.text
        user = update.message.from_user
        return LOCALITY

    return PINCODE


def pincode(update, context):
    context.user_data['Pincode'] = update.message.text
    user = update.message.from_user
    regex = r"^[1-9][\d]{5}$"

    if(re.search(regex, context.user_data['Pincode'])):
        logger.info("Pincode of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            '''Thankyou, you have made it easier for us to find you a match.
Would you like us to communicate via phone or email?''',
            reply_markup=ReplyKeyboardMarkup([MODE_OF_CONTACT_OPTIONS], one_time_keyboard=True))

    else:
        update.message.reply_text(
            'Please enter a valid Pincode', reply_markup=ReplyKeyboardRemove())
        user = update.message.from_user
        context.user_data['Pincode'] = update.message.text
        return PINCODE

    return MODEOFCONTACT

def modeofcontact(update, context):
    context.user_data['Modeofcontact'] = update.message.text
    user = update.message.from_user
    logger.info("Mode of contact is %s: %s",
        user.first_name, update.message.text)
        
    if(context.user_data['Modeofcontact']=="MailID"):
        update.message.reply_text(
        'Please enter your Email Id', reply_markup=ReplyKeyboardRemove())
        return MAILID
    elif(context.user_data['Modeofcontact']=="Phone"):
        update.message.reply_text(
        'Please enter your Phone Number', reply_markup=ReplyKeyboardRemove())
        return PHONE_NUMBER
    else:
        update.message.reply_text('Please enter valid preferred mode of contact Phone/Email',
reply_markup=ReplyKeyboardRemove([MODE_OF_CONTACT_OPTIONS], one_time_keyboard=True))
        return MODEOFCONTACT
    return MAILID

def mailid(update, context):
    context.user_data['MailID'] = update.message.text
    user = update.message.from_user
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if(re.search(regex, context.user_data['MailID'])):
        context.user_data['Phone_Number'] = "Not Provided"
        user = update.message.from_user
        logger.info("Email of %s: %s", user.first_name, update.message.text)
        reply_keyboard = [REQUIREMENTS_OPTIONS]
        update.message.reply_text('Do you need or have a book',
            reply_markup=ReplyKeyboardMarkup([REQUIREMENTS_OPTIONS], one_time_keyboard=True))
        return REQUIREMENTS

    else:
        update.message.reply_text(
            'Please enter a valid Email Id', reply_markup=ReplyKeyboardRemove())
        return MAILID
    return PHONE_NUMBER

def phone_number(update, context):
    context.user_data['Phone_Number'] = update.message.text
    user = update.message.from_user
    regex = r'^[6-9]\d{9}$'
    if(re.search(regex, context.user_data['Phone_Number'])):
        context.user_data['MailID'] = "Not Provided"
        user = update.message.from_user
        logger.info("Phone Number of %s: %s", user.first_name, update.message.text)
        reply_keyboard = [REQUIREMENTS_OPTIONS]
        update.message.reply_text('Do you need or have a book',
            reply_markup=ReplyKeyboardMarkup([REQUIREMENTS_OPTIONS], one_time_keyboard=True))
        return REQUIREMENTS

    else:
        update.message.reply_text(
            'Please enter a valid Phone Number', reply_markup=ReplyKeyboardRemove())
        return PHONE_NUMBER
    return REQUIREMENTS


def Requirements(update, context):
    context.user_data['Requirements'] = update.message.text
    user = update.message.from_user

    if(context.user_data['Requirements'] in REQUIREMENTS_OPTIONS):
        logger.info("Requirement of %s: %s",
                    user.first_name, update.message.text)

        update.message.reply_text(
            '''
		We are on our way to connect you with other readers around you.
		Which board books are you looking for/ have??''',
            reply_markup=ReplyKeyboardMarkup([BOARD_OPTIONS], one_time_keyboard=True))
        return BOARD
    else:
        update.message.reply_text('Please enter valid requirements',
                                  reply_markup=ReplyKeyboardRemove([REQUIREMENTS_OPTIONS]))
        user = update.message.from_user
        context.user_data['Requirements'] = update.message.text
        return REQUIREMENTS
    return BOARD


def board(update, context):
    context.user_data['Board'] = update.message.text
    user = update.message.from_user
    if(context.user_data['Board']in BOARD_OPTIONS):
        logger.info("Board of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            '''The Grade/class please. Enter a number 1 to 12''',
            reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text('Please enter valid Board. (CBSE/ICSE/State Board)',
                                  reply_markup=ReplyKeyboardMarkup([BOARD_OPTIONS], one_time_keyboard=True))
        user = update.message.from_user
        context.user_data['Board'] = update.message.text
        return BOARD

    return STANDARD


def standard(update, context):
    context.user_data['Standard'] = update.message.text
    user = update.message.from_user
    regex = r"^([1-9]|1[012])$"

    if(re.search(regex, context.user_data['Standard'])):
        logger.info("Books of standard %s: %s",
                    user.first_name, update.message.text)
        update.message.reply_text(
            '''
    What is the Medium of instruction/book Ex Hindi/English/Kannada?
       ''',
           reply_markup=ReplyKeyboardMarkup([MEDIUM_OPTIONS], one_time_keyboard=True))

    else:
        update.message.reply_text(
            'Please enter valid Standard from 1 to 12', reply_markup=ReplyKeyboardRemove())
        user = update.message.from_user
        context.user_data['Standard'] = update.message.text
        return STANDARD
    return MEDIUM

def medium(update, context):
    context.user_data['Medium'] = update.message.text
    user = update.message.from_user
    regex = r"^[a-z , A-Z]+$"

    if(re.search(regex, context.user_data['Medium'])):
        logger.info("Medium of %s: %s",
                    user.first_name, update.message.text)
        update.message.reply_text(
            '''
       Which subjects do you have in mind? 
Please list them. 
Ex: Physics, Hindi, Mathematics, Chemistry, Biology, Science, Social Science, English, Hindi, Kannada, Sanskrit, French, RS Aggarwal, RD Sharma, History, Civics, Geography, Others?''',
            reply_markup=ReplyKeyboardRemove())

    else:
        update.message.reply_text(
            'Please enter valid Standard valid medium of instruction/book ex Hindi/English/Kannada',
            reply_markup=ReplyKeyboardMarkup([MEDIUM_OPTIONS], one_time_keyboard=True))
        user = update.message.from_user
        context.user_data['Standard'] = update.message.text
        return MEDIUM
    return SUBJECTS


def subjects(update, context):
    context.user_data['Subjects'] = update.message.text
    user = update.message.from_user
    regex = r"^[a-z,-:A-Z 0-9]+$"

    if(re.search(regex, context.user_data['Subjects'])):
        logger.info("Books of Subjects for %s: %s",
                    user.first_name, update.message.text)
        update.message.reply_text(
            'How do you want to deal?',
            reply_markup=ReplyKeyboardMarkup([DEAL_OPTIONS], one_time_keyboard=True))

    else:
        update.message.reply_text(
            'Please enter valid Subjects', reply_markup=ReplyKeyboardRemove())
        user = update.message.from_user
        context.user_data['Subjects'] = update.message.text
        return SUBJECTS
    return DEAL_TYPE


def deal_type(update, context):
    context.user_data['Deal_Type'] = update.message.text
    user = update.message.from_user

    if(context.user_data['Deal_Type'] in DEAL_OPTIONS):
        logger.info("Deal of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
            f'''
We got all we need to find the contacts for your books. Displayed below are your details.
Name : {user.first_name},
Locality : {context.user_data["Locality"]}, 
City : {context.user_data["City"]}, 
Pincode : {context.user_data["Pincode"]}, 
Modeofcontact : {context.user_data["Modeofcontact"]},
MailID : {context.user_data["MailID"]},
Contact : {context.user_data["Phone_Number"]}, 
Requirements : {context.user_data["Requirements"]}, 
Board : {context.user_data["Board"]}, 
Standard : {context.user_data["Standard"]},
Medium : {context.user_data["Medium"]}, 
Subjects : {context.user_data["Subjects"]}, 
Deal_Type : {context.user_data["Deal_Type"]}, 

Please let us know if your previous details were correct. Press yes to confirm or no to fill details again.
		''',
            reply_markup=ReplyKeyboardMarkup([YES_NO_OPTIONS], one_time_keyboard=True))
        return CONFIRM

    else:
        update.message.reply_text('Please enter valid Deal (Buy/Sell/Donate/Exchange)',
                                  reply_markup=ReplyKeyboardMarkup([DEAL_OPTIONS], one_time_keyboard=True))
        user = update.message.from_user
        context.user_data['Deal_Type'] = update.message.text
        return DEAL_TYPE


def confirm(update, context):
    context.user_data['Confirm'] = update.message.text
    user = update.message.from_user
    logger.info("Confirm of %s : %s", user.first_name, update.message.text)

    if context.user_data['Confirm'] == "Yes":
        logger.info("Confirmation of %s : %s",
                    user.first_name, update.message.text)
       
        update.message.reply_text(f'''
		Your details have been confirmed and saved. We are nearing the end of our conversation. 
		Since you are looking for books, you might also have a few from previous grades. 
		If you share your details we can find you a student who might be in need of them!
		Would you like to register more book requests?''',
                                  reply_markup=ReplyKeyboardMarkup([YES_NO_OPTIONS], one_time_keyboard=True))
        return FINALQUESTION

    else:
        user = update.message.from_user
        update.message.reply_text('''
		Sorry we got it wrong would you like to enter  again options Yes or No''',
                                  reply_markup=ReplyKeyboardMarkup([YES_NO_OPTIONS], one_time_keyboard=True))
        return CANCEL


def finalquestion(update, context):
    context.user_data['Moredetails'] = update.message.text
    user = update.message.from_user
    # if user says yes in previous moredetails functions then take them to start
    # otherwise end the conversation

    if context.user_data['Moredetails'] == "Yes":
        ########################################################################
        ############   ADD  context.user_data in the database here  ############
        ########################################################################
        db = DB()
        db.setup()
        db.add_item(user.first_name,
        context.user_data["Locality"],
        context.user_data["City"],
        context.user_data["Pincode"],
        context.user_data["Modeofcontact"],
        context.user_data["MailID"],
        context.user_data["Phone_Number"], 
		context.user_data["Requirements"], 
		context.user_data["Board"], 
		context.user_data["Standard"], 
        context.user_data["Medium"],
		context.user_data["Subjects"], 
		context.user_data["Deal_Type"])
        user = update.message.from_user
        update.message.reply_text(
            f'''
        Hello! {user.first_name} 
        Welcome to Sumrux's book exchange campaign #BackToStudies 
        Thank you for choosing us to help you.  
        This is a free service by Sumrux for academic books during Covid-19 recovery. 
        Let us know the details of the books you are looking for/the books you have. 
        We will find the right people for your books and connect them to you. 
        You have complete freedom to talk to them and finalize the deal. You can buy/sell/donate/exchange the books. 
        To know how it works visit 
        Https://www.sumrux.com/know-backtostudies

        Let us get you started. 
        We need your locality to find the closest match. 
        Please enter your city.
            ''')
        return CITY

    else:
        db = DB()
        db.setup()
        db.add_item(user.first_name,
        context.user_data["Locality"],
        context.user_data["City"],
        context.user_data["Pincode"],
        context.user_data["Modeofcontact"],
        context.user_data["MailID"],
        context.user_data["Phone_Number"], 
		context.user_data["Requirements"], 
		context.user_data["Board"], 
		context.user_data["Standard"],
        context.user_data["Medium"], 
		context.user_data["Subjects"], 
		context.user_data["Deal_Type"])
        update.message.reply_text(f'''{context.user_data['Moredetails']} :
			Well, that brings us to the end of our conversation. 
			Thankyou for going green during this lockdown. 
			We shall soon reach out to you with your book match.
			Till then, stay safe.''',
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    return ConversationHandler.END

def cancel(update, context):
    context.user_data['Confirm'] = update.message.text
    user = update.message.from_user
    if context.user_data['Confirm'] == "Yes":  
        logger.info("Confirmation of %s : %s",
                    user.first_name, update.message.text)  
        ########################################################################
        ############   ADD  context.user_data in the database here  ############
        ########################################################################
        user = update.message.from_user
        update.message.reply_text(
            f'''
        Hello! {user.first_name} 
        Welcome to Sumrux's book exchange campaign #BackToStudies 
        Thank you for choosing us to help you.  
        This is a free service by Sumrux for academic books during Covid-19 recovery. 
        Let us know the details of the books you are looking for/the books you have. 
        We will find the right people for your books and connect them to you. 
        You have complete freedom to talk to them and finalize the deal. You can buy/sell/donate/exchange the books. 
        To know how it works visit 
        Https://www.sumrux.com/know-backtostudies

        Let us get you started. 
        We need your locality to find the closest match. 
        Please enter your city.
            ''')
        return CITY
    else:
        user = update.message.from_user
        update.message.reply_text('''
		Sorry to see you go. In Case you change your mind please type @SumruxBot in telegram search''')
    return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # will Create the Updater and pass it our bot's token.
    # Make sure to set use_context=True to use the new context based callbacks

    updater = Updater(
        os.getenv("TELEGRAM_TOKEN", ""), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states INFO, LOCATION, BIO, CLASSNAMES
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            START: [MessageHandler(Filters.text, start)],

            LOCALITY: [MessageHandler(Filters.text, locality)],

            CITY: [MessageHandler(Filters.text, city)],

            PINCODE: [MessageHandler(Filters.text, pincode)],

            MAILID: [MessageHandler(Filters.text, mailid)],

            PHONE_NUMBER: [MessageHandler(Filters.text, phone_number)],

            MODEOFCONTACT: [MessageHandler(Filters.text, modeofcontact)],

            REQUIREMENTS: [MessageHandler(Filters.text, Requirements)],

            BOARD: [MessageHandler(Filters.text, board)],

            STANDARD: [MessageHandler(Filters.text, standard)],

            MEDIUM: [MessageHandler(Filters.text, medium)],

            SUBJECTS: [MessageHandler(Filters.text, subjects)],

            DEAL_TYPE: [MessageHandler(Filters.text, deal_type)],

            CONFIRM: [MessageHandler(Filters.text, confirm)],

            FINALQUESTION: [MessageHandler(Filters.text, finalquestion)],
            CANCEL: [MessageHandler(Filters.text, cancel)]

        },

        fallbacks=[CommandHandler('cancel', cancel)], )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    #    press ctrl c for stopping the bot
    # SIGTERM or SIGABRT. This should be used most of the time
    # start_polling() is non-blocking and will stop the bot.
    updater.idle()
    # d.add_item(CITY, PINCODE, STANDARD, BOARD, MEDIUM, SUBJECTS, NUMBER, EMAIL, REQ, CONFIRM)
    # print(CITY, PINCODE, STANDARD, BOARD, MEDIUM,
    #       SUBJECTS, NUMBER, EMAIL, REQ, CONFIRM)

    # d.get_items()


if __name__ == '__main__':
    main()
