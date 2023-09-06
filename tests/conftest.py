custom_order = [
    "empty_setup",
    "mock_test_a1",
    "mock_test_c1",
    "mock_test_a2",
    "mock_test_a3",
    "mock_test_b2",
    "create_user",
    "create_spam",
    "offer_spam",
    "order_spam_insufficient_funds",
    "deposit_money_in_bank",
    "order_spam",
    "close_threads_automatically",
    "eat_spam",
    "delete_user",
]


class Conftest:
    def get_testing_order(self, tests_to_be_run):
        order = [None] * len(custom_order)
        for test in tests_to_be_run:
            order[custom_order.index(test.func.__name__)] = test
        return list(filter(None, order))
