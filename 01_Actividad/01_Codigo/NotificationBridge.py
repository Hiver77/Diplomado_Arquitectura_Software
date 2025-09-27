from abc import ABC, abstractmethod
from enum import Enum, auto
 
 
 
 
class User:
    def __init__(self, user_id: str):
        self.user_id = user_id
 
    def __repr__(self) -> str:
        return f"User(user_id={self.user_id!r})"
 
 
class NotificationPayload:
    """
    Contenido de la notificacion: titulo y mensaje
    """
    def __init__(self, title: str, message: str):
        self.title = title
        self.message = message
 
    def __repr__(self) -> str:
        return f"NotificationPayload(title={self.title!r}, message={self.message!r})"
 
 
# Abstraccion Tipo de plataforma
class Platform(ABC):
    @abstractmethod
    def deliver(self,
                title: str,
                message: str) -> None:
        ...
 
class WebPlatform(Platform):
    def deliver(self,
                title: str,
                message: str) -> None:
        print(f"[WEB]  {title} -> {message} ")
 
 
class MobilePlatform(Platform):
    def deliver(self,
                title: str,
                message: str) -> None:
        print(f"[MOBILE]  {title.upper()} — {message} ")
 
 
class DesktopPlatform(Platform):
    def deliver(self,
                title: str,
                message: str) -> None:
        print(f"[DESKTOP]  {title} -> {message} ")
 
 
# Abstraccion Tipo de notificacion
class Notification(ABC):
    """
    Abstraccion en notificacion
    """
    def __init__(self, platform: Platform, user: User):
        self._platform = platform
        self._user = user
 
    def set_platform(self, platform: Platform) -> None:
        self._platform = platform
 
    @abstractmethod
    def send(self, payload: NotificationPayload) -> None:
        ...
 
 
class MessageNotification(Notification):
    def send(self, payload: NotificationPayload) -> None:
        self._platform.deliver(f"Mensaje: {payload.title}", payload.message)
 
 
class AlertNotification(Notification):
    def send(self, payload: NotificationPayload) -> None:
        self._platform.deliver(f"Alerta: {payload.title}", f"Atención! {payload.message}")
 
 
class WarningNotification(Notification):
    def send(self, payload: NotificationPayload) -> None:
        self._platform.deliver(f"Advertencia: {payload.title}", payload.message)
 
 
class ConfirmationNotification(Notification):
    def send(self, payload: NotificationPayload) -> None:
        self._platform.deliver(f"Confirmacion: {payload.title}", payload.message )
 
 
 
if __name__ == "__main__":
    user1 = User("Alice")
 
    # MESSAGE on WEB
    n1 = MessageNotification(WebPlatform(), user1)
    n1.send(NotificationPayload("Bienvenido", "Bienvenido al sistema"))
 
    print("\n---\n")
 
    # ALERT on MOBILE
    n2 = AlertNotification(MobilePlatform(), user1)
    n2.send(NotificationPayload("Uso de CPU", "Supera el 90%"))
 
    print("\n---\n")
 
    # WARNING on DESKTOP, then switch to WEB
    n3 = WarningNotification(DesktopPlatform(), user1)
    n3.send(NotificationPayload("Disco", "Poco espacio en disco"))
    n3.set_platform(WebPlatform())
    n3.send(NotificationPayload("Disco", "Poco espacio en disco"))
 
    print("\n---\n")
 
    # CONFIRMATION on WEB
    n4 = ConfirmationNotification(WebPlatform(), user1)
    n4.send(NotificationPayload("Pago recibido", "Factura enviada al correo"))