import telebot
import config
import texts
import sqlite3

bot = telebot.TeleBot(config.bot_token)

con = sqlite3.connect('users.sqlite',check_same_thread=False)
cur = con.cursor()


#Hundles
try:
    @bot.message_handler(regexp="[/buy_]\d\d\d\d\d")
    def handle_message(message):
        type = message.text.split("_")[0]

        if(type == '/rate'):
            cur.execute('SELECT rate_bool FROM rate WHERE user_id = ' + str(message.chat.id))
            con.commit()

            data_rate_bool = cur.fetchone()

            id = message.text.split("_")[1]

            if(data_rate_bool == None):

                    markup_rate = telebot.types.InlineKeyboardMarkup(row_width=1)

                    b1 = telebot.types.InlineKeyboardButton(text="1", callback_data="1_"+str(id))
                    b2 = telebot.types.InlineKeyboardButton(text="2", callback_data="2_"+str(id))
                    b3 = telebot.types.InlineKeyboardButton(text="3", callback_data="3_"+str(id))
                    b4 = telebot.types.InlineKeyboardButton(text="4", callback_data="4_"+str(id))
                    b5 = telebot.types.InlineKeyboardButton(text="5", callback_data="5_"+str(id))

                    markup_rate.add(b1,b2,b3,b4,b5)

                    bot.send_message(message.chat.id, text='Поставте оценку магазину по шкале от 1 до 5. ', reply_markup=markup_rate)
            else:
                    bot.send_message(message.chat.id, text='Изините,  но вы ставили оценку этому магазину.')

        if (type == '/buy'):
            id = message.text.split("_")[1]
            print(id)
            cur.execute(' SELECT operator FROM markets WHERE id_market = '+ '"'+str(id)+'"')
            con.commit()
            data_operator = cur.fetchall()
            print(data_operator)
            bot.send_message(message.chat.id, texts.operator_out_text_prt1+ str(data_operator[0][0])+texts.operator_out_text_prt2)

        if (type == '/lament'):
            id = message.text.split("_")[1]
            cur.execute('INSERT INTO "lament" ("id_market","user_id","kind") VALUES (' + '"' + str(id) + '"' + ', "' + str(
                message.chat.id) + '"' + ', "' + "" + '")')
            con.commit()

            markup_lament = telebot.types.InlineKeyboardMarkup(row_width=1)

            b1 = telebot.types.InlineKeyboardButton(text="Мошенничество", callback_data="Мошенничество")
            b2 = telebot.types.InlineKeyboardButton(text="Продажа веществ запрещённых правилами",
                                                    callback_data="Продажа")
            b3 = telebot.types.InlineKeyboardButton(text="Дезинформация",
                                                    callback_data="Дезинформация в описании")
            b4 = telebot.types.InlineKeyboardButton(text="Некачественный продукт", callback_data="Некачественный")

            markup_lament.add(b1, b2, b3, b4)

            bot.send_message(message.chat.id, text='Выберете категорию вашей жалобы:', reply_markup=markup_lament)
except:
    print("ERROR")
    

@bot.message_handler(commands=['help'])
def handler_command_start(message):
    bot.send_message(message.chat.id, parse_mode="Markdown",text=texts.help_text )

@bot.message_handler(commands=['start'])
def handler_command_start(message):

    if(chack_user(message.chat.id)):
        delete_user(message.chat.id)
    else:
        pass

    markup_city = telebot.types.InlineKeyboardMarkup(row_width=2)

    b1  =  telebot.types.InlineKeyboardButton(text="Москва", callback_data="Москва")
    b2  =  telebot.types.InlineKeyboardButton(text='Санкт-Петербург', callback_data='Санкт-Петербург')
    b3  =  telebot.types.InlineKeyboardButton(text='Новосибирск', callback_data='Новосибирск')
    b4  =  telebot.types.InlineKeyboardButton(text='Екатеринбург', callback_data='Екатеринбург')
    b5  =  telebot.types.InlineKeyboardButton(text='Нижний Новгород', callback_data='Нижний Новгород')
    b7  =  telebot.types.InlineKeyboardButton(text='Казань', callback_data='Казань')
    b8  =  telebot.types.InlineKeyboardButton(text='Челябинск', callback_data='Челябинск')
    b9  =  telebot.types.InlineKeyboardButton(text='Омск', callback_data='Омск')
    b10 =  telebot.types.InlineKeyboardButton(text='Самара', callback_data='Самара')
    b11 =  telebot.types.InlineKeyboardButton(text='Ростов-на-Дону', callback_data='Ростов-на-Дону')
    b12 =  telebot.types.InlineKeyboardButton(text='Уфа', callback_data='Уфа')
    b13 =  telebot.types.InlineKeyboardButton(text='Красноярск', callback_data='Красноярск')
    b14 =  telebot.types.InlineKeyboardButton(text='Пермь', callback_data='Пермь')
    b15 =  telebot.types.InlineKeyboardButton(text='Воронеж', callback_data='Воронеж')

    markup_city.add(b1,b2,b3,b4,b5,b7,b8,b9,b10,b11,b12,b12,b13,b14,b15,b13)

    bot.send_message(message.chat.id,text=texts.strat_message,reply_markup=markup_city)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if(message.text == "Марихуана" or message.text == "Бошки" ):
        bot.send_message(message.chat.id, "http://telegra.ph/Marihuana-07-31")
    if (message.text == "ЛСД" or message.text == "LSD"):
        bot.send_message(message.chat.id, "http://telegra.ph/LSD-07-31")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if (call.data.find("1_") != -1):
        murk = call.data.split('_')[0]
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text="Оценка -  " + str(murk))
        id = call.data.split('_')[1]
        rate(call,id)
    if (call.data.find("2_") != -1):
        murk = call.data.split('_')[0]
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text="Оценка -  " + str(murk))
        id = call.data.split('_')[1]
        rate(call,id)
    if (call.data.find("3_") != -1):
        murk = call.data.split('_')[0]
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text="Оценка -  " + str(murk))
        id = call.data.split('_')[1]
        rate(call,id)
    if (call.data.find("4_") != -1):
        murk = call.data.split('_')[0]
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text="Оценка -  " + str(murk))
        id = call.data.split('_')[1]
        rate(call,id)
    if (call.data.find("5_") != -1):
        murk = call.data.split('_')[0]
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text="Оценка -  " + str(murk))
        id = call.data.split('_')[1]
        rate(call,id)


    if call.data == "Мошенничество":
        kind_of_lament(call)
    if call.data == "Продажа":
        kind_of_lament(call)
    if call.data == "Дезинформация":
        kind_of_lament(call)
    if call.data == "Некачественный":
        kind_of_lament(call)

    if call.data == "Москва":
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы выбрали город - "+call.data)
        setCity_in_DB(call,call.message.chat.id)
        getDrugName(call)
    if call.data == 'Санкт-Петербург':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы выбрали город - " + call.data)
        setCity_in_DB(call, call.message.chat.id)
        getDrugName(call)
    if call.data == 'Новосибирск':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы выбрали город - " + call.data)
        setCity_in_DB(call, call.message.chat.id)
        getDrugName(call)
    if call.data == 'Екатеринбург':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы выбрали город - " + call.data)
        setCity_in_DB(call, call.message.chat.id)
        getDrugName(call)
    if call.data == 'Нижний Новгород':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы выбрали город - " + call.data)
        setCity_in_DB(call, call.message.chat.id)
        getDrugName(call)
    if call.data == 'Казань':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы выбрали город - " + call.data)
        setCity_in_DB(call, call.message.chat.id)
        getDrugName(call)
    if call.data == 'Челябинск':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы выбрали город - " + call.data)
        setCity_in_DB(call, call.message.chat.id)
        getDrugName(call)
    if call.data == 'Омск':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы выбрали город - " + call.data)
        setCity_in_DB(call, call.message.chat.id)
        getDrugName(call)
    if call.data == 'Самара':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы выбрали город - " + call.data)
        setCity_in_DB(call, call.message.chat.id)
        getDrugName(call)
    if call.data == 'Ростов-на-Дону':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы выбрали город - " + call.data)
        setCity_in_DB(call, call.message.chat.id)
        getDrugName(call)
    if call.data == 'Уфа':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы выбрали город - " + call.data)
        setCity_in_DB(call, call.message.chat.id)
        getDrugName(call)
    if call.data == 'Красноярск':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы выбрали город - " + call.data)
        setCity_in_DB(call, call.message.chat.id)
        getDrugName(call)
    if call.data == 'Пермь':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы выбрали город - " + call.data)
        setCity_in_DB(call, call.message.chat.id)
        getDrugName(call)
    if call.data == 'Воронеж':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы выбрали город - " + call.data)
        setCity_in_DB(call, call.message.chat.id)
        getDrugName(call)
    if call.data == 'Волгоград':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы выбрали город - " + call.data)
        setCity_in_DB(call, call.message.chat.id)
        getDrugName(call)

    if call.data == 'Кокаин':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Вы выбрали наркотик - " + call.data)
        setDrug_in_DB(call, call.message.chat.id)
        out_markets(call, call.message.chat.id)
    if call.data == 'Крэк-кокаин':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text="Вы выбрали наркотик - " + call.data)
        setDrug_in_DB(call, call.message.chat.id)
        out_markets(call, call.message.chat.id)
    if call.data == 'ЛСД':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text="Вы выбрали наркотик - " + call.data)
        setDrug_in_DB(call, call.message.chat.id)
        out_markets(call, call.message.chat.id)
    if call.data == 'Экстази':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text="Вы выбрали наркотик - " + call.data)
        setDrug_in_DB(call, call.message.chat.id)
        out_markets(call, call.message.chat.id)
    if call.data == 'Марихуана':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text="Вы выбрали наркотик - " + call.data)
        setDrug_in_DB(call, call.message.chat.id)
        out_markets(call, call.message.chat.id)
    if call.data == 'Амфетамин':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text="Вы выбрали наркотик - " + call.data)
        setDrug_in_DB(call, call.message.chat.id)
        out_markets(call, call.message.chat.id)
    if call.data == 'Кетамин':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text="Вы выбрали наркотик - " + call.data)
        setDrug_in_DB(call, call.message.chat.id)
        out_markets(call, call.message.chat.id)
    if call.data == 'МДМА':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text="Вы выбрали наркотик - " + call.data)
        setDrug_in_DB(call, call.message.chat.id)
        out_markets(call, call.message.chat.id)
    if call.data == 'ДМТ':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text="Вы выбрали наркотик - " + call.data)
        setDrug_in_DB(call, call.message.chat.id)
        out_markets(call, call.message.chat.id)
    if call.data == 'Гашиш':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                  text="Вы выбрали наркотик - " + call.data)
        setDrug_in_DB(call, call.message.chat.id)
        out_markets(call, call.message.chat.id)

    if call.data == 'next':
        cur.execute('UPDATE users_list SET pos = pos + 1 WHERE user_id = '+str(call.message.chat.id))
        con.commit()
        out_markets(call, call.message.chat.id)

    if call.data == 'back':
        cur.execute('UPDATE users_list SET pos = pos - 1 WHERE user_id = '+str(call.message.chat.id))
        con.commit()
        out_markets(call, call.message.chat.id)

#Function

def setCity_in_DB(call,user_id):
    try:
        cur.execute('INSERT INTO "main"."users_list" ("user_id","city","drug_name") VALUES (' + '"' +str(user_id)+ '"'+',"'+str(call.data)+'"'+',"") ')
        con.commit()
    except:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="HTML",
                              text="```У нас технические проблемы. Мы уже работаем над их исправление. Просим прощения.```")

def setDrug_in_DB(call,user_id):
    try:
        cur.execute('UPDATE "main"."users_list" SET "drug_name" = '+'"'+str(call.data)+'"'+' WHERE  "user_id" = '+str(user_id))
        con.commit()
    except:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="HTML",
                              text="```У нас технические проблемы. Мы уже работаем над их исправление. Просим прощения.```")

def getDrugName(call):

    markup_drugs = telebot.types.InlineKeyboardMarkup()

    b1 = telebot.types.InlineKeyboardButton(text='Кокаин', callback_data= 'Кокаин')
    b2 = telebot.types.InlineKeyboardButton(text='Крэк-кокаин',callback_data=  'Крэк-кокаин')
    b3 = telebot.types.InlineKeyboardButton(text='ЛСД', callback_data= 'ЛСД')
    b4 = telebot.types.InlineKeyboardButton(text='Экстази', callback_data= 'Экстази')
    b5 = telebot.types.InlineKeyboardButton(text='Марихуана',callback_data=  'Марихуана')
    b6 = telebot.types.InlineKeyboardButton(text='Амфетамин',callback_data=  'Амфетамин')
    b7 = telebot.types.InlineKeyboardButton(text='Кетамин',callback_data=  'Кетамин')
    b8 = telebot.types.InlineKeyboardButton(text='МДМА',callback_data=  'МДМА')
    b9 = telebot.types.InlineKeyboardButton(text='ДМТ',callback_data=  'ДМТ')
    b10 = telebot.types.InlineKeyboardButton(text='Гашиш', callback_data= 'Гашиш')

    markup_drugs.add(b1, b2, b3, b4, b5,b6, b7, b8, b9, b10)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texts.enter_name_drug,reply_markup=markup_drugs)

def out_markets(call, user_id):
    ## Get market list ##
    try:
        cur.execute('SELECT city FROM users_list WHERE user_id = '+str(user_id))
        con.commit()
        data_city = cur.fetchone()

        cur.execute('SELECT drug_name FROM users_list WHERE user_id = '+str(user_id) )
        con.commit()
        data_drug_name = cur.fetchone()

        cur.execute(' SELECT * FROM markets WHERE instr(citys, "'+str(data_city[0])+'") > 0 AND instr(drugs, "'+str(data_drug_name[0])+'") > 0'  )
        con.commit()

        data_market = cur.fetchall()
    except:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="HTML",
                              text="```У нас технические проблемы. Мы уже работаем над их исправление. Просим прощения.```")
    ###############################

    ## Output date ##

    markup_next = telebot.types.InlineKeyboardMarkup()

    b_next = telebot.types.InlineKeyboardButton(text="--->", callback_data='next')
    b_back = telebot.types.InlineKeyboardButton(text="<---",callback_data='back')

    cur.execute('SELECT pos FROM users_list WHERE user_id = ' + str(call.message.chat.id))
    con.commit()
    data_pos = cur.fetchone()

    print(data_pos[0])

    if (data_pos[0] == 0):
        if (len(data_market) - 1 == 0):
            None
        else:
            markup_next.add(b_next)
    if (data_pos[0] != 0):
        if (len(data_market) - 1 <= data_pos[0]):
            markup_next.add(b_back)
            stop(len(data_market),user_id)
        else:
            markup_next.add(b_back,b_next)

    try:

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="HTML", text="<b>"+data_market[data_pos[0]][1]+"</b>"+"\n Описание: \n"
                                                                                                                            "<i>"+str(data_market[data_pos[0]][2])+"</i>"+"\n"                                                                                                     "Рейтинг: \n"+ ""
                                                                                                                            ""+str( data_market[data_pos[0]][3] / data_market[data_pos[0]][4])+ "\n"
                                                                                                                            "Купить: /buy_"+str(data_market[data_pos[0]][0]) + "\n"
                                                                                                                            "Подать жалобу /lament_"+str(data_market[data_pos[0]][0]) + "\n"
                                                                                                                            "Оценить: /rate_"+str( data_market [data_pos[0]] [0] ) , reply_markup=markup_next)
    except IndexError:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown",text="Нам очень жаль, но в этом городе _пока_ нету ни одного магазина.")

def stop(len_data_market, user_id):
    cur.execute('UPDATE users_list SET pos = ' + str(len_data_market-1) + ' WHERE user_id = ' + str(user_id))
    con.commit()

def kind_of_lament(call):
    cur.execute('UPDATE lament SET kind = ' + '"'+str(call.data)+'"' + ' WHERE user_id = ' + str(call.message.chat.id))
    con.commit()

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="HTML",text="Спасибо, вы нам очень помогли. Наши модераторы скоро разберутся. ")

def rate(call,id):
    murk = call.data.split("_")[0]
    cur.execute('UPDATE markets SET murk_sum = murk_sum + '+str(murk)+ ', murk_dev = murk_dev + 1 WHERE id_market = '+str(id))
    con.commit()

    cur.execute('INSERT INTO "rate" ("user_id","rate_bool") VALUES ("'+str(call.message.chat.id)+'" , "TRUE")')
    con.commit()

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="HTML",text="Спасибо за вашу оценку")

def chack_user(user_id):
    try:
        cur.execute('SELECT user_id FROM users_list WHERE user_id = ' + str(user_id))
        con.commit()
        data_user = cur.fetchone()
        if(data_user == None ):
            return False
        else:
            return True
    except:
        pass

def delete_user(user_id):
    cur.execute('DELETE FROM users_list WHERE user_id = '+ str(user_id))
    con.commit()


bot.polling(none_stop=True)
