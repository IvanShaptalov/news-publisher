async def handle_start(message: types.Message, state=None):
    fullname = useful_methods.get_full_user_name(message)
    if not db.get_from_db_multiple_filter(db.User, [db.User.chat_id == message.chat.id]):
        user = db.User()
        user.chat_id, user.user_fullname = message.chat.id, fullname
        user.save()
    await message.reply(text_util.MAIN_MENU_OPENED.format(fullname))
    if state:
        await state.finish()
        db.User.set_in_chat(chat_id=message.chat.id,
                            chat_hash=None)
        logging.info('leave chat, chat state finish')