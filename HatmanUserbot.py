

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
from pyrogram.types import Message
from typing import Union
from typing import List
from pyrogram import types
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
from pyrogram.errors import PeerIdInvalid

print("HatManUserbot started..")
print("#######################")

ubot = Client("killersession", api_id=25047326,
              api_hash="9673ea812441c77e912979cd0f8a2572", lang_code="it")
ubot.start()

IDSSS, usernamesss = (ubot.get_me()).id, (ubot.get_me()).username
statusse = False
ignore = []

# Addword

try:
    userbotspammer = sqlite3.connect("userbot.db")
    userbotspammer.cursor().execute("CREATE TABLE IF NOT EXISTS gruppi (chatid INT)")
    userbotspammer.cursor().execute(
        "CREATE TABLE IF NOT EXISTS paypal_links (id INTEGER PRIMARY KEY, link TEXT)")
    userbotspammer.cursor().execute(
        "CREATE TABLE IF NOT EXISTS litecoin_links (id INTEGER PRIMARY KEY, link TEXT)")
    userbotspammer.cursor().execute(
        "CREATE TABLE IF NOT EXISTS bitcoin_links (id INTEGER PRIMARY KEY, link TEXT)")
    userbotspammer.cursor().execute(
        "CREATE TABLE IF NOT EXISTS ethereum_links (id INTEGER PRIMARY KEY, link TEXT)")
    userbotspammer.cursor().execute(
        "CREATE TABLE IF NOT EXISTS revolut_links (id INTEGER PRIMARY KEY, link TEXT)")
except:
    pass


async def save_link(link, table_name):
                    try:
                        # Elimina eventuali link esistenti nella tabella specificata
                        cursor.execute(f"DELETE FROM {table_name}")

                        # Inserisci il nuovo link
                        cursor.execute(
                            f"INSERT INTO {table_name} (link) VALUES (?)", (link,))
                        userbotspammer.commit()
                    except Exception as e:
                        print(f"Errore durante il salvataggio del link: {e}")

                async def load_link(table_name):
                    try:
                        cursor.execute(f"SELECT link FROM {table_name} LIMIT 1")
                        result = cursor.fetchone()
                        if result:
                            return result[0]
                        else:
                            return None
                    except Exception as e:
                        print(f"Errore durante il recupero del link: {e}")
                        return None


spamcheck = false

muted_users = {}
scheduled_tasks = {}


@ubot.on_message(filters.user("self") & filters.command("addgroup", "."))
async def groupadd(_, message):
    try:
        print(message.chat.type)
        if str(message.chat.type) == "ChatType.GROUP":
            group = message.chat.id
            gruppo = await ubot.get_chat(group)
            userbotspammer.cursor().execute("INSERT INTO gruppi (chatid) VALUES (?)", [gruppo.id])
            userbotspammer.commit()
            try:
                await ubot.join_chat(gruppo)
            except:
                pass
            await message.edit(f"Group {gruppo.title} added")
        else:
            group = message.text.split(" ")[1]
            gruppo = await ubot.get_chat(group)
            userbotspammer.cursor().execute("INSERT INTO gruppi (chatid) VALUES (?)", [gruppo.id])
            userbotspammer.commit()
            try:
                await ubot.join_chat(group)
            except:
                pass
            await message.edit(f"{gruppo.title} added!")
    except:
        traceback.print_exc() #errori
        await message.edit(" Error in .addgroup!")

@ubot.on_message(filters.user("self") & filters.command("remgroup", "."))
async def rimuovigruppo(_, message):
    try:
        count = userbotspammer.cursor().execute("SELECT COUNT(chatid) FROM gruppi").fetchone()[0]
        if count == 0:
            await message.edit(" There are no group")
        else:
            group = await ubot.get_chat(message.text.split(" ")[1])
            userbotspammer.cursor().execute("DELETE FROM gruppi WHERE chatid = ?", [group.id])
            userbotspammer.commit()
            await message.edit(f" Group {group.title} removed")
    except:
        group = await ubot.get_chat(message.text.split(" ")[1])
        await message.edit(f" Error in .remgroup {group.title}")

@ubot.on_message(filters.user("self") & filters.command("grouplist", "."))
async def listagruppi(_, message):
    count = userbotspammer.cursor().execute("SELECT COUNT(chatid) FROM gruppi").fetchone()[0]
    if count == 0:
        await message.edit(" There are  no group!")
    else:
        gruppimsg = ""
        for gruppi, in userbotspammer.cursor().execute("SELECT chatid FROM gruppi").fetchall():
            gruppimsg += f"â¥ {(await ubot.get_chat(gruppi)).title} | <code>{(await ubot.get_chat(gruppi)).id}</code>

"
        await message.edit(f"<b> Group list:</b>

{gruppimsg}")
        

timespam = None
messaggio = ""

@ubot.on_message(filters.user("self") & filters.command("time", "."))
async def tempo(_, message):
    global timespam
    minuti = message.text.split(" ")[1]
    if len(message.text.split(" ")) > 1:
        try:
            int(minuti)
            secondi = minuti * 60
            if secondi >= 300:
                timespam = int(minuti)
                await message.edit(f"Time set on {timespam} minutes")
                pass
            else:
                await message.edit("Min is 5 minutes")
                return
        except:
            return await message.edit(" put time in minutes")

@ubot.on_message(filters.user("self") & filters.command("setmex", "."))
async def setmex(_, message):
    global messaggio
    try:
        messaggio = message.text.replace(f".setmex", "")
        await message.edit(f" Message set

 <code>{messaggio}</code>")
    except:
        await message.edit("Wrong format, .setmex Messaggio")

@ubot.on_message(filters.user("self") & filters.command("spam", "."))
async def spamavviato(_, message):
    global spamcheck
    count = userbotspammer.cursor().execute("SELECT COUNT(chatid) FROM gruppi").fetchone()[0]
    if count == 0:
        await message.edit(" There are no group!")
    else:
        if not spamcheck:
            spamcheck = True
            await message.edit(f" Spam started in {count} group")
            while spamcheck:
                for gruppi, in userbotspammer.cursor().execute("SELECT chatid FROM gruppi").fetchall():
                    try:
                        await ubot.send_message(gruppi, messaggio)
                        await asyncio.sleep(0.5)
                    except:
                         await asyncio.sleep(0.5)
                await asyncio.sleep(int(timespam))
        else:
            await message.edit("wrong format, .spam")




@ubot.on_message(filters.user("self") & filters.command("stop", "."))
async def stopspam(_, message):
    global spamcheck
    if spamcheck:
        spamcheck = False
        await message.edit(" Spam end")
    else:
        await message.edit(" Spam not started yet")



@ubot.on_message(filters.user("self") & filters.command("help", prefixes="."))
async def help_command(client, message):
    await message.edit_text("https://telegra.ph/HatmanUserbot-01-14")

@ubot.on_message(filters.user("self") & filters.command("dev", prefixes="."))
async def creator_command(client, message):
    await message.edit_text("I am developed by @hatmanexchanger!")

@ubot.on_message(filters.user("self") & filters.command("percentage", prefixes="."))
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

@ubot.on_message(filters.user("self") & filters.command("setlink", "."))
async def set_generic_link(client, message):
    try:
        command_parts = message.text.split(' ', 2)
        table_name = command_parts[1]
        link_value = command_parts[2]

        await save_link(link_value, table_name)

        await message.edit_text(f"Link for {table_name} set successfully.")
    except (IndexError, ValueError):
        await message.edit_text("Right command: .setlink [table_name] [link_value]")

@ubot.on_message(filters.user("self") & filters.command("getlink", "."))
async def get_generic_link(client, message):
    try:
        table_name = message.text.split(' ', 1)[1]

        link_value = await load_link(table_name)
        if link_value:
            await message.edit_text(f"Link for {table_name}:\n{link_value}")
        else:
            await message.edit_text(f"No link set for {table_name}. Use .setlink to set a link.")
    except (IndexError, ValueError):
        await message.edit_text("Right command: .getlink [table_name]")
        
@ubot.on_message(filters.user("self") & filters.regex(r'^\.[a-zA-Z0-9_]+$'))
async def direct_link_command(client, message):
    try:
        table_name = message.text[1:]

        link_value = await load_link(table_name)
        if link_value:
            await message.edit_text(f"{link_value}")
        else:
            await message.edit_text(f"No link set for {table_name}. Use .setlink to set a link.")
    except (IndexError, ValueError):
        await message.edit_text(f"Right command format: .{table_name}")
       
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
        # Verifica se l'utente ÃÂ¨ muteato e se il mittente ÃÂ¨ valido
        if message.from_user and message.from_user.id in muted_users:
            # Elimina il messaggio
            await message.delete()
    except Exception as e:
        print(f"Error while deleting muted user's message: {e}")

idle()


