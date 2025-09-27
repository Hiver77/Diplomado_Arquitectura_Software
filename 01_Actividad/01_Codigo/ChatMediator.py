from abc import ABC, abstractmethod



class Mediator(ABC):
    @abstractmethod
    def register(self, user):
        ...

    @abstractmethod
    def unregister(self, username):
        ...

    @abstractmethod
    def send(self, sender, message):
        ...

# -----------------------------
# Mediador
# -----------------------------
class ChatRoom(Mediator):
    def __init__(self, name):
        self._name = name
        self._users = {}

    def register(self, user):
        self._users[user.username] = user
        print(f"* {user.username} se unió a #{self._name}")

    def unregister(self, username):
        if username in self._users:
            del self._users[username]
            print(f"* {username} se fue de #{self._name}")

    def send(self, sender, message, to=None):
        for uname, user in self._users.items():
            if uname != sender.username:
                user.receive(f"[{sender.username}] {message}")



class User:
    def __init__(self, username, room):
        self.username = username
        self._room = room
        self._room.register(self)

    def send(self, message):
        self._room.send(self, message)

    def receive(self, message):
        print(f"[INBOX {self.username}] {message}")

    def leave(self):
        self._room.unregister(self.username)


if __name__ == "__main__":
    room = ChatRoom("Arquitectura de Software")

    user1 = User("Eliana", room)
    user2 = User("Iver", room)
    user3 = User("Leidy", room)
    user4 = User("Juan", room)

    user1.send("Hola a todos!")      
    user2.send("Hola!") 
    user3.send("Como estan todos?")      
    user4.send("Buenas tardes a todos")

    user2.leave()