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

ubot = Client("killersession", api_id=25047326, api_hash="9673ea812441c77e912979cd0f8a2572", lang_code="it")
ubot.start()

IDSSS, usernamesss = (ubot.get_me()).id, (ubot.get_me()).username
statusse = False
ignore = []

# Addword
class Database:
    def __init__(self, file_name: str):
        self.database = file_name
        if not os.path.exists(file_name):
            with open(file_name, "w") as f:
                json.dump({"gruppi": {}}, f)

    async def save(self, update: dict):
        with open(self.database, "w") as f:
            json.dump(update, f)

    async def add_group(self, chat_id: int, intervallo: int, messaggio: str):
        update = json.load(open(self.database))
        chat_id_str = str(chat_id)
        update["gruppi"][chat_id_str] = {"intervallo": intervallo, "messaggio": messaggio}
        await self.save(update)
        return update["gruppi"][chat_id_str]

    async def del_group(self, chat_id: int):
        try:
            chat_id_str = str(chat_id)
            update = json.load(open(self.database))
            
            if chat_id_str in update["gruppi"]:
                del update["gruppi"][chat_id_str]
                await self.save(update)
                return True, chat_id_str
            else:
                return False, chat_id_str
        except Exception as e:
            print(f"Error during del_group: {e}")
            return False, None

    async def get_groups(self):
        update = json.load(open(self.database))
        return update.get("gruppi", {})
        
    async def load_paypal_link(self):
        update = json.load(open(self.database))
        return update.get("paypal_link")

    async def save_paypal_link(self, link):
        update = json.load(open(self.database))
        update["paypal_link"] = link
        await self.save(update)

    async def load_litecoin_link(self):
        update = json.load(open(self.database))
        return update.get("litecoin_link")

    async def save_litecoin_link(self, link):
        update = json.load(open(self.database))
        update["litecoin_link"] = link
        await self.save(update)

    async def load_bitcoin_link(self):
        update = json.load(open(self.database))
        return update.get("bitcoin_link")

    async def save_bitcoin_link(self, link):
        update = json.load(open(self.database))
        update["bitcoin_link"] = link
        await self.save(update)
        
    async def load_ethereum_link(self):
        update = json.load(open(self.database))
        return update.get("ethereum_link")

    async def save_ethereum_link(self, link):
        update = json.load(open(self.database))
        update["ethereum_link"] = link
        await self.save(update)


word = Database("word.json")

paypal_link = None
litecoin_link = None
bitcoin_link = None
ethereum_link = None

gruppi = []
muted_users = {}
scheduled_tasks = {}

async def send_spam(client: Client, chat_id: int, intervallo: int, messaggio: str):
    try:
        while True:
            print(f"Sending spam message to group {chat_id}")
            await client.send_message(chat_id, text=messaggio)
            print(f"Spam message sent to group {chat_id}")
            await asyncio.sleep(intervallo * 60)
    except asyncio.CancelledError:
        print(f"Spam task for group {chat_id} cancelled.")
    except Exception as e:
        print(f"Error while sending spam in group {group_id}: {e}")

@ubot.on_message(filters.user("self") & filters.command("spam", "."))
async def spam_command(client: Client, message: Message):
    try:
        args = message.text.split(maxsplit=2)
        
        if len(args) < 3:
            await message.edit_text("Usage: `.spam <minutes> <messaggio>`")
            return

        intervallo = int(args[1])
        messaggio = args[2]

        # Get the list of groups from the database
        groups = await word.get_groups()
        gruppi = list(groups.keys())

        for chat_id in gruppi:
            try:
                print(f"Trying to send spam in group {chat_id}")
                
                # Set basic permissions
                chat = await client.get_chat(chat_id)
                await client.restrict_chat_member(chat_id, user_id=client.me.id, permissions={
                    "can_send_messages": True,
                    "can_send_media_messages": True,
                    "can_send_polls": True,
                    "can_send_other_messages": True,
                    "can_add_web_page_previews": True,
                    "can_invite_users": True,
                })

                print(f"Basic permissions set for group {chat_id}")

                task = asyncio.create_task(send_spam(client, chat_id, intervallo, messaggio))
                scheduled_tasks[chat_id] = task
                print(f"Spam task created for group {chat_id}")

            except Exception as e:
                print(f"Error in group {chat_id}: {e}")

        await message.edit_text(f"Spam started successfully in all groups.")
    except Exception as e:
        print(f"Error while starting spam: {e}")
        await message.edit_text("Error while starting spam.")



# Comando per fermare lo spam
@ubot.on_message(filters.user("self") & filters.command("stopspam", prefixes="."))
async def stop_spam_command(client, message):
    try:
        # Cancella i task programmati per ogni gruppo
        for group_id, task in scheduled_tasks.items():
            task.cancel()

        await message.edit_text("Spam stopped successfully.")
    except Exception as e:
        print(f"Error while stopping spam: {e}")
        await message.edit_text("Error while stopping spam.")

        
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
            await message.edit_text(f"Group {gruppo_id} added to the list ")
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
        success, removed_group_id = await word.del_group(chat_id)
        if success:
            await message.edit_text(f"Group {removed_group_id} successfully removed from the list and database.")
        else:
            await message.edit_text(f"Group {removed_group_id} not found in the list.")

    except (ValueError, IndexError):
        await message.edit_text("Right command: .delgroup [id_group] or [username]")

@ubot.on_message(filters.user("self") & filters.command("ppset", "."))
async def set_paypal_link(client, message):
    global paypal_link
    try:
        # Estrai il testo del messaggio dopo il comando
        command_text = message.text.split(' ', 1)[1]
        link_paypal = command_text

        # Imposta il link PayPal generico
        paypal_link = link_paypal

        # Salva il link PayPal nel database
        await word.save_paypal_link(link_paypal)

        await message.edit_text("Link PayPal set successfully.")
    except (IndexError, ValueError):
        await message.edit_text("Right command: .ppset [link_paypal]")

@ubot.on_message(filters.user("self") & filters.command("pp", "."))
async def show_paypal_link(client, message):
    # Usa Database.paypal_link per ottenere il link PayPal
    paypal_link = await word.load_paypal_link()
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

        await word.save_litecoin_link(link_litecoin)

        await message.edit_text("Ltc address set successfully.")
    except (IndexError, ValueError):
        await message.edit_text("Right command: .ltcset [Address]")

@ubot.on_message(filters.user("self") & filters.command("ltc", "."))
async def show_litecoin_link(client, message):
    litecoin_link = await word.load_litecoin_link()
    if litecoin_link:
        await message.edit_text(f"{litecoin_link}")
    else:
        await message.edit_text("No ltc address  set. Use .ltcset to set a link.")

@ubot.on_message(filters.user("self") & filters.command("btcset", "."))
async def set_bitcoin_link(client, message):
    global bitcoin_link
    try:
        # Estrai il testo del messaggio dopo il comando
        command_text = message.text.split(' ', 1)[1]
        link_bitcoin = command_text

        # Imposta il link Litecoin generico
        bitcoin_link = link_bitcoin

        await word.save_bitcoin_link(link_bitcoin)

        await message.edit_text("Btc address set successfully.")
    except (IndexError, ValueError):
        await message.edit_text("Right command: .btcset [Address]")

@ubot.on_message(filters.user("self") & filters.command("btc", "."))
async def show_bitcoin_link(client, message):
    bitcoin_link = await word.load_bitcoin_link()
    if bitcoin_link:
        await message.edit_text(f"{bitcoin_link}")
    else:
        await message.edit_text("No btc address  set. Use .btcset to set a link.")

@ubot.on_message(filters.user("self") & filters.command("ethset", "."))
async def set_eth_link(client, message):
    global ethereum_link
    try:
        # Estrai il testo del messaggio dopo il comando
        command_text = message.text.split(' ', 1)[1]
        link_ethereum = command_text

        # Imposta il link Litecoin generico
        ethereum_link = link_ethereum

        await word.save_ethereum_link(link_ethereum)

        await message.edit_text("Eth address set successfully.")
    except (IndexError, ValueError):
        await message.edit_text("Right command: .ethset [Address]")

@ubot.on_message(filters.user("self") & filters.command("eth", "."))
async def show_ethereum_link(client, message):
    ethereum_link = await word.load_ethereum_link()
    if ethereum_link:
        await message.edit_text(f"{ethereum_link}")
    else:
        await message.edit_text("No eth address  set. Use .ethset to set a link.")
       
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
        # Verifica se l'utente Ã¨ muteato e se il mittente Ã¨ valido
        if message.from_user and message.from_user.id in muted_users:
            # Elimina il messaggio
            await message.delete()
    except Exception as e:
        print(f"Error while deleting muted user's message: {e}")


idle()
