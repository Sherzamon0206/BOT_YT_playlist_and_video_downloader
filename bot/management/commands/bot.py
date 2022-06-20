from django.core.management.base import BaseCommand
from telegram.utils.request import Request
from django.conf import settings
from  telegram import Bot
from telegram.ext import Updater
import requests



class Command(BaseCommand):
    help='Bu django telegram bot'

    def handle(self,*args,**options):
        request=Request(
        )
        bot=Bot(
            request=request,
            token=settings.TOKEN1,


        )

        print(bot.get_me())


#########################################################################
import time

import pytube
from django.shortcuts import render
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters,CallbackQueryHandler
from bot.models import *
import re
from pytube import YouTube, Playlist
from io import BytesIO
from telegram import Update, ReplyKeyboardMarkup,InlineKeyboardMarkup, InlineKeyboardButton
import logging

# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)
# logger = logging.getLogger(__name__)
#end-logging

#buttons
button = ReplyKeyboardMarkup([["Restart"]], resize_keyboard=True)
button3 = ReplyKeyboardMarkup([["users", "Add_admin"], ["Homepage"], ["send_message", "all_admins"]],resize_keyboard=True)
button2 = ReplyKeyboardMarkup([["Homepage", "AdminPanel"]], resize_keyboard=True)
button4 = ReplyKeyboardMarkup([["Restart"],["AdminPanel"]], resize_keyboard=True)
keyboard = [
    [
        InlineKeyboardButton("mp3✅", callback_data="mp3"),
        InlineKeyboardButton("video✅", callback_data="video")
    ]
]
video="video",
mp3="mp3",


############################################################
#__functions_______

# for  all users __________**********
def start(update: Update, context: CallbackContext):
    time.sleep(0.01)
    context.user_data['id'] = update.effective_user.id
    id = update.effective_user.id
    f_name = update.effective_user.first_name
    l_name = update.effective_user.last_name
    username = update.effective_user.username
    # user add to base **************************************8
    try:
        profile = Profile.objects.get(exeterenal_id=id)
        profile.f_name = f_name
        profile.username = username
        profile.l_name = l_name
        profile.save()
    except:
        user, created = Profile.objects.get_or_create(exeterenal_id=id, username=username, f_name=f_name, l_name=l_name)
    # cheking user  for  admin or  custom user
    try:
        if AdminPanel.objects.get(admin_id=context.user_data['id']) is not None:
            update.message.reply_text(
                f"""<i> Hi {update.effective_user.first_name}\n</i><b>♻️send  me  a  playlist  or  video  url  link </b>🔔 \n 



					""", reply_markup=button4, parse_mode="HTML")
            return 'admin'
    except:
        update.message.reply_text(
            f"""<i> Hi {update.effective_user.first_name}\n</i><b>♻️send  me  a  playlist  or  video  url  link </b>🔔 \n 



				""", reply_markup=button, parse_mode="HTML")
        return 'bot'
def download_check(update: Update, context: CallbackContext):

    query = update.callback_query
    answer = query.data
    query.delete_message()



    url = context.user_data['url']
    id = context.user_data['id']
    print(update.callback_query.data)
    print(url)


    if answer == "video":
        print("video if ga kirdi")

        try:
            print("video  try  ga kirdi")

            playlist = Playlist(url)
            playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
            soni = len(playlist.video_urls)
            print("soni: ",soni)

            links = playlist.video_urls
            print(f"try: {links}" ,)
        except:
            print("video exceptga kirdi")

            links = []
            links.append(url)
            print("except : ", links)

        for link in links:
            buffer = BytesIO()
            time.sleep(0.1)

            yt = YouTube(link)
            video = yt.streams.get_highest_resolution()
            video.stream_to_buffer(buffer=buffer)
            buffer.seek(0)
            filename = video.title
            #
            context.bot.send_video(chat_id=id, video=buffer, filename=filename)

        context.bot.send_message(chat_id=id, text="video download complete")
        return 'bot'


    elif answer == "mp3":
        print(" mp3 elif ga kirdi")
        url = context.user_data['url']
        print(url)

        try:
            print("mp3 try ga kirdi")
            if Playlist(url):
                print("ifga kirdi")
                playlist = Playlist(context.user_data['url'])
                playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
                soni = len(playlist.video_urls)
                print("soni: ",soni)
                links = playlist.video_urls
                print(links)
            elif YouTube(url):
                print("else ga kirdi")
                links=[]
                links.append(context.user_data['url'])



        except:
            print("mp3 exceptga kirdi")

            links = []
            links.append(url)
            print(links)

        for link in links:

            buffer = BytesIO()
            time.sleep(0.1)

            yt = YouTube(link)
            music = yt.streams.filter(only_audio=True).first()
            music.stream_to_buffer(buffer=buffer)
            buffer.seek(0)
            filename = music.title
            #
            context.bot.send_audio(chat_id=id, audio=buffer, filename=filename)


        context.bot.send_message(chat_id=id, text="music download complete")
        return 'bot'
def url(update: Update, context: CallbackContext):
    link = str(update.message.text)
    print(requests.get(link))



    try:
        if pytube.YouTube(link).check_availability() is None:

            update.message.reply_text("Please select   mp3🎵 or video format🎞",
                                      reply_markup=InlineKeyboardMarkup(keyboard))
            context.user_data['url'] = link
            print("url yaroqli")
            return 'callback'

    except:
        update.message.reply_text("the link you sent is invalid🧐❌")
        update.message.reply_text("please resend♻️")
        print("yaroqsiz url")
        return 'bot'

# admin panel  for all admins -----------****************************

def adminpanel(update: Update, context: CallbackContext):
    update.message.reply_text("Options:", reply_markup=button3)

    return "admin"

#--------users -data name id  fname  lname    ------id list  / excel /  txt
def users(update: Update, context: CallbackContext):
    id = context.user_data['id']
    userlar = Profile.objects.all()
    soni = userlar.count()
    context.bot.send_message(chat_id=id, text=f"number_of_users : {soni}",
                             reply_markup=ReplyKeyboardMarkup([["users_data","users_id"],["Homepage", "AdminPanel"]], resize_keyboard=True))


    return "admin"
def users_data(update:Update,context:CallbackContext):
    id = context.user_data['id']
    userlar = Profile.objects.all()
    soni = userlar.count()
    context.bot.send_message(chat_id=id, text=f"number_of_users : {soni}",
                             reply_markup=ReplyKeyboardMarkup([["users_data", "users_id"], ["Homepage", "AdminPanel"]],
                                                              resize_keyboard=True))



    for i in userlar:
        try:
            context.bot.send_message(chat_id=id,
                                     text=f"""{i.id} || {i.f_name} | {i.l_name} | {i.username} | {i.exeterenal_id}"""
                                   )
        except:
            continue

    return "admin"
def users_id(update: Update, context: CallbackContext):
    id = context.user_data['id']
    userlar = Profile.objects.all()
    soni = userlar.count()
    context.bot.send_message(chat_id=id, text=f"number_of_users : {soni}",
                             reply_markup=ReplyKeyboardMarkup([["users_data","users_id"],["Homepage", "AdminPanel"]], resize_keyboard=True))

    for i in userlar:
        try:
            context.bot.send_message(chat_id=id, text=f"""{i.exeterenal_id}""",
                                     )
        except:
            continue

    return "admin"


# admin setting -------------------add,delete,admin data---**********8

def add_admin(update: Update, context: CallbackContext):
    id = context.user_data['id']

    update.message.reply_text("yangi admin ismini kiriting:")

    return "add_admin"
def add_admin_name(update: Update, context: CallbackContext):
    id = context.user_data['id']
    context.user_data['adminname'] = update.message.text
    update.message.reply_text("yangi admin telegram id sini kiriting :")

    return "add_admin_id"
def add_adminid(update: Update, context: CallbackContext):
    context.user_data['admin_id'] = update.message.text
    id = context.user_data['id']
    admin_id = context.user_data["admin_id"]
    admin_name = context.user_data["adminname"]
    update.message.reply_html(f"""
	admin ismi: {admin_name}
	admin id:   {admin_id}

	Tasdiqlaysizmi
	""", reply_markup=ReplyKeyboardMarkup([["Yes", "No"]], resize_keyboard=True))

    return "add_admin_confirm"
def add_adminconfirm(update: Update, context: CallbackContext):
    confirm_text = str(update.message.text)

    admin_id = context.user_data["admin_id"]
    admin_name = context.user_data["adminname"]

    if confirm_text == "Yes":
        admin, created = AdminPanel.objects.get_or_create(name=admin_name, admin_id=admin_id)
        update.message.reply_text(f"""
		ismi: {admin_name},
		id :{admin_id}

		admin qo'shildi


		""", reply_markup=ReplyKeyboardMarkup([["all_admins"], ["users"], ['Homepage']],
                                              resize_keyboard=True))
        return "admin"

    if confirm_text == "No":
        update.message.reply_text("Bekor qilindi ", reply_markup=button3)

        return "admin"
def admin_view(update: Update, context: CallbackContext):
    adminlar = AdminPanel.objects.all()

    for i in adminlar:
        update.message.reply_text(f"""{i.name}---{i.admin_id}""", reply_markup=ReplyKeyboardMarkup([["Add_admin","delete_admin"], ["Homepage"]],resize_keyboard=True))

    return "admin"
def delete_admin(update: Update, context: CallbackContext):
    update.message.reply_text("")
    pass


    return 'delete_admin'
def delete_admin_confirm(update:Update,context:CallbackContext):
    pass

####------for ads and sending message to all users-----------------------************
def send_message(update: Update, context: CallbackContext):
    update.message.reply_text("please send a message:",
                              reply_markup=ReplyKeyboardMarkup([["Homepage", "AdminPanel"]], resize_keyboard=True)
                              )
    return 'xabar'
def send_message_to_users(update: Update, context: CallbackContext):
    # print(update.message)
    users = Profile.objects.all()
    count = 0
    message = update.message
    for i in users:
        try:
            context.bot.forward_message(chat_id=i.exeterenal_id, from_chat_id=update.effective_user.id,
                                        message_id=message.message_id, protect_content=False)
            count += 1


        except:
            continue
    update.message.reply_text(f"""message sending to {count} users""",
                              reply_markup=ReplyKeyboardMarkup([["AdminPanel"]], resize_keyboard=True)
                              )
    return 'admin'

















conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', start),
        MessageHandler(Filters.regex('^(' + 'Restart' + ')$'), start), ],
    states={
        'bot': [
            MessageHandler(Filters.regex('^(' + 'Restart' + ')$'), start),
            CommandHandler('start', start),
            MessageHandler(Filters.text, url)
        ],
        'xabar': [
            CommandHandler('start', start),
            MessageHandler(Filters.regex('^(' + 'Homepage' + ')$'), start),
            MessageHandler(Filters.regex('^(' + 'AdminPanel' + ')$'), adminpanel),
            MessageHandler(Filters.all,send_message_to_users),
        ],
        'admin': [
            CommandHandler('start', start),
            MessageHandler(Filters.regex('^(' + 'Restart' + ')$'), start),
            MessageHandler(Filters.regex('^(' + 'Homepage' + ')$'), start),
            MessageHandler(Filters.regex('^(' + 'AdminPanel' + ')$'), adminpanel),
            MessageHandler(Filters.regex('^(' + 'users' + ')$'), users),
            MessageHandler(Filters.regex('^(' + 'users_data' + ')$'), users_data),
            MessageHandler(Filters.regex('^(' + 'users_id' + ')$'), users_id),
            MessageHandler(Filters.regex('^(' + "send_message" + ')$'), send_message),
            MessageHandler(Filters.regex('^(' + 'all_admins' + ')$'), admin_view),
            MessageHandler(Filters.regex('^(' + "Add_admin" + ')$'), add_admin),
            MessageHandler(Filters.regex('^(' + "delete_admin" + ')$'), delete_admin),
            MessageHandler(Filters.text, url),
        ],
        "add_admin": [
            MessageHandler(Filters.regex('^(' + 'Restart' + ')$'), start),
            MessageHandler(Filters.regex('^(' + 'Homepage' + ')$'), start),
            MessageHandler(Filters.text, add_admin_name)
        ],
        "add_admin_id": [
            MessageHandler(Filters.regex('^(' + 'Restart' + ')$'), start),
            MessageHandler(Filters.regex('^(' + 'Homepage' + ')$'), start),
            MessageHandler(Filters.text, add_adminid)
        ],
        "add_admin_confirm": [
            MessageHandler(Filters.regex('^(' + 'Restart' + ')$'), start),
            MessageHandler(Filters.regex('^(' + 'Homepage' + ')$'), start),
            MessageHandler(Filters.text, add_adminconfirm)
        ],
        'callback': [
            CallbackQueryHandler(download_check),
            MessageHandler(Filters.regex('^(' + 'Restart' + ')$'), start),
            CommandHandler('start', start), ],
        'delete_admin':[
            CallbackQueryHandler(delete_admin_confirm)]
    },
    fallbacks=[
        MessageHandler(Filters.regex('^(' + 'Restart' + ')$'), start),
        CommandHandler('start', start),]
)
#########################################################################











updater = Updater(settings.TOKEN1)

updater.dispatcher.add_handler(conv_handler)


updater.start_polling()
updater.idle()