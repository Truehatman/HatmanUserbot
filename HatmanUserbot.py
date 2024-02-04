##HatmanUserbot
import pyrogram
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
import subprocess
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
    userbotspammer.cursor().execute("CREATE TABLE IF NOT EXISTS muted_users (user_id INT)")
except Exception as e:
    print(f"Error connecting to the database: {e}")
except:
    pass

async def create_table_if_not_exists(table_name, connection):
    cursor = connection.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, link TEXT)")
    connection.commit()

async def save_link(link, table_name, connection):
    try:
        await create_table_if_not_exists(table_name, connection)
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {table_name}")
        cursor.execute(f"INSERT INTO {table_name} (link) VALUES (?)", (link,))
        connection.commit()
    except Exception as e:
        print(f"Errore durante il salvataggio del link: {e}")

async def load_link(table_name, connection):
    try:
        await create_table_if_not_exists(table_name, connection)
        cursor = connection.cursor()
        cursor.execute(f"SELECT link FROM {table_name} LIMIT 1")
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        print(f"Errore durante il recupero del link: {e}")
        return None

async def delete_link(table_name, connection):
    try:
        await create_table_if_not_exists(table_name, connection)
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {table_name}")
        connection.commit()
    except Exception as e:
        print(f"Errore durante l'eliminazione del link: {e}")

spamcheck = False

muted_users = {}
scheduled_tasks = {}






@ubot.on_message(filters.user("self") & filters.command("addgroup", "."))
async def groupadd(_, message):
    try:
        if message.chat.type == "group":
            group_id = message.chat.id
            if not is_group_in_list(group_id):
                userbotspammer.cursor().execute("INSERT INTO gruppi (chatid) VALUES (?)", [group_id])
                userbotspammer.commit()
                try:
                    await ubot.join_chat(group_id)
                except:
                    pass

                chat_info = await ubot.get_chat(group_id)
                chat_username = chat_info.username if chat_info.username else f"ID: {group_id}"

                await message.edit(f"Group @{chat_username} added")
            else:
                await message.edit("Group is already in the list.")
        elif message.text == ".addgroup":
            await message.edit("Please use .addgroup in a group chat to add it.")
        else:
            group_id = message.text.split(" ")[1]
            if not is_group_in_list(group_id):
                userbotspammer.cursor().execute("INSERT INTO gruppi (chatid) VALUES (?)", [group_id])
                userbotspammer.commit()
                try:
                    await ubot.join_chat(group_id)
                except:
                    pass

                chat_info = await ubot.get_chat(group_id)
                chat_username = chat_info.username if chat_info.username else f"ID: {group_id}"

                await message.edit(f"Group @{chat_username} added!")
            else:
                await message.edit("Group is already in the list.")
    except Exception as e:
        print(e)
        await message.edit("Error in .addgroup!")

@ubot.on_message(filters.user("self") & filters.command("remgroup", "."))
async def group_remove(_, message):
    try:
        if message.chat.type == "group":
            group_id = message.chat.id
            if is_group_in_list(group_id):
                userbotspammer.cursor().execute("DELETE FROM gruppi WHERE chatid=?", [group_id])
                userbotspammer.commit()

                chat_info = await ubot.get_chat(group_id)
                chat_username = chat_info.username if chat_info.username else f"ID: {group_id}"

                await message.edit(f"Group @{chat_username} removed")
            else:
                await message.edit("Group is not in the list.")
        elif message.text == ".remgroup":
            await message.edit("Please use .remgroup in a group chat to remove it.")
        else:
            group_id = message.text.split(" ")[1]
            if is_group_in_list(group_id):
                userbotspammer.cursor().execute("DELETE FROM gruppi WHERE chatid=?", [group_id])
                userbotspammer.commit()

                chat_info = await ubot.get_chat(group_id)
                chat_username = chat_info.username if chat_info.username else f"ID: {group_id}"

                await message.edit(f"Group @{chat_username} removed!")
            else:
                await message.edit("Group is not in the list.")
    except Exception as e:
        print(e)
        await message.edit("Error in .remgroup!")

def is_group_in_list(group_id):
    result = userbotspammer.cursor().execute("SELECT COUNT(chatid) FROM gruppi WHERE chatid = ?", [group_id]).fetchone()[0]
    return result > 0

# Funzione per avviare la lista dei gruppi
@ubot.on_message(filters.user("self") & filters.command("grouplist", "."))
async def listagruppi(_, message):
    try:
        count = userbotspammer.cursor().execute("SELECT COUNT(chatid) FROM gruppi").fetchone()[0]

        if count == 0:
            await message.edit("There are no groups!")
        else:
            gruppimsg = ""
            for gruppi, in userbotspammer.cursor().execute("SELECT chatid FROM gruppi").fetchall():
                try:
                    chat_info = await ubot.get_chat(gruppi)
                    chat_title = chat_info.title if chat_info.title else f"Group ID: {gruppi}"
                    gruppimsg += f"➥ {chat_title} | <code>{gruppi}</code>\n"
                except pyrogram.errors.UsernameNotOccupied:
                    gruppimsg += f"➥ Group ID: <code>{gruppi}</code>\n"
                except Exception as e:
                    print(f"Error processing group {gruppi}: {e}")
                    
            print(f"Group list:\n{gruppimsg}")  # Aggiunta di una stampa per il debug
            await message.edit(f"<b>Group list:</b>\n{gruppimsg}")
    
    except Exception as e:
        print(f"Error in .grouplist: {e}")
        await message.edit("Error in .grouplist!")

# Funzione per il reset della lista dei gruppi
@ubot.on_message(filters.user("self") & filters.command("resetgrouplist", "."))
async def reset_grouplist(_, message):
    try:
        # Elimina tutti i dati dalla tabella 'gruppi'
        userbotspammer.cursor().execute("DELETE FROM gruppi")
        userbotspammer.commit()

        await message.edit("Group list reset successfully!")
    except Exception as e:
        print(f"Error in .resetgrouplist: {e}")
        await message.edit("Error resetting group list!")

@ubot.on_message(filters.user("self") & filters.command("time", "."))
async def tempo(_, message):
    global timespam
    if len(message.text.split(" ")) > 1:
        minuti = message.text.split(" ")[1]
        try:
            minuti = int(minuti)
            if minuti >= 5:
                timespam = minuti
                await message.edit(f"Time set on {timespam} minutes")
            else:
                await message.edit("Min is 5 minutes")
        except ValueError:
            await message.edit("Put a valid integer for the time in minutes")
    else:
        await message.edit("Please specify the time in minutes.")

@ubot.on_message(filters.user("self") & filters.command("setmex", "."))
async def setmex(_, message):
    global messaggio
    try:
        messaggio = message.text.replace(f".setmex", "")
        await message.edit(f"Message set <code>{messaggio}</code>")
    except:
        await message.edit("Wrong format, .setmex Messaggio")

@ubot.on_message(filters.user("self") & filters.command("spam", "."))
async def spamavviato(_, message):
    global spamcheck
    count = userbotspammer.cursor().execute("SELECT COUNT(chatid) FROM gruppi").fetchone()[0]
    if count == 0:
        await message.edit("There are no groups!")
    else:
        if not spamcheck:
            spamcheck = True
            await message.edit(f"Spam started in {count} groups")
            while spamcheck:
                for gruppi, in userbotspammer.cursor().execute("SELECT chatid FROM gruppi").fetchall():
                    try:
                        await ubot.send_message(gruppi, messaggio)
                        await asyncio.sleep(0.7)
                    except:
                         await asyncio.sleep(0.7)
                await asyncio.sleep(timespam * 60)
            spamcheck = False  # Assicurati di reimpostare spamcheck dopo il ciclo di spam
        else:
            await message.edit("Wrong format, .spam")




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
    await message.edit_text("I am developed by @TrueHatman!")

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

def is_user_muted(user_id):
    try:
        cursor = userbotspammer.cursor()
        cursor.execute("SELECT * FROM muted_users WHERE user_id = ?", [user_id])
        result = cursor.fetchone()

        return result is not None  # Restituisce True se l'utente è già mutato, altrimenti False
    except Exception as e:
        print(f"Error checking if user is muted: {e}")
        return False


@ubot.on_message(filters.command("mute", ".") & filters.reply)
async def mute_user(_, message):
    try:
        user_id = message.reply_to_message.from_user.id

        if not is_user_muted(user_id):
            userbotspammer.cursor().execute("INSERT INTO muted_users (user_id) VALUES (?)", [user_id])
            userbotspammer.commit()
            await message.edit_text("User muted successfully.")
        else:
            await message.edit_text("User is already muted.")
    except Exception as e:
        print(f"Error while muting user: {e}")
        await message.edit_text("Error while muting user.")

@ubot.on_message(filters.command("unmute", ".") & filters.reply)
async def unmute_user(_, message):
    try:
        user_id = message.reply_to_message.from_user.id

        if is_user_muted(user_id):
            userbotspammer.cursor().execute("DELETE FROM muted_users WHERE user_id=?", [user_id])
            userbotspammer.commit()
            await message.edit_text("User unmuted successfully.")
        else:
            await message.edit_text("User is not muted.")
    except Exception as e:
        print(f"Error while unmuting user: {e}")
        await message.edit_text("Error while unmuting user.")

@ubot.on_message(filters.user("self") & filters.command("setcmd", "."))
async def set_generic_link(client, message):
    try:
        command_parts = message.text.split(' ', 2)
        table_name = command_parts[1]
        link_value = command_parts[2]

        await save_link(link_value, table_name, userbotspammer)

        await message.edit_text(f"Command for {table_name} set successfully.")
    except (IndexError, ValueError):
        await message.edit_text("Right command: .setcmd [table_name] [link_value]")

@ubot.on_message(filters.user("self") & filters.regex(r'^\.[a-zA-Z0-9_]+$'))
async def direct_link_command(client, message):
    try:
        table_name = message.text[1:]

        link_value = await load_link(table_name, userbotspammer)
        if link_value:
            await message.edit_text(f"{link_value}")
        else:
            await message.edit_text(f"No command set for {table_name}. Use .setcmd to set a command.")
    except (IndexError, ValueError):
        await message.edit_text(f"Right command format: .{table_name}")

@ubot.on_message(filters.user("self") & filters.command("delcmd", "."))
async def delete_generic_link(client, message):
    try:
        command_parts = message.text.split(' ', 2)
        table_name = command_parts[1]

        await delete_link(table_name, userbotspammer)

        await message.edit_text(f"Command for {table_name} deleted successfully.")
    except (IndexError, ValueError):
        await message.edit_text("Right command: .delcmd [table_name]")

@ubot.on_message(filters.text)
async def delete_muted_messages(client, message):
    try:
        # Verifica se l'utente è muteato e se il mittente è valido
        if message.from_user and is_user_muted(message.from_user.id):
            # Elimina il messaggio
            await message.delete()
    except Exception as e:
        print(f"Error while deleting muted user's message: {e}")

idle()
