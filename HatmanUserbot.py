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
from pyrogram.types import ChatPermissions
from typing import Union
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
import sqlite3
ubot = Client("killersession", api_id=25047326, api_hash="9673ea812441c77e912979cd0f8a2572", lang_code="it")
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
            f.write(json.dumps({"word": {}, "wordr": {}, "sticker": False, "gruppi": {}}))
            f.close()

    async def save(self, update: dict):
        os.remove(self.database)
        f = open(self.database, "a+")
        f.write(json.dumps(update))
        f.close()

    async def add_group(self, chat_id: int, intervallo: int, messaggio: str):
        update = json.load(open(self.database))
        gruppi = update.setdefault("gruppi", {})
        gruppi[chat_id] = {"intervallo": intervallo, "messaggio": messaggio}
        await self.save(update)
        return gruppi[chat_id]
        
   async def del_group(self, chat_id: Union[int, str]):
        try:
            chat_id_str = str(chat_id)
            update = json.load(open(self.database))
            gruppi = update.setdefault("gruppi", {})

            print(f"Before deletion - Groups: {gruppi}")

            if chat_id_str in gruppi:
                del gruppi[chat_id_str]
                await self.save(update)

                print(f"After deletion - Groups: {gruppi}")

                return True
            else:
                print(f"Group ID {chat_id_str} not found in the list.")
                return False
        except Exception as e:
            print(f"Error during del_group: {e}")
            return False

    async def get_groups(self):
        update = json.load(open(self.database))
        gruppi = update.setdefault("gruppi", {})
        return gruppi

word = Database("word.json")

paypal_link = None
litecoin_link = None
gruppi = {}
muted_users = {}
scheduled_tasks = {}

@ubot.on_message(filters.user("self") & filters.command("help", "."))
async def help_command(client, message):
    await message.edit_text("https://telegra.ph/HatmanUserbot-01-14")

@ubot.on_message(filters.user("self") & filters.command("dev", "."))
async def creator_command(client, message):
    await message.edit_text("I am developed by @hatmanexchanger!")

@ubot.on_message(filters.user("self") & filters.command("percentage", "."))
async def percentage_command(client, message):
    # Estrai il testo del messaggio dopo il comando
    command_text = message.text.split(' ', 2)[1:]

    try:
        # Estrai i valori del numero e della percentuale
        numero = float(command_text[0])
        percentuale = float(command_text[1])

        # Calcola la percentuale
        risultato1 = (percentuale / 100) * numero
        risultato2 = numero - risultato1

        # Invia la risposta
        await message.edit_text(f"{percentuale}% of {numero} is {risultato1} and {numero} - {risultato1} is {risultato2} ")
    except (ValueError, IndexError):
        # Gestisce il caso in cui la conversione o l'accesso ai valori fallisce
        await message.edit_text("Right command is: .percentage [number] [percentage]")

@ubot.on_message(filters.user("self") & filters.command("addgroup", prefixes="."))
async def add_group_command(client, message):
    try:
        # Estrai il testo del messaggio dopo il comando
        command_text = message.text.split(' ', 1)[1]

        # Ottieni l'ID del gruppo a partire dal suo username o ID
        try:
            chat = await client.get_chat(chat_id=command_text)
            gruppo_id = chat.id
        except ValueError:
            gruppo_id = None

        # Aggiungi il gruppo al database
        if gruppo_id is not None:
            group_settings = await word.add_group(gruppo_id, intervallo=5, messaggio="")
            await message.edit_text(f"Group {gruppo_id} added to the list with settings: {group_settings}")
        else:
            await message.edit_text("Invalid group ID or username.")
    except (ValueError, IndexError):
        await message.edit_text("Right command: .addgroup [id_group] or [username]")

@ubot.on_message(filters.user("self") & filters.command("grouplist", prefixes="."))
async def group_list_command(client, message):
    try:
        groups = await word.get_groups()
        if groups:
            group_list = "\n".join([f"{chat_id} (@{group_data['username']})" if 'username' in group_data else f"{chat_id}" for chat_id, group_data in groups.items()])
            await message.edit_text(f"Group list:\n{group_list}")
        else:
            await message.edit_text("No groups found.")
    except Exception as e:
        print(f"Error while fetching group list: {e}")
        await message.edit_text("Error while fetching group list.")

@ubot.on_message(filters.user("self") & filters.command("delgroup", prefixes="."))
async def del_group_command(client, message):
    try:
        # Estrai il testo del messaggio dopo il comando
        command_text = message.text.split(' ', 1)[1]

        # Cerca di ottenere direttamente l'ID del gruppo senza sollevare eccezioni
        chat_id = None

        try:
            chat_id = int(command_text)
        except ValueError:
            pass

        if chat_id is None:
            try:
                chat = await client.get_chat(command_text)
                chat_id = chat.id
            except Exception:
                pass

        # Rimuovi il gruppo dalla lista e dal database
        if chat_id is not None:
            await word.del_group(chat_id)
            if str(chat_id) in gruppi:
                del gruppi[str(chat_id)]
                await message.edit_text(f"Group {chat_id} removed from the list and database.")
            else:
                await message.edit_text(f"Group {chat_id} is not in the list.")
        else:
            await message.edit_text("Invalid group ID or username.")
    except (ValueError, IndexError):
        await message.edit_text("Right command: .delgroup [id_group] or [username]")

@ubot.on_message(filters.user("self") & filters.command("spam", prefixes="."))
async def spam_command(client, message):
    try:
        global scheduled_tasks
        command_text = message.text.split(' ', 2)[1:]
        intervallo = int(command_text[0])
        messaggio = command_text[1]

        for gruppo_id in gruppi:
            if gruppo_id in scheduled_tasks:
                scheduled_tasks[gruppo_id].cancel()

            gruppi[gruppo_id] = {'intervallo': intervallo, 'messaggio': messaggio}
            task = asyncio.create_task(send_spam(client, gruppo_id))

            scheduled_tasks[gruppo_id] = asyncio.ensure_future(
                asyncio.sleep(intervallo * 60)
            )
        await message.edit_text(f"Spam on! I will send the message every {intervallo} minutes in all groups.")
    except (ValueError, IndexError):
        await message.edit_text("Right command: .spam [minutes] [message]")

@ubot.on_message(filters.command("stopspam", prefixes="."))
async def stop_spam_command(client, message):
    try:
        global scheduled_tasks
        for gruppo_id in gruppi:
            if gruppo_id in scheduled_tasks:
                scheduled_tasks[gruppo_id].cancel()
                await asyncio.sleep(1)  # Aggiunto per evitare sovrapposizioni nella cancellazione
                del scheduled_tasks[gruppo_id]

        await message.edit_text("Spam stopped successfully.")
    except Exception as e:
        print(f"Error while stopping spam: {e}")
        await message.edit_text("Error while stopping spam")

async def send_spam(client, gruppo_id):
    try:
        while True:
            await client.send_message(gruppo_id, gruppi[gruppo_id]['messaggio'])
            await asyncio.sleep(gruppi[gruppo_id]['intervallo'] * 60)
    except asyncio.CancelledError:
        print(f"Spam task cancelled for group {gruppo_id}")
    except Exception as e:
        print(f"Error while sending the message in group {gruppo_id}: {e}")

@ubot.on_message(filters.user("self") & filters.command("ppset", "."))
async def set_paypal_link(client, message):
    global paypal_link
    try:
        # Estrai il testo del messaggio dopo il comando
        command_text = message.text.split(' ', 1)[1]
        link_paypal = command_text

        # Imposta il link PayPal generico
        paypal_link = link_paypal

        await message.edit_text("Link PayPal set successfully.")
    except (IndexError, ValueError):
        await message.edit_text("Right command: .ppset [link_paypal]")

@ubot.on_message(filters.user("self") & filters.command("pp", "."))
async def show_paypal_link(client, message):
    if paypal_link:
        await message.edit_text(f"Link PayPal:\n{paypal_link}")
    else:
        await message.edit_text("No link PayPal set. Use .ppset to set a link.")

@ubot.on_message(filters.user("self") & filters.command("ltcset", "."))
async def set_litecoin_link(client, message):
    global litecoin_link
    try:
        # Estrai il testo del messaggio dopo il comando
        command_text = message.text.split(' ', 1)[1]
        link_litecoin = command_text

        # Imposta il link Litecoin generico
        litecoin_link = link_litecoin

        await message.edit_text("Ltc address set successfully.")
    except (IndexError, ValueError):
        await message.edit_text("Right command: .ltcset [Address]")

@ubot.on_message(filters.user("self") & filters.command("ltc", "."))
async def show_litecoin_link(client, message):
    if litecoin_link:
        await message.edit_text(f"{litecoin_link}")
    else:
        await message.edit_text("No ltc address  set. Use .ltcset to set a link.")
       
@ubot.on_message(filters.user("self") & filters.command("block", "."))
async def block_user(client, message):
    try:
        # Estrai l'ID dell'utente a cui si sta rispondendo
        user_id = message.reply_to_message.from_user.id

        # Blocca l'utente
        await client.block_user(user_id)

        await message.edit_text("User blocked.")
    except Exception as e:
        print(f"Error while blocking the user:{e}")
        await message.edit_text("Error while blocking the user.")

@ubot.on_message(filters.command("unblock", ".") & filters.reply)
async def unblock_user(client, message):
    try:
        # Estrai l'ID dell'utente a cui si sta rispondendo
        user_id = message.reply_to_message.from_user.id

        # Sblocca l'utente
        await client.unblock_user(user_id)

        await message.edit_text("User unblocked successfully.")
    except Exception as e:
        print(f"Error while unblocking user: {e}")
        await message.edit_text("Error while unblocking user.")

# Comando per disattivare le notifiche per un utente in risposta
@ubot.on_message(filters.command("mute", ".") & filters.reply)
async def mute_user(client, message):
    try:
        # Estrai l'ID dell'utente a cui si sta rispondendo
        user_id = message.reply_to_message.from_user.id

        # Aggiungi l'utente al dizionario dei muteati
        muted_users[user_id] = True
        
        await message.edit_text("User muted successfully.")
    except Exception as e:
        print(f"Error while muting user: {e}")
        await message.edit_text("Error while muting user.")
        
@ubot.on_message(filters.command("unmute", ".") & filters.reply)
async def unmute_user(client, message):
    try:
        # Estrai l'ID dell'utente a cui si sta rispondendo
        user_id = message.reply_to_message.from_user.id

        # Rimuovi l'utente dal dizionario dei muteati
        muted_users.pop(user_id, None)

        await message.edit_text("User unmuted successfully.")
    except Exception as e:
        print(f"Error while unmuting user {e}")
        await message.edit_text("Error while unmuting user.")

# Handler per eliminare i messaggi degli utenti muteati
@ubot.on_message(filters.text)
async def delete_muted_messages(client, message):
    try:
        # Verifica se l'utente è muteato e se il mittente è valido
        if message.from_user and message.from_user.id in muted_users:
            # Elimina il messaggio
            await message.delete()
    except Exception as e:
        print(f"Error while deleting muted user's message: {e}")

idle()
