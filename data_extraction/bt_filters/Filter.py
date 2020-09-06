class Filter:
    def __init__(self):
        self._filtered_list = None
        self.__list_to_filter = []

    def filter(self, list_to_filter: list) -> list:
        if self._filtered_list is None:
            self._apply_filter(list_to_filter)

        return self._filtered_list

    def _apply_filter(self, list_to_filter: list):
        pass
