from abc import ABC, abstractmethod
from enum import Enum


# ---------- Enums ----------
class EngineType(Enum):
    GASOLINE = "Gasoline"
    DIESEL = "Diesel"
    HYBRID = "Hybrid"
    ELECTRIC = "Electric"


class Color(Enum):
    WHITE = "White"
    BLACK = "Black"
    SILVER = "Silver"
    RED = "Red"
    BLUE = "Blue"
    GREEN = "Green"


class WheelType(Enum):
    STANDARD = "Standard"
    SPORT = "Sport"
    PREMIUM = "Premium"


class SoundSystem(Enum):
    BASIC = "Basic"
    PREMIUM = "Premium"
    BOSE = "Bose"


class InteriorMaterial(Enum):
    CLOTH = "Cloth"
    LEATHER = "Leather"
    PREMIUM_LEATHER = "Premium Leather"


# ---------- Interface Builder ----------
class Builder(ABC):
    @abstractmethod
    def set_engine(self, engine: EngineType): pass
    @abstractmethod
    def set_color(self, color: Color): pass
    @abstractmethod
    def set_wheels(self, wheels: WheelType): pass
    @abstractmethod
    def set_sound(self, sound: SoundSystem): pass
    @abstractmethod
    def set_interior(self, interior: InteriorMaterial): pass
    @abstractmethod
    def set_sunroof(self, sunroof: bool): pass
    @abstractmethod
    def set_gps(self, gps: bool): pass
    @abstractmethod
    def set_parking_sensors(self, parking_sensors: bool): pass
    @abstractmethod
    def set_bluetooth(self, bluetooth: bool): pass
    @abstractmethod
    def build(self): pass


# ---------- Concrete Builder ----------
class CarBuilder(Builder):
    def __init__(self):
        self.engine = None
        self.color = None
        self.wheels = None
        self.sound = None
        self.interior = None
        self.sunroof = False
        self.gps = False
        self.parking_sensors = False
        self.bluetooth = False

    def set_engine(self, engine: EngineType): self.engine = engine; return self
    def set_color(self, color: Color): self.color = color; return self
    def set_wheels(self, wheels: WheelType): self.wheels = wheels; return self
    def set_sound(self, sound: SoundSystem): self.sound = sound; return self
    def set_interior(self, interior: InteriorMaterial): self.interior = interior; return self
    def set_sunroof(self, sunroof: bool): self.sunroof = sunroof; return self
    def set_gps(self, gps: bool): self.gps = gps; return self
    def set_parking_sensors(self, parking_sensors: bool): self.parking_sensors = parking_sensors; return self
    def set_bluetooth(self, bluetooth: bool): self.bluetooth = bluetooth; return self

    def build(self):
        car = Car(
            engine=self.engine,
            color=self.color,
            wheels=self.wheels,
            sound=self.sound,
            interior=self.interior,
            sunroof=self.sunroof,
            gps=self.gps,
            parking_sensors=self.parking_sensors,
            bluetooth=self.bluetooth
        )
        return car


# ---------- Product ----------
class Car:
    def __init__(self, engine: EngineType, color: Color, wheels: WheelType,
                 sound: SoundSystem, interior: InteriorMaterial, sunroof: bool, gps: bool, parking_sensors: bool, bluetooth: bool):
        self.engine = engine
        self.color = color
        self.wheels = wheels
        self.sound = sound
        self.interior = interior
        self.sunroof = sunroof
        self.gps = gps
        self.parking_sensors = parking_sensors
        self.bluetooth = bluetooth

    def __str__(self):
        details = [
            f"Engine: {self.engine.value if self.engine else 'Not specified'}",
            f"Color: {self.color.value if self.color else 'Not specified'}",
            f"Wheels: {self.wheels.value if self.wheels else 'Not specified'}",
            f"Sound System: {self.sound.value if self.sound else 'Not specified'}",
            f"Interior: {self.interior.value if self.interior else 'Not specified'}",
            f"Sunroof: {'Yes' if self.sunroof else 'No'}",
            f"GPS: {'Yes' if self.gps else 'No'}",
            f"Parking Sensors: {'Yes' if self.parking_sensors else 'No'}",
            f"Bluetooth: {'Yes' if self.bluetooth else 'No'}",
        ]
        return "Car features:\n  " + "\n  ".join(details)


# ---------- Director ----------
class Director:
    def __init__(self, builder: Builder):
        self.builder = builder

    def construct_sports_car(self):
        return (self.builder
                .set_engine(EngineType.GASOLINE)
                .set_color(Color.RED)
                .set_wheels(WheelType.SPORT)
                .set_sound(SoundSystem.BOSE)
                .set_interior(InteriorMaterial.PREMIUM_LEATHER)
                .set_sunroof(True)
                .set_gps(True)
                .build())

    def construct_economy_car(self):
        return (self.builder
                .set_engine(EngineType.DIESEL)
                .set_color(Color.WHITE)
                .set_wheels(WheelType.STANDARD)
                .set_sound(SoundSystem.BASIC)
                .set_interior(InteriorMaterial.CLOTH)
                .build())

    def construct_luxury_car(self):
        return (self.builder
                .set_engine(EngineType.HYBRID)
                .set_color(Color.SILVER)
                .set_wheels(WheelType.PREMIUM)
                .set_sound(SoundSystem.PREMIUM)
                .set_interior(InteriorMaterial.LEATHER)
                .set_sunroof(True)
                .set_gps(True)
                .build())


# ---------- Client (main) ----------
def main():
    builder = CarBuilder()
    director = Director(builder)

    # Customer chooses predefined cars
    sports_car = director.construct_sports_car()
    economy_car = director.construct_economy_car()
    luxury_car = director.construct_luxury_car()

    # Customer builds a custom car
    custom_car = (builder
                  .set_engine(EngineType.ELECTRIC)
                  .set_color(Color.BLUE)
                  .set_wheels(WheelType.SPORT)
                  .set_interior(InteriorMaterial.CLOTH)
                  .set_gps(True)
                  .set_parking_sensors(True)
                  .set_bluetooth(True)
                  .build())

    print("Predefined cars:")
    print("Sport Car:")
    print(sports_car)
    print("Economy Car:")
    print(economy_car)
    print("Luxury Car:")
    print(luxury_car)

    print("\nCustom car:")
    print(custom_car)


if __name__ == "__main__":
    main()