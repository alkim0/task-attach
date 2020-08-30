class Menu(object):
    def __init__(self, options):
        self._options = options

    def show_and_pick(self):
        """
        Returns the index of the chosen option in `options`
        """
        for i, option in enumerate(self._options):
            print("{}) {}".format(i + 1, option))

        while True:
            number = input("Pick a number: ")
            try:
                number = int(number)
                assert 0 < number <= len(self._options)
                return number - 1
            except:
                print("That's not a valid number")
