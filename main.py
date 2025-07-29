# main.py - Telegram bot entry point


@dp.callback_query_handler(lambda c: c.data == "gift")
async def gift_info(call: types.CallbackQuery):
    lang = get_user(call.from_user.id)["lang"]
    await call.message.answer(t("gift_prompt", lang))

@dp.message_handler(lambda msg: msg.reply_to_message and msg.text.isdigit())
async def handle_gift(message: types.Message):
    recipient_id = message.reply_to_message.from_user.id
    stars = int(message.text)
    sender = get_user(message.from_user.id)
    if sender["stars"] < stars:
        await message.reply("❌ Недостаточно звёзд")
        return
    # Обновляем
    data = load_data()
    uid_sender = str(message.from_user.id)
    uid_recipient = str(recipient_id)

    data[uid_sender]["stars"] -= stars
    data[uid_sender]["gifts"].append({"to": recipient_id, "stars": stars})
    if uid_recipient not in data:
        data[uid_recipient] = {
            "lang": "ru", "stars": 0, "spent": 0, "ref": None,
            "orders": [], "gifts": [], "reg": "-"
        }
    data[uid_recipient]["stars"] += stars
    data[uid_recipient]["gifts"].append({"from": message.from_user.id, "stars": stars})
    save_data(data)
    await message.reply(f"🎁 Вы подарили {stars}⭐ пользователю {recipient_id}")


@dp.callback_query_handler(lambda c: c.data == "orders")
async def show_orders(call: types.CallbackQuery):
    u = get_user(call.from_user.id)
    lang = u["lang"]
    orders = u.get("orders", [])
    gifts = u.get("gifts", [])

    text = f"{t('orders_history', lang)}:\n"
    if orders:
        for i, order in enumerate(orders, 1):
            text += f"{i}) {order['stars']}⭐ за {order['price']} TON\n"
    else:
        text += f"{t('no_orders', lang)}\n"

    text += f"\n{t('gift_history', lang)}:\n"
    if gifts:
        for g in gifts:
            if 'from' in g:
                text += f"📩 Получено {g['stars']}⭐ от {g['from']}\n"
            elif 'to' in g:
                text += f"📤 Отправлено {g['stars']}⭐ пользователю {g['to']}\n"
    else:
        text += "—\n"

    await call.message.edit_text(text)
