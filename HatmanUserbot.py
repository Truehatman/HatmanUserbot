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
import os
import json

class Database:

try:
    userbotspammer = sqlite3.connect("userbot.db")
    userbotspammer.cursor().execute("CREATE TABLE IF NOT EXISTS gruppi (chatid INT)")
except:
    pass

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
        await message.edit(" Errore in .addgroup!")

@ubot.on_message(filters.user("self") & filters.command("remgroup", "."))
async def rimuovigruppo(_, message):
    try:
        count = userbotspammer.cursor().execute("SELECT COUNT(chatid) FROM gruppi").fetchone()[0]
        if count == 0:
            await message.edit("There are no groups !")
        else:
            group = await ubot.get_chat(message.text.split(" ")[1])
            userbotspammer.cursor().execute("DELETE FROM gruppi WHERE chatid = ?", [group.id])
            userbotspammer.commit()
            await message.edit(f" Group {group.title} Ã¨removed!")
    except:
        group = await ubot.get_chat(message.text.split(" ")[1])
        await message.edit(f" Error in .remgroup {group.title}")

@ubot.on_message(filters.user("self") & filters.command("grouplist", "."))
async def listagruppi(_, message):
    count = userbotspammer.cursor().execute("SELECT COUNT(chatid) FROM gruppi").fetchone()[0]
    if count == 0:
        await message.edit(" There are no group!")
    else:
        gruppimsg = ""
        for gruppi, in userbotspammer.cursor().execute("SELECT chatid FROM gruppi").fetchall():
            gruppimsg += f"â¥ {(await ubot.get_chat(gruppi)).title} | <code>{(await ubot.get_chat(gruppi)).id}</code>\n\n"
        await message.edit(f"<b> Â» Group List:</b>\n\n{gruppimsg}")
        

timespam = None
messaggio = ""

@ubot.on_message(filters.user("self") & filters.command("time", "."))
async def tempo(_, message):
    global timespam
    minuti = message.text.split(" ")[1]
    minuti = minuti * 60
    if len(message.text.split(" ")) > 1:
        try:
            int(minuti)
            if int(minuti) >= 300:
                timespam = int(minuti)
                await message.edit(f"Time set on {timespam} minutes")
                pass
            else:
                await message.edit("Min is 5 minutes")
                return 
        except:
            return await message.edit("Time has to be more than 5 minutes ")

@ubot.on_message(filters.user("self") & filters.command("setmex", "."))
async def setmex(_, message):
    global messaggio
    try:
        messaggio = message.text.replace(f".setmex", "")
        await message.edit(f" Message set\n\n <code>{messaggio}</code>")
    except:
        await message.edit("Format wrong, .setmex Messaggio")

@ubot.on_message(filters.user("self") & filters.command("spam", "."))
async def spamavviato(_, message):
    global spamcheck
    count = userbotspammer.cursor().execute("SELECT COUNT(chatid) FROM gruppi").fetchone()[0]
    if count == 0:
        await message.edit(" There are no Groups!")
    else:
        if not spamcheck:
            spamcheck = True
            await message.edit(f" Spam started. Im spamming in {count} groups")
            while spamcheck:
                for gruppi, in userbotspammer.cursor().execute("SELECT chatid FROM gruppi").fetchall():
                    try:
                        await ubot.send_message(gruppi, messaggio)
                        await asyncio.sleep(0.5)
                    except:
                         await asyncio.sleep(0.5)
                await asyncio.sleep(int(timespam))
        else:
            await message.edit("Format wrong, .spam")

@ubot.on_message(filters.user("self") & filters.command("stop", "."))
async def stopspam(_, message):
    global spamcheck
    if spamcheck:
        spamcheck = False
        await message.edit(" Spam end")
    else:
        await message.edit(" Spam not started")



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
        # Verifica se l'utente ÃÂ¨ muteato e se il mittente ÃÂ¨ valido
        if message.from_user and message.from_user.id in muted_users:
            # Elimina il messaggio
            await message.delete()
    except Exception as e:
        print(f"Error while deleting muted user's message: {e}")

idle()
