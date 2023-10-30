class News:
    def __init__(self, id, owner, title, href):
        self.__id = id
        self.__owner = owner
        self.__title = title
        self.__href = href

    @property
    def id(self):
        return self.__id

    @property
    def owner(self):
        return self.__owner

    @property
    def title(self):
        return self.__title

    @property
    def href(self):
        return self.__href

    def __str__(self):
        return f"News id: {self.__id}, owner: {self.__owner}, title: {self.__title}, href: {self.__href}"