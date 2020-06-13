class NotCsvException(Exception):
    """this is the exception for check the csv type"""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name + "'s" + " file type is not csv"
