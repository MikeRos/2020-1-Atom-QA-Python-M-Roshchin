class UndefinedBrowser(Exception):
    pass


class UnexpectedDBData(Exception):
    def __init__(self):
        self.message = "Somehow we found test data in DB. Remove it or change test data if this data is real."

    def __str__(self):
        return self.message


class DBDataNotFound(Exception):
    def __init__(self):
        self.message = "Test data that should be inserted in DB during test not found"

    def __str__(self):
        return self.message


class NoNewTab(Exception):
    def __init__(self):
        self.message = "Page is not opened in new tab"
        raise AssertionError

    def __str__(self):
        return self.message