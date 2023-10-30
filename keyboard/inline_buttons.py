from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def start_keyboard():
    markup = InlineKeyboardMarkup()
    questionnaire_button = InlineKeyboardButton(
        "Start Questionnaire",
        callback_data="start_questionnaire"
    )
    registration_button = InlineKeyboardButton(
        "Registration",
        callback_data="fsm_start"
    )
    profile_button = InlineKeyboardButton(
        "My Profile",
        callback_data="my_profile"
    )
    random_profile_button = InlineKeyboardButton(
        "View Profile",
        callback_data="random_profile"
    )
    reference_menu_button = InlineKeyboardButton(
        "Referral Menu",
        callback_data="reference_menu"
    )
    news_list_menu_button = InlineKeyboardButton(
        "News",
        callback_data="news_list_menu"
    )
    fav_news_list_menu_button = InlineKeyboardButton(
        "Favorite News",
        callback_data="fav_news_list_menu"
    )
    markup.add(questionnaire_button)
    markup.add(registration_button)
    markup.add(profile_button)
    markup.add(random_profile_button)
    markup.add(reference_menu_button)
    markup.add(news_list_menu_button)
    markup.add(fav_news_list_menu_button)
    return markup


async def questionnaire_one_keyboard():
    markup = InlineKeyboardMarkup()
    yes_button = InlineKeyboardButton(
        "Yes",
        callback_data="hungry_yes"
    )
    no_button = InlineKeyboardButton(
        "No",
        callback_data="hungry_no"
    )
    markup.add(yes_button)
    markup.add(no_button)
    return markup


async def admin_keyboard():
    markup = InlineKeyboardMarkup()
    admin_user_list_button = InlineKeyboardButton(
        "User list",
        callback_data="admin_user_list"
    )
    markup.add(admin_user_list_button)
    return markup


async def like_dislike_keyboard(owner_tg_id):
    markup = InlineKeyboardMarkup()
    like_button = InlineKeyboardButton(
        "Like",
        callback_data=f"user_form_like_{owner_tg_id}"
    )
    dislike_button = InlineKeyboardButton(
        "Dislike",
        callback_data="random_profile"
    )
    markup.add(like_button)
    markup.add(dislike_button)
    return markup


async def edit_delete_form_keyboard():
    markup = InlineKeyboardMarkup()
    edit_button = InlineKeyboardButton(
        "Edit",
        callback_data=f"fsm_start"
    )
    delete_button = InlineKeyboardButton(
        "Delete",
        callback_data="delete_user_form"
    )
    markup.add(edit_button)
    markup.add(delete_button)
    return markup


async def my_profile_register_keyboard():
    markup = InlineKeyboardMarkup()
    my_profile_button = InlineKeyboardButton(
        "Registration",
        callback_data="fsm_start"
    )
    markup.add(my_profile_button)
    return markup


async def reference_menu_keyboard():
    markup = InlineKeyboardMarkup()
    reference_link_button = InlineKeyboardButton(
        "Referral Link",
        callback_data="reference_link"
    )
    reference_list_button = InlineKeyboardButton(
        "Referral List",
        callback_data="reference_list"
    )
    markup.add(reference_link_button)
    markup.add(reference_list_button)
    return markup


async def news_menu_keyboard(news_id):
    markup = InlineKeyboardMarkup()
    news_link_button = InlineKeyboardButton(
        "Save",
        callback_data=f"update_news_link_{news_id}"
    )
    markup.add(news_link_button)
    return markup
