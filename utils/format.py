# delete link properties from user_id in telegram message with empty symbol
def format_user_id(user_id: str) -> str:
    return user_id[:3] + '&#8203;' + user_id[3:]