#HatmanUserbot
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
import subprocess
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

async def delete_link(table_name, user):
    if table_name in commands_dict:
        del commands_dict[table_name]
    else:
        raise ValueError("Table not found.")

spamcheck = False

muted_users = {}
scheduled_tasks = {}


@ubot.on_message(filters.user("self") & filters.command("addgroup", prefixes="."))
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

@ubot.on_message(filters.user("self") & filters.command("remgroup", prefixes="."))
async def remove_group(_, message):
    try:
        # Check if the message has an argument
        if len(message.command) > 1:
            input_value = message.command[1]  # Use the second element of the command list
        else:
            await message.edit("You must specify the name or ID of the group to remove.")
            return

        try:
            # Try to get the group using the username or ID
            chat_info = await ubot.get_chat(input_value)
            group_id = chat_info.id
        except Exception as e:
            await message.edit(f"Error: {str(e)}")
            return

        print(f"Attempting to remove group with ID: {group_id} from the list.")

        # Check if the group is in the list before removal
        if is_group_in_list(group_id):
            try:
                # Remove everything related to the group from the 'gruppi' table in the database
                userbotspammer.cursor().execute("DELETE FROM gruppi WHERE chatid = ?", [group_id])
                userbotspammer.commit()
                await message.edit(f"Group with ID {group_id} removed from the list.")
            except Exception as remove_exception:
                print(f"Error removing the group (ID: {group_id}) from the list: {str(remove_exception)}")
                await message.edit(f"Error removing the group from the list.")
        else:
            await message.edit(f"Group with ID {group_id} not found in the list.")
    except Exception as e:
        print(e)
        await message.edit(f"Error in .remgroup: {str(e)}")

def is_group_in_list(group_id):
    try:
        result = userbotspammer.cursor().execute("SELECT COUNT(chatid) FROM gruppi WHERE chatid = ?", [group_id]).fetchone()[0]
        return result > 0
    except Exception as e:
        print(f"Error in is_group_in_list: {str(e)}")
        return False

# Funzione per avviare la lista dei gruppi
@ubot.on_message(filters.user("self") & filters.command("grouplist", prefixes="."))
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
@ubot.on_message(filters.user("self") & filters.command("resetgrouplist", prefixes="."))
async def reset_grouplist(_, message):
    try:
        # Elimina tutti i dati dalla tabella 'gruppi'
        userbotspammer.cursor().execute("DELETE FROM gruppi")
        userbotspammer.commit()

        await message.edit("Group list reset successfully!")
    except Exception as e:
        print(f"Error in .resetgrouplist: {e}")
        await message.edit("Error resetting group list!")

@ubot.on_message(filters.user("self") & filters.command("time", prefixes="."))
async def tempo(_, message):
    global timespam
    if len(message.text.split(" ")) > 1:
        minuti = message.text.split(" ")[1]
        try:
            minuti = int(minuti)
            secondi = minuti * 60
            if secondi >= 300:
                timespam = minuti
                await message.edit(f"Time set on {timespam} minutes")
                timespam = secondi
            else:
                await message.edit("Min is 5 minutes")
        except ValueError:
            await message.edit("Put a valid integer for the time in minutes")
    else:
        await message.edit("Please specify the time in minutes.")

@ubot.on_message(filters.user("self") & filters.command("setmex", prefixes="."))
async def setmex(_, message):
    global messaggio
    try:
        messaggio = message.text.replace(f".setmex", "")
        await message.edit(f" Message set <code>{messaggio}</code>")
    except:
        await message.edit("Wrong format, .setmex Messaggio")

@ubot.on_message(filters.user("self") & filters.command("spam", prefixes="."))
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
                        await asyncio.sleep(0.7)
                    except:
                         await asyncio.sleep(0.7)
                await asyncio.sleep(int(timespam))
        else:
            await message.edit("wrong format, .spam")




@ubot.on_message(filters.user("self") & filters.command("stop", prefixes="."))
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


@ubot.on_message(filters.user("your_user_id") & filters.command("update", "."))
async def update_code(_, message):
    try:
        # Sostituisci 'YOUR_GITHUB_TOKEN' con il tuo token personale di GitHub
        github_token = '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'
        repo_url = "https://github.com/hatmanexchange/HatmanUserbot.git"

        # Setta la variabile d'ambiente per utilizzare il token durante l'operazione di pull
        os.environ['GITHUB_TOKEN'] = github_token

        # Scarica il codice più recente
        subprocess.run(["git", "pull", repo_url])

        # Rimuovi la variabile d'ambiente dopo l'operazione di pull
        del os.environ['GITHUB_TOKEN']

        # Riavvia il bot o esegui altre operazioni necessarie
        await message.edit("Code updated successfully. Restarting the bot...")
        # Puoi aggiungere qui il codice per il riavvio del bot, se necessario

    except Exception as e:
        print(e)
        await message.edit(f"Error updating the code: {str(e)}")

@ubot.on_message(filters.user("self") & filters.command("setcmd", prefixes="."))
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

@ubot.on_message(filters.user("self") & filters.command("delcmd", prefixes="."))
async def delete_generic_link(client, message):
    try:
        command_parts = message.text.split(' ', 2)
        table_name = command_parts[1]

        await delete_link(table_name, userbotspammer)

        await message.edit_text(f"Command for {table_name} deleted successfully.")
    except (IndexError, ValueError):
        await message.edit_text("Right command: .delcmd [table_name]")

idle()


