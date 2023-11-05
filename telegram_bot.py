from config import * #Token y df
import telebot 
from telebot import types

#Instanciamos bot de Telegram

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def send_long_message(chat_id, text):
    max_message_length = 4000  # Límite de caracteres de Telegram
    messages = [text[i:i + max_message_length] for i in range(0, len(text), max_message_length)]
    
    for message in messages:
        bot.send_message(chat_id, message)



#Responder al comando /start
@bot.message_handler(commands=["start"])
def cmd_start(message):
    """Inicializa el bot y realiza el scraping"""
    bot.reply_to(message,"Bienvenido al bot de noticias")



# Manejador para el comando /about
@bot.message_handler(commands=['about'])
def about(message):
    
    about_message = (
        "Este bot fue desarrollado por:\n"
        "- Di Marco, Nicolas\n"
        "- Escandell, Ariel\n"
        "- Raffaeli, Taiel\n\n"
        "La fuente de las noticias es xataka.com\n"
        "Fue desarrollado para la materia PNL de la TUIA."
    )

    # Envia el mensaje al usuario
    bot.reply_to(message, about_message)


@bot.message_handler(commands=["resumen"])
def cmd_resumen(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    
    # Define las opciones del teclado personalizado
    buttons = [
        types.KeyboardButton("1. Medicina"),
        types.KeyboardButton("2. IA"),
        types.KeyboardButton("3. Cine y Comics"),
        types.KeyboardButton("4. Ordenadores"),
    ]

    # Agrega las opciones al teclado
    markup.add(*buttons)

    # Envía un mensaje con el teclado personalizado
    bot.reply_to(message, "Selecciona una categoría de noticias:", reply_markup=markup)

# Manejador para manejar la selección de categoría
@bot.message_handler(func=lambda message: message.text in ["1. Medicina", "2. IA", "3. Cine y Comics", "4. Ordenadores"])
def handle_resumen_selection(message):
    chat_id = message.chat.id
    selected_option = int(message.text.split(".")[0])  # Extraer el número de la opción

    if selected_option in [1, 2, 3, 4]:
        # Acceder al valor de COD_categoria
        cod_categoria = selected_option - 1  # Restar 1 para que coincida con el índice del DataFrame

        # Filtrar el DataFrame de resúmenes por COD_categoria
        resumen_categoria = resumen[resumen['COD_Categoria'] == cod_categoria]

        if not resumen_categoria.empty:
            resumen_text = resumen_categoria.iloc[0]['Resumen']
            bot.reply_to(message, resumen_text)
        else:
            bot.reply_to(message, "No hay resúmenes disponibles para esta categoría.")
    else:
        bot.reply_to(message, "Opción no válida. Por favor, elige un número válido.")




# Responder al comando /medicina
# Manejador de comando para /medicina
@bot.message_handler(commands=["medicina"])
def cmd_medicina(message):
    # Filtrar noticias de Medicina del DataFrame
    noticias_medicina = df[df['COD_Categoria'] == 0]
    last_category = 0
    if not noticias_medicina.empty:
        titulos_medicina = noticias_medicina['Titulo'].tolist()
        # Crear un mensaje enumerado con los títulos
        response = "Noticias de Medicina disponibles:\n"
        for i, titulo in enumerate(titulos_medicina, start=1):
            response += f"{i}. {titulo}\n"

        # Guardar las noticias en el diccionario
        noticias_dict["medicina"][message.chat.id] = noticias_medicina

        # Enviar la respuesta al usuario
        bot.reply_to(message, response)
    else:
        response = "No hay noticias de Medicina disponibles."
        bot.reply_to(message, response)
    global active_handler
    active_handler = 'medicina'
    #bot.reply_to(message, "Manejador de Medicina activado.")


# Manejador para manejar la selección de noticias de Medicina
@bot.message_handler(func=lambda message: message.text.isdigit() and active_handler == 'medicina')
def handle_medicina_selection(message):
    chat_id = message.chat.id
    
    # Verificar si hay noticias de Medicina disponibles en el diccionario
    if chat_id in  noticias_dict["medicina"]:
        noticias_medicina =  noticias_dict["medicina"][chat_id]
        selected_news = int(message.text)

        if 1 <= selected_news <= len(noticias_medicina):
            # Obtener el contenido de la noticia seleccionada
            contenido = noticias_medicina.iloc[selected_news - 1]['Texto']
            send_long_message(chat_id, contenido)
        else:
            bot.send_message(chat_id, "Selección no válida. Por favor, elige un número válido.")
    else:
        bot.send_message(chat_id, "No hay noticias de Medicina disponibles.")


# Responder al comando /ia
@bot.message_handler(commands=["ia"])
def cmd_ia(message):
    # Filtrar noticias de IA del DataFrame
    noticias_ia = df[df['COD_Categoria'] == 1]
    last_category = 1
    if not noticias_ia.empty:
        titulos_ia = noticias_ia['Titulo'].tolist()
        # Crear un mensaje enumerado con los títulos
        response = "Noticias de IA disponibles:\n"
        for i, titulo in enumerate(titulos_ia, start=1):
            response += f"{i}. {titulo}\n"

        # Guardar las noticias en el diccionario
        noticias_dict["ia"][message.chat.id] = noticias_ia

        # Enviar la respuesta al usuario
        bot.reply_to(message, response)
    else:
        response = "No hay noticias de IA disponibles."
        bot.reply_to(message, response)
    global active_handler
    active_handler = 'ia'
    #bot.reply_to(message, "Manejador de IA activado.")

# Manejador para manejar la selección de noticias
@bot.message_handler(func=lambda message: message.text.isdigit()and active_handler == 'ia')
def handle_news_selection(message):
    chat_id = message.chat.id

    # Verificar si hay noticias disponibles en el diccionario
    if chat_id in noticias_dict["ia"]:
        noticias_ia = noticias_dict["ia"][chat_id]
        selected_news = int(message.text)

        if 1 <= selected_news <= len(noticias_ia):
            # Obtener el contenido de la noticia seleccionada
            contenido = noticias_ia.iloc[selected_news - 1]['Texto']
            send_long_message(chat_id, contenido)
        else:
            bot.send_message(chat_id, "Selección no válida. Por favor, elige un número válido.")
    else:
        bot.send_message(chat_id, "No hay noticias disponibles.")




# Manejador de comando para /cyc
@bot.message_handler(commands=["cyc"])
def cmd_cyc(message):
    # Filtrar noticias de Cine y Comics del DataFrame
    noticias_cyc = df[df['COD_Categoria'] == 2]
    last_category = 2
    if not noticias_cyc.empty:
        titulos_cyc = noticias_cyc['Titulo'].tolist()
        # Crear un mensaje enumerado con los títulos
        response = "Noticias de Cine y Comics disponibles:\n"
        for i, titulo in enumerate(titulos_cyc, start=1):
            response += f"{i}. {titulo}\n"

        # Guardar las noticias en el diccionario
        noticias_dict["cyc"][message.chat.id] = noticias_cyc

        # Enviar la respuesta al usuario
        bot.reply_to(message, response)
    else:
        response = "No hay noticias de Cine y Comics disponibles."
        bot.reply_to(message, response)
    global active_handler
    active_handler = 'cyc'

# Manejador para manejar la selección de noticias de Cine y Comics
@bot.message_handler(func=lambda message: message.text.isdigit() and active_handler == 'cyc')
def handle_cyc_selection(message):
    chat_id = message.chat.id

    # Verificar si hay noticias de Cine y Comics disponibles en el diccionario
    if chat_id in noticias_dict["cyc"]:
        noticias_cyc = noticias_dict["cyc"][chat_id]
        selected_news = int(message.text)

        if 1 <= selected_news <= len(noticias_cyc):
            # Obtener el contenido de la noticia seleccionada
            contenido = noticias_cyc.iloc[selected_news - 1]['Texto']
            send_long_message(chat_id, contenido)
        else:
            bot.send_message(chat_id, "Selección no válida. Por favor, elige un número válido.")
    else:
        bot.send_message(chat_id, "No hay noticias de Cine y Comics disponibles.")


# Responder al comando /pc
# Manejador de comando para /pc
@bot.message_handler(commands=["pc"])
def cmd_pc(message):
    # Filtrar noticias de Ordenadores del DataFrame
    noticias_pc = df[df['COD_Categoria'] == 3]
    last_category = 3
    if not noticias_pc.empty:
        titulos_pc = noticias_pc['Titulo'].tolist()
        # Crear un mensaje enumerado con los títulos
        response = "Noticias de Ordenadores disponibles:\n"
        for i, titulo in enumerate(titulos_pc, start=1):
            response += f"{i}. {titulo}\n"

        # Guardar las noticias en el diccionario
        noticias_dict["pc"][message.chat.id] = noticias_pc

        # Enviar la respuesta al usuario
        bot.reply_to(message, response)
    else:
        response = "No hay noticias de Ordenadores disponibles."
        bot.reply_to(message, response)
    global active_handler
    active_handler = 'pc'

# Manejador para manejar la selección de noticias de Ordenadores
@bot.message_handler(func=lambda message: message.text.isdigit()and active_handler == 'pc')
def handle_pc_selection(message):
    chat_id = message.chat.id

    # Verificar si hay noticias de Ordenadores disponibles en el diccionario
    if chat_id in noticias_dict["pc"]:
        noticias_pc = noticias_dict["pc"][chat_id]
        selected_news = int(message.text)

        if 1 <= selected_news <= len(noticias_pc):
            # Obtener el contenido de la noticia seleccionada
            contenido = noticias_pc.iloc[selected_news - 1]['Texto']
            send_long_message(chat_id, contenido)
        else:
            bot.send_message(chat_id, "Selección no válida. Por favor, elige un número válido.")
    else:
        bot.send_message(chat_id, "No hay noticias de Ordenadores disponibles.")


#Main###################
if __name__ == '__main__':
    print("iniciando el bot")
    bot.set_my_commands([
        telebot.types.BotCommand("/start","inicializa el bot"),
        telebot.types.BotCommand("/resumen","muestra las categorias de noticias"),
        telebot.types.BotCommand("/medicina","muestra las noticias de medicina"),
        telebot.types.BotCommand("/ia","muestra las noticias de IA"),
        telebot.types.BotCommand("/cyc","muestra las noticias de cine y comics"),
        telebot.types.BotCommand("/pc","muestra las noticias de ordenadores"),
        telebot.types.BotCommand("/about","datos sobre el bot"),
    ])
    noticias_dict = {
    "medicina": {},
    "ia": {},
    "cyc": {},
    "pc": {}
    }
    active_handler = None
    bot.add_message_handler(handle_resumen_selection)

    bot.infinity_polling()
    print("Fin")