from .internals import users, spam_dict

def create_user(username: str) -> dict:
    users[id(username)] = {"username": username, "deposited": 0}
    return {
        "id": id(username),
    }

def create_spam(user_id: int, amount: str) -> dict:
    spam_dict[id(amount)] = {"spam_amount": amount, "owner": user_id}
    return {
        "id": id(amount),
    }

def offer_spam(spam_id: int, user_id: int, amount: str) -> dict:
    return {}

def deposit(user_id: int, amount: str) -> dict:
    users[user_id]["deposited"] += int(amount[:-1])
    return {}

def order_spam(user_id: int, spam_id: int) -> dict:
    if users[user_id]["amount"] > 0:
        spam_dict[spam_id]["owner"] = user_id
    return {}

def eat_spam(spam_id):
    spam_owner = spam_dict[spam_id]["owner"]
    del spam_dict[spam_id]
    return spam_owner

def delete_user(user_id: str) -> dict:
    del users[user_id]
