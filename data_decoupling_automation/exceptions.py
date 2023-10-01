class BadInputException(Exception):
    """
    When a user submits a bad input we can't validate it entirely until we try to process it.

    This exception allows us so communicate the input related issue to the user.
    """

    def __init__(self, response_dict: dict, *args) -> None:
        self.response_dict = response_dict
        super().__init__(str(response_dict), *args)
