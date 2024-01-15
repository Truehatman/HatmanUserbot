from sched import scheduler
from pyrogram import Client, filters, idle
from pyrogram.raw.functions.messages import StartBot, DeleteHistory, InstallStickerSet
from pyrogram.raw.functions.help import GetUserInfo
from pyrogram.errors import * 
from pyrogram.errors import UsernameInvalid
from pyrogram.enums import ChatType, ParseMode, UserStatus
from pyrogram.raw.functions.account import UpdateNotifySettings
from pyrogram.raw.base import InputPeer
from pyrogram.raw.types import InputPeerNotifySettings, InputNotifyPeer, InputPeerChat, Message
import asyncio
import time
import asyncio
import datetime
from multiprocessing import get_context
import os
import traceback
import requests
import validators
from pathlib import Path
from random import randint
import json
import random
import string
from random import randint
import time
ubot = Client("killersession", api_id=28, api_hash="542", lang_code="it")
ubot.start()

IDSSS, usernamesss = (ubot.get_me()).id, (ubot.get_me()).username
statusse = False
ignore = []

# Addword
class Database:
    def __init__(self, file_name: str):
        self.database = file_name
        if os.path.exists(file_name) == False:
            f = open(file_name, "a+")
            f.write(json.dumps({"word": {}, "wordr": {}, "sticker": False}))
            f.close()

    async def save(self, update: dict):
        os.remove(self.database)
        f = open(self.database, "a+")
        f.write(json.dumps(update))
        f.close()

    async def add_word(self, word: str, risposta: str):
        update = json.load(open(self.database))
        update["word"][str(word)] = risposta
        await self.save(update)
        return json.load(open(self.database))["word"][word]

    async def add_wordr(self, word: str, risposta: str):
        update = json.load(open(self.database))
        update["wordr"][str(word)] = risposta
        await self.save(update)
        return json.load(open(self.database))["wordr"][word]
word = Database("word.json")

paypal_link = None

gruppi = []


@ubot.on_message(filters.user("self") & filters.command("help", "."))
async def help_command(client, message):
    await message.reply_text("https://telegra.ph/HatmanUserbot-01-14")

@ubot.on_message(filters.user("self") & filters.command("dev", "."))
async def creator_command(client, message):
    await message.reply_text("I am developed by @hatmanexchanger!")

@ubot.on_message(filters.user("self") & filters.command("percentuale", "."))
async def percentage_command(client, message):
    # Estrai il testo del messaggio dopo il comando
    command_text = message.text.split(' ', 2)[1:]

    try:
        # Estrai i valori del numero e della percentuale
        numero = float(command_text[0])
        percentuale = float(command_text[1])

        # Calcola la percentuale
        risultato = (percentuale / 100) * numero

        # Invia la risposta
        await message.reply_text(f"{percentuale}% of {numero} is {risultato}")
    except (ValueError, IndexError):
        # Gestisce il caso in cui la conversione o l'accesso ai valori fallisce
        await message.reply_text("Right command is: .percentage [number] [percentage]")

@ubot.on_message(filters.user("self") & filters.command("addgroup", "."))
async def add_group_command(client, message):
    try:
        # Estrai il testo del messaggio dopo il comando
        command_text = message.text.split(' ', 1)[1]
        gruppo_id = int(command_text)

        # Aggiungi il gruppo alla lista con un messaggio di default solo se non Ã¨ giÃ  presente
        if gruppo_id not in gruppi:
            gruppi[gruppo_id] = {'intervallo': 5, 'messaggio': ""}
            await message.reply_text(f"Group {gruppo_id} added to the list.")
        else:
            await message.reply_text(f"Group is already in the list {gruppo_id}.")
    except (ValueError, IndexError):
        await message.reply_text("Right command: .addgroup [id_group]")

@ubot.on_message(filters.user("self") & filters.command("spam", "."))
async def spam_command(client, message):
    try:
        # Estrai il testo del messaggio dopo il comando
        command_text = message.text.split(' ', 2)[1:]
        intervallo = int(command_text[0])
        messaggio = command_text[1]

        # Imposta l'intervallo e il messaggio di spam per il gruppo specifico
        gruppo_id = message.chat.id
        gruppi[gruppo_id] = {'intervallo': intervallo, 'messaggio': messaggio}

        # Pianifica l'invio del messaggio al gruppo ogni intervallo specificato
        scheduler.every(intervallo).minutes.do(send_spam, client, gruppo_id)

        await message.reply_text(f"Spam on! i will send the message every {intervallo} minutes.")
    except (ValueError, IndexError):
        await message.reply_text("Right command: .spam [minutes] [message]")

def send_spam(client, gruppo_id):
    try:
        # Invia il messaggio di spam al gruppo specifico
        client.send_message(gruppo_id, gruppi[gruppo_id]['messaggio'])
    except Exception as e:
        print(f"error while the sending of the message in group {gruppo_id}: {e}")

@ubot.on_message(filters.user("self") & filters.command("listgroup", "."))
async def list_groups_command(client, message):
    elenco_gruppi = "\n".join([f"{gruppo_id}: {client.get_chat(gruppo_id).title}" for gruppo_id in gruppi])
    await message.reply_text(f"List of groups:\n{elenco_gruppi}")

@Client.on_message(filters.command("stopspam"))
async def stop_spam_command(client, message):
    try:
        # Interrompi la pianificazione per tutti i gruppi
        for group_id in gruppi:
            schedule.clear(f'send_spam_{group_id}')
        
        await message.reply_text("Spam stopped successfully.")
    except Exception as e:
        print(f"Error while stopping spam  {e}")
        await message.reply_text("Error while stopping spam")

@ubot.on_message(filters.user("self") & filters.command("cloud", "."))
async def save_to_cloud(client, message):
    try:
        # Estrai il messaggio a cui si sta rispondendo
        replied_message = message.reply_to_message

        # Salva il messaggio nei messaggi salvati
        await client.save_file(replied_message, file_name="")

        await message.reply_text("Message correctly saved")
    except Exception as e:
        print(f"Error while the saving of the message: {e}")

@ubot.on_message(filters.user("self") & filters.command("paypal", "."))
async def set_paypal_link(client, message):
    global paypal_link
    try:
        # Estrai il testo del messaggio dopo il comando
        command_text = message.text.split(' ', 1)[1]
        link_paypal = command_text

        # Imposta il link PayPal generico
        paypal_link = link_paypal

        await message.reply_text("Link PayPal set successfully.")
    except (IndexError, ValueError):
        await message.reply_text("Right command: .paypal [link_paypal]")

@ubot.on_message(filters.user("self") & filters.command("pp", "."))
async def show_paypal_link(client, message):
    if paypal_link:
        await message.reply_text(f"Link PayPal:\n{paypal_link}")
    else:
        await message.reply_text("No link PayPal set. Use .paypal perto set a link.")
        
@ubot.on_message(filters.user("self") & filters.command("paypal", "."))
async def block_user(client, message):
    try:
        # Estrai l'ID dell'utente a cui si sta rispondendo
        user_id = message.reply_to_message.from_user.id

        # Blocca l'utente
        await client.block_user(user_id)

        await message.reply_text("User blocked.")
    except Exception as e:
        print(f"Error while blocking the user:{e}")
        await message.reply_text("Error while blocking the user.")

@ubot.on_message(filters.command("unblock", ".") & filters.reply)
async def unblock_user(client, message):
    try:
        # Estrai l'ID dell'utente a cui si sta rispondendo
        user_id = message.reply_to_message.from_user.id

        # Sblocca l'utente
        await client.unblock_user(user_id)

        await message.reply_text("Iser blocked successfully.")
    except Exception as e:
        print(f"Error while blocking user: {e}")
        await message.reply_text("Error while blocking user.")

@ubot.on_message(filters.command("mute", ".") & filters.reply)
async def mute_user(client, message):
    try:
        # Estrai l'ID dell'utente a cui si sta rispondendo
        user_id = message.reply_to_message.from_user.id

        # Muta l'utente
        await client.restrict_chat_member(message.chat.id, user_id, ChatPermissions())

        await message.reply_text("User muted successfully.")
    except Exception as e:
        print(f"Error while muting user: {e}")
        await message.reply_text("Error while muting user.")
        
@ubot.on_message(filters.command("unmute", ".") & filters.reply)
async def unmute_user(client, message):
    try:
        # Estrai l'ID dell'utente a cui si sta rispondendo
        user_id = message.reply_to_message.from_user.id

        # Rimuovi la muta dall'utente
        await client.restrict_chat_member(message.chat.id, user_id, ChatPermissions(can_send_messages=True))

        await message.reply_text("User unmuted successfully.")
    except Exception as e:
        print(f"Error while unmuting user {e}")
        await message.reply_text("Error while unmuting user.")

idle()