from dataclasses import dataclass, asdict
from typing import Type, Dict, ClassVar


@dataclass
class InfoMessage:
    """Training Information Message."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Basic Training Class."""
    action: int
    duration: float
    weight: float

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_HOUR: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Get the distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get the average speed of movement."""
        return Training.get_distance(self) / self.duration

    try:
        def get_spent_calories(self) -> float:
            """Get the number of calories consumed."""
            pass
    except NotImplementedError:
        print('The method is not implemented')

    def show_training_info(self) -> InfoMessage:
        """Return the information message about the training session."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Training: running."""
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar = 1.79
    MIN: ClassVar = 60

    def get_spent_calories(self) -> float:
        """Get the number of calories consumed."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * Training.get_mean_speed(self)
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MIN))


@dataclass
class SportsWalking(Training):
    """Training: sports walking."""
    height: float

    WEIGHT_MULTIPLIER: ClassVar[float] = 0.035
    AVG_MULTIPLIER: ClassVar[float] = 0.029
    CONVERSION_ms: ClassVar[float] = 0.278
    CONVERSION_m: ClassVar[int] = 100
    MIN: ClassVar[int] = 60

    def get_spent_calories(self) -> float:
        """Get the number of calories consumed."""
        return ((self.WEIGHT_MULTIPLIER * self.weight
                + (Training.get_mean_speed(self)
                   * self.CONVERSION_ms)**2
                / (self.height / self.CONVERSION_m)
                * self.AVG_MULTIPLIER * self.weight)
                * (self.duration * self.MIN))


@dataclass
class Swimming(Training):
    """Training: swimming."""
    length_pool: float
    count_pool: float

    LEN_STEP: ClassVar[float] = 1.38
    OFFSET_AVG_SPEED: ClassVar[float] = 1.1
    SPEED_MULTIPLIER: ClassVar[int] = 2

    def get_distance(self) -> float:
        """Get the distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_spent_calories(self) -> float:
        """Get the number of calories consumed."""
        return ((Swimming.get_mean_speed(self) + self.OFFSET_AVG_SPEED)
                * self.SPEED_MULTIPLIER * self.weight * self.duration)

    def get_mean_speed(self) -> float:
        """Get the average speed of movement."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Read the data received from the sensors."""
    dict_training: Dict[str, Type[training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in dict_training:
        info_packages: training = dict_training[workout_type](*data)
        return info_packages
    else:
        print('Тренировка не найдена!')


def main(training: Training) -> None:
    """Main Function."""
    info = Training.show_training_info(training)
    print(info.get_message())


if __name__ == '__main__':
    packages: list = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
