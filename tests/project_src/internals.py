users = {}
spam_dict = {}


def get_spam(spam_id: int):
    spam = spam_dict[spam_id]
    setattr(spam, "owner", spam["owner"])
    return spam
