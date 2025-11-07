import telebot
from telebot import types

bot = telebot.TeleBot()
import sqlite3 as sq

with sq.connect('database.db', check_same_thread=False) as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS products (
        pr_type INTEGER DEFAULT 0,
        pr_name TEXT DEFAULT ERROR,
        pr_price INTEGER DEFAULT 0,
        in_stock INTEGER DEFAULT 0
        )""")

    # ТЕРМИНАЛЬНЫЕ ПЕРЕМЕННЫЕ
    adminnames = []
    operator_id = 
    terminal = types.InlineKeyboardMarkup()
    terminal_button = types.InlineKeyboardButton('Терминал администратора', callback_data='cb_admin_terminal')
    terminal.add(terminal_button)
    open_terminal = types.InlineKeyboardMarkup(row_width=1)
    add_product_button = types.InlineKeyboardButton('Добавить товар', callback_data='cb_admin_add')
    remove_product_button = types.InlineKeyboardButton('Удалить товар', callback_data='cb_admin_remove')
    open_terminal.add(add_product_button, remove_product_button)
    # ПЕРЕМЕННЫЕ СТАРТА
    start_menu = types.InlineKeyboardMarkup(row_width=2)
    info = types.InlineKeyboardButton('ℹ️ Информация', callback_data="cb_info")
    shop = types.InlineKeyboardButton('🛒 Наши товары', callback_data="cb_shop")
    order = types.InlineKeyboardButton('💵 На заказ', callback_data="cb_order")
    write_to_admin = types.InlineKeyboardButton('💬 Чат с админом', callback_data="cb_write_to_admin")
    start_menu.add(shop, order, info, write_to_admin)
    start_call = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start = types.KeyboardButton('/start')
    start_call.add(start)
    # ПЕРМЕННЫЕ ВЫБОРА ТИПА ПРОДУКТА
    product_type_menu_buttons = types.InlineKeyboardMarkup(row_width=2)
    pod_button = types.InlineKeyboardButton('Поды', callback_data="cb_pod_button")
    jija_button = types.InlineKeyboardButton("Жидкости", callback_data="cb_jija_button")
    odnorazki_button = types.InlineKeyboardButton("Одноразки", callback_data="cb_odnorazki_button")
    other_product_type_button = types.InlineKeyboardButton("Расходники", callback_data="cb_other_product_type_button")
    product_type_menu_buttons.add(pod_button, jija_button, odnorazki_button, other_product_type_button)


    # ПЕРЕМЕННЫЕ отмены

    def is_number(str):
        try:
            int(str)
            return True
        except ValueError:
            return False

            # СТАРТ


    @bot.message_handler(commands=['start'])
    def start(message):
        #bot.send_photo(message.chat.id, "", reply_markup=start_call)
        startmsg = f'Привет, {message.from_user.first_name}. \nДобро пожаловать в ******************\nВыбери одну из кнопок ниже.\nИспользуй /start для того, чтобы вызвать это окно.'
        bot.send_message(message.chat.id, startmsg, reply_markup=start_menu)

        if message.from_user.username in adminnames:
            bot.send_message(message.chat.id, 'Возможности админа:', reply_markup=terminal)

            # ПРОВЕРКА НА ДАННЫЕ С КОЛЛБЕКА


    @bot.callback_query_handler(func=lambda message: True)
    def ans(message):
        if message.data == "cb_info":
            info_menu(message)
        elif message.data == "cb_shop":
            shop_menu(message)
        elif message.data == "cb_order":
            bot.send_message(message.message.chat.id,
                             '🤖❌ К сожалению доставка на заказ не работает на данный момент, приносим наши извинения.')
        elif message.data == "cb_write_to_admin":
            bot.send_message(message.message.chat.id,
                             '🚨 Самый актуальный список админов на данный момент  👉 ************* 👈 🚨')
        elif message.data == 'cb_admin_terminal':
            msg = bot.send_message(message.message.chat.id, 'Введите ключ безопасности:')
            bot.register_next_step_handler(msg, terminal_menu)
        elif message.data == 'cb_pod_button':
            show_shop(message, 1)
        elif message.data == 'cb_jija_button':
            show_shop(message, 2)
        elif message.data == 'cb_odnorazki_button':
            show_shop(message, 3)
        elif message.data == 'cb_other_product_type_button':
            show_shop(message, 4)
        elif message.data == 'cb_admin_add':
            add_product_type(message)
        elif message.data == 'cb_admin_remove':
            delete_product_name(message)
        elif len(message.data.split()) == 3:
            print(message.data.split()[0])
            print('111')
            buydata = message.data.split()
            if message.data.split()[0] == 'cb_buy':
                print('cb_buy')
                buy(message, buydata)
            elif message.data.split()[0] == 'cb_buy_yes':
                buy_yes(message, buydata)
            elif message.data.split()[0] == 'cb_buy_cancel':
                buy_cancel(message, buydata)
            elif message.data.split()[0] == 'cb_bought':
                bought(message, buydata)


    def buy(message, buydata):
        try:
            cur.execute(f"SELECT pr_name FROM products WHERE rowid = {buydata[1]}")
            name = cur.fetchone()
            buy_menu = types.InlineKeyboardMarkup(row_width=1)
            yes = types.InlineKeyboardButton('Отправить запрос',
                                             callback_data=f"cb_buy_yes {buydata[1]} {message.from_user.username}")
            buy_menu.add(yes)
            bot.send_message(message.message.chat.id,
                             f'✅Вы уверены, что хотите купить товар {name[0]}? \n➡️Если вы согласитесь мы отправим ваш запрос админу-оператору, который свяжется с вами и обсудит детали покупки.',
                             reply_markup=buy_menu)
        except TypeError:
            bot.send_message(message.message.chat.id, f'Что-то пошло не так, обратитесь к тех админу.')
            print(f"ошибка в модуле buy {buydata}")


    def buy_yes(message, buydata):
        cur.execute(f"SELECT pr_name FROM products WHERE rowid = {buydata[1]}")
        name = cur.fetchone()
        buy_buttons = types.InlineKeyboardMarkup(row_width=2)
        bought_button = types.InlineKeyboardButton('Товар продан',
                                                   callback_data=f"cb_bought {buydata[1]} {message.from_user.username}")
        buy_buttons.add(bought_button)
        cancel_buttons = types.InlineKeyboardMarkup(row_width=2)
        cansel_button = types.InlineKeyboardButton('Отменить запрос',
                                                   callback_data=f'cb_buy_cancel {buydata[1]} {message.from_user.username}')
        cancel_buttons.add(cansel_button)
        bot.send_message(message.message.chat.id, f'✅Мы отправили запрос на покупку товара {name[0]}',
                         reply_markup=cancel_buttons)
        bot.send_message(operator_id, f'✅Пришёл запрос на покупку товара {name[0]}, от @{buydata[2]}',
                         reply_markup=buy_buttons)


    def buy_cancel(message, buydata):
        cur.execute(f"SELECT pr_name FROM products WHERE rowid = {buydata[1]}")
        name = cur.fetchone()
        bot.send_message(message.message.chat.id, f'❌ Запрос на покупку товара {name[0]} отменён')
        bot.send_message(operator_id, f'❌ Запрос на покупку товара {name[0]}, от @{buydata[2]} отменили.')


    def bought(message, buydata):
        cur.execute(f"SELECT pr_name FROM products WHERE rowid = {buydata[1]}")
        name = cur.fetchone()
        print(name)
        name = '"' + name[0] + '"'
        print(name)
        cur.execute(f'SELECT in_stock FROM products WHERE rowid = {buydata[1]}')
        in_stockd = cur.fetchone()
        if in_stockd == 1:
            bot.send_message(message.message.chat.id, f'Товары {name} полностью закончились')
            cur.execute(f'DELETE FROM products WHERE pr_name = {name}')
        else:
            cur.execute(f'UPDATE products SET in_stock = in_stock - 1 WHERE pr_name = {name}')
            bot.send_message(message.message.chat.id, f'Удалена 1 штука товара {name}')


    def shop_menu(message):
        bot.send_photo(message.message.chat.id, 'https://imgur.com/pc9rWKE', reply_markup=product_type_menu_buttons)
        # bot.send_message(message.message.chat.id, "Какой тип продукта вас интересует?", reply_markup= product_type_menu_buttons)


    def info_menu(message):
        info_msg = 'ℹ️ <u>Информация</u>\n🔴 Для покупки в боте нажмите "🛒 Наши товары" и выберите интересующую вас продукцию.\n🔴 В случае неполадок или недопонимания вы можете обратиться к админу.\n🔴 Заходите к нам в вк, там ещё больше товаров!\n🔴 Гляньте наши другие проекты ниже!'
        info_markup = types.InlineKeyboardMarkup(row_width=1)
        info_markup_vk = types.InlineKeyboardButton('Наш VK', url='*********')
        info_markup_clothshop = types.InlineKeyboardButton('Магазин одежды в ********** ********',
                                                           url='*************')
        info_markup.add(info_markup_vk, info_markup_clothshop)
        bot.send_message(message.message.chat.id, info_msg, parse_mode='html', reply_markup=info_markup)


    def show_shop(message, sh_type):
        cur.execute(f'SELECT COUNT(*) FROM products WHERE pr_type = {sh_type}')
        num = cur.fetchall()[0][0]
        print(num)
        if num > 0:
            cur.execute(f'SELECT rowid, * FROM products WHERE pr_type = {sh_type}')
            data = cur.fetchmany(99)
            print(data)
            shop_pg1 = types.InlineKeyboardMarkup(row_width=2)
            # if num < 10:
            #     pg2 = types.InlineKeyboardButton('Следующая страница', callback_data='cb_shop_pg2')
            #     shop_pg1.add(pg2)
            for i in range(num):
                print(i)
                cd_pr_buy = []
                product_button = types.InlineKeyboardButton(f'{data[i][2]} | {data[i][3]}₽ | {data[i][4]} шт в наличии',
                                                            callback_data=f"cb_buy {data[i][0]} {message.from_user.username}")
                shop_pg1.add(product_button)
            if sh_type == 1:
                bot.send_photo(message.message.chat.id, "https://imgur.com/dOlQU1Y")
                bot.send_message(message.message.chat.id, f'💨 Выбрана категория : Поды', reply_markup=shop_pg1)
            elif sh_type == 2:
                bot.send_photo(message.message.chat.id, 'https://imgur.com/McjbZCt')
                bot.send_message(message.message.chat.id, f'💨 Выбрана категория : Жидкости', reply_markup=shop_pg1)
            elif sh_type == 3:
                bot.send_photo(message.message.chat.id, 'https://imgur.com/V5RMHoA')
                bot.send_message(message.message.chat.id, f'💨 Выбрана категория : Одноразки', reply_markup=shop_pg1)
            elif sh_type == 4:
                bot.send_photo(message.message.chat.id, 'https://imgur.com/nNcajmm')
                bot.send_message(message.message.chat.id, f'💨 Выбрана категория : Расходники', reply_markup=shop_pg1)


        else:
            bot.send_message(message.message.chat.id, 'Товар данной категории закончился')

        # ТЕРМИНАЛ


    def terminal_menu(message):
        if message.text == "1":
            terminal_menu_open(message)
        else:
            bot.send_message(message.chat.id, 'Код доступа не подходит.')


    def terminal_menu_open(message):
        bot.send_message(message.chat.id, 'Терминал', reply_markup=open_terminal)


    def delete_product_name(message):
        msg = bot.send_message(message.message.chat.id, 'Введите имя товара')
        bot.register_next_step_handler(msg, delete_product1)


    def delete_product1(message):
        global pr_name_
        pr_name_ = "'" + message.text + "'"
        cur.execute(f"SELECT in_stock FROM products WHERE pr_name = {pr_name_}")
        global in_stock_old
        try:
            in_stock_old = cur.fetchone()[0]
            msg = bot.send_message(message.chat.id,
                                   'Введите кол-во товара, которое вы хотите удалить из базы (натуральное число)')
            bot.register_next_step_handler(msg, delete_product2)
        except TypeError:
            bot.send_message(message.chat.id, "Данного наименования нет в базе")

    def delete_product2(message):
        in_stock_oldd = in_stock_old
        pr_named = pr_name_
        if message.text.isnumeric():

            in_stock_del = int(message.text)
            if in_stock_del >= in_stock_oldd:
                bot.send_message(message.chat.id, f'Товары {pr_name} полностью закончились')
                cur.execute(f'DELETE FROM products WHERE pr_name = {pr_named}')
            else:
                cur.execute(f"UPDATE products SET in_stock = in_stock - {in_stock_del} WHERE pr_name = {pr_named}")
                bot.send_message(message.chat.id, f'Удалено {in_stock_del}шт товара {pr_named}')
        else:
            bot.send_message(message.chat.id,
                             'Натуральное число')


    def add_product_type(message):
        msg = bot.send_message(message.message.chat.id,
                               'Выбор типа товара\nВведите нужную цифру\nПод - 1\nЖидкость - 2\nОдноразка - 3\nДругое - 4')
        bot.register_next_step_handler(msg, add_product_name)


    def add_product_name(message):
        global pr_type
        pr_type = message.text
        msg = bot.send_message(message.chat.id, 'Введите имя товара')
        bot.register_next_step_handler(msg, add_product_costs)


    def add_product_costs(message):
        global pr_name
        pr_name = '"' + message.text + '"'
        msg = bot.send_message(message.chat.id, 'Введите стоимость товара (без символа рубля)')
        bot.register_next_step_handler(msg, add_product_num)


    def add_product_num(message):
        global pr_prise
        pr_prise = message.text
        msg = bot.send_message(message.chat.id,
                               'Введите кол-во товара (ОЧЕНЬ ВАЖНО!!! ЭТО ДОЛЖНО БЫТЬ НАТУРАЛЬНОЕ ЧИСЛО!)')
        bot.register_next_step_handler(msg, add_product)


    def add_product(message):
        global in_stock
        if is_number(message.text):
            in_stock = int(message.text)
            if in_stock > 0:
                pr_typed = pr_type
                pr_named = pr_name
                pr_prised = pr_prise
                cur.execute(f"SELECT in_stock FROM products WHERE pr_name = {pr_named}")
                if cur.fetchone() == None:
                    cur.execute(f"INSERT INTO products VALUES({pr_typed}, {pr_named}, {pr_prised}, {in_stock})")
                    bot.send_message(message.chat.id,
                                     f'Добавлен новый товар\nТип товара: {pr_typed}\nНазвание товара: {pr_named}\nСтоимость товара: {pr_prised}₽\nКол-во товара: {in_stock}')
                else:
                    cur.execute(f'UPDATE products SET in_stock = in_stock + {in_stock} where pr_name = {pr_named}')
                    bot.send_message(message.chat.id, f'Изменено кол-во товара {pr_named} на {in_stock} штук')
            else:
                bot.send_message(message.chat.id,
                                 'Число должнно быть натуральным')
                terminal_menu_open(message)
        else:
            bot.send_message(message.chat.id,
                             'Число должно быть натурольным')
            terminal_menu_open(message)


    bot.polling(none_stop=True)
