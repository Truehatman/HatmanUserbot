from pyrogram import Client, filters
import schedule
import time

# Credenziali API comuni
api_id = '25047326'
api_hash = '9673ea812441c77e912979cd0f8a2572'

# Lista delle sessioni con rispettivi numeri di telefono
sessions = [
    {'phone_number': '+39 351 555 7518'},
    # Aggiungi più sessioni secondo necessità
]

# Variabile per memorizzare il link PayPal generico
paypal_link = None

#Creazione di una lista gruppi
gruppi = []

# Creazione di una lista di clienti Pyrogram
clients = [Client(f"{session['phone_number']}", api_id, api_hash) for session in sessions]

@Client.on_message(filters.command(["help"]))
async def help_command(client, message):
    await message.reply_text("https://telegra.ph/HatmanUserbot-01-14")

@Client.on_message(filters.command("creator"))
async def creator_command(client, message):
    await message.reply_text("I am developed by @hatmanexchanger!")

@Client.on_message(filters.command("percentage"))
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

@Client.on_message(filters.command("addgroup"))
async def add_group_command(client, message):
    try:
        # Estrai il testo del messaggio dopo il comando
        command_text = message.text.split(' ', 1)[1]
        gruppo_id = int(command_text)

        # Aggiungi il gruppo alla lista con un messaggio di default solo se non è già presente
        if gruppo_id not in gruppi:
            gruppi[gruppo_id] = {'intervallo': 5, 'messaggio': ""}
            await message.reply_text(f"Group {gruppo_id} added to the list.")
        else:
            await message.reply_text(f"Group is already in the list {gruppo_id}.")
    except (ValueError, IndexError):
        await message.reply_text("Right command: .addgroup [id_group]")

@Client.on_message(filters.command("spam"))
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
        schedule.every(intervallo).minutes.do(send_spam, client, gruppo_id)

        await message.reply_text(f"Spam on! i will send the message every {intervallo} minutes.")
    except (ValueError, IndexError):
        await message.reply_text("Right command: .spam [minutes] [message]")

def send_spam(client, gruppo_id):
    try:
        # Invia il messaggio di spam al gruppo specifico
        client.send_message(gruppo_id, gruppi[gruppo_id]['messaggio'])
    except Exception as e:
        print(f"error while the sending of the message in group {gruppo_id}: {e}")

@Client.on_message(filters.command("listgroups"))
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

@Client.on_message(filters.command(["cloud"], prefixes=".") & filters.reply)
async def save_to_cloud(client, message):
    try:
        # Estrai il messaggio a cui si sta rispondendo
        replied_message = message.reply_to_message

        # Salva il messaggio nei messaggi salvati
        await client.save_file(replied_message, file_name="")

        await message.reply_text("Message correctly saved")
    except Exception as e:
        print(f"Error while the saving of the message: {e}")

@Client.on_message(filters.command(["paypal"], prefixes="."))
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
        await message.reply_text("Right command: /paypal [link_paypal]")

@Client.on_message(filters.command(["pp"], prefixes="."))
async def show_paypal_link(client, message):
    if paypal_link:
        await message.reply_text(f"Link PayPal:\n{paypal_link}")
    else:
        await message.reply_text("No link PayPal set. Use /paypal perto set a link.")
        
@Client.on_message(filters.command(["block"], prefixes=".") & filters.reply)
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

@Client.on_message(filters.command(["unblock"], prefixes=".") & filters.reply)
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

@Client.on_message(filters.command(["mute"], prefixes=".") & filters.reply)
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
        
@Client.on_message(filters.command(["unmute"], prefixes=".") & filters.reply)
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

async def main():
    # Avvio di tutti i clienti
    for client in clients:
        await client.start()
        print(f"Client connected for {client.get_me().username}")

    # Attivazione dei comandi e inizio dell'ascolto
    for client in clients:
        await client.send_message('me', ".help")  # Invia il comando di help per mostrare i comandi
        await client.send_message('me', ".creator")  # Invia il comando /creator per mostrare il creatore
        await client.send_message('me', ".percentage 50 20")  # Esempio di utilizzo del comando /percentage
        await client.send_message('me', ".addgroup 123456")  # Esempio di aggiunta di un gruppo alla lista
        await client.send_message('me', ".spam 10 Messaggio di spam personalizzato")  # Esempio di attivazione dello spam con parametri personalizzati
        await client.send_message('me', ".listgroups")  # Esempio di comando per mostrare l'elenco dei gruppi

        await client.send_message('me', "/paypal https://paypal.me/il_tuo_link")  # Esempio di impostazione del link PayPal
        await client.send_message('me', "/pp")  # Esempio di comando per mostrare il link PayPal

 # Esegui il loop di scheduling in background
    while True:
        schedule.run_pending()
        time.sleep(1)

    await Client.run(clients)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())