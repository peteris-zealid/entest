import tests.project_src as src
import tests.project_src.internals as src_internals
from entest import STATUS, assert_raises, depends_on


@depends_on()
def create_user():
    user1 = src.create_user("my_name")
    user2 = src.create_user("other_name")
    return {
        "user_id1": user1["id"],
        "user_id2": user2["id"],
    }


@depends_on()
def create_spam(user_id1):
    spam = src.create_spam(user_id1, "500g")
    return {
        "spam_id": spam["id"],
    }


@depends_on()
def offer_spam(spam_id, user_id2):
    src.offer_spam(spam_id, user_id2, "3.40£")


@depends_on(create_user)
def deposit_money_in_bank(user_id2):
    src.deposit(user_id2, "100£")


@depends_on(offer_spam, previous=True)
def order_spam(user_id2, spam_id):
    src.order_spam(user_id2, spam_id)
    spam = src.internals.get_spam(spam_id)
    assert spam["owner"] == user_id2


@depends_on(offer_spam, without=deposit_money_in_bank)
def order_spam_insufficient_funds(user_id1, user_id2, spam_id):
    assert_raises(
        lambda: src.order_spam(user_id2, spam_id),
        message="insufficient_funds",
    )
    spam = src_internals.get_spam(spam_id)
    assert spam["owner"] == user_id1


@depends_on(create_spam, run_last=True)
def eat_spam(spam_id, user_id1, user_id2):
    user_id = src.eat_spam(spam_id)
    expected_user_id = user_id2 if order_spam.status == STATUS.passed else user_id1
    assert user_id == expected_user_id


@depends_on(create_user, run_last=True)
def delete_user(user_id1):
    src.delete_user(user_id1)
