"""Программный модуль фитнес-трекера.
Модуль рассчитывает и отображает результаты тренировки.
"""
from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List, Tuple, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
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
        """Вывести текст сообщения о тренировке."""
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP: ClassVar[float] = 0.65
    MIN_IN_HOUR: ClassVar[int] = 60
    M_IN_KM: ClassVar[int] = 1000

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Дочерний метод класса '
                                  f'{type(self).__name__} не переопределен')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    MULTIPLYING_COEFFICIENT: int = 18
    SUBTRACTING_COEFFICIENT: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.MULTIPLYING_COEFFICIENT * self.get_mean_speed()
                 - self.SUBTRACTING_COEFFICIENT) * self.weight
                / self.M_IN_KM) * self.duration * self.MIN_IN_HOUR


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    SPEED_PER_HEIGHT_COEFFICIENT: ClassVar[float] = 0.029
    WEIGHT_COEFFICIENT: ClassVar[float] = 0.035

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.WEIGHT_COEFFICIENT * self.weight
                 + (self.get_mean_speed() ** 2 // self.height)
                 * self.SPEED_PER_HEIGHT_COEFFICIENT * self.weight)
                * self.duration * self.MIN_IN_HOUR)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: int
    LEN_STEP: ClassVar[float] = 1.38
    SPEED_COEFFICIENT: ClassVar[float] = 1.1
    WEIGHT_COEFFICIENT: ClassVar[int] = 2

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM) / self.duration

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.SPEED_COEFFICIENT)
                * self.WEIGHT_COEFFICIENT * self.weight)


TYPES_OF_TRAINING: Dict[str, Tuple[Type[Training], int]] = {
    'SWM': (Swimming, 5),
    'RUN': (Running, 3),
    'WLK': (SportsWalking, 4)
}


def read_package(type_of_training: str,
                 measured_data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if type_of_training not in TYPES_OF_TRAINING:
        raise KeyError('Передан неверный тип тренировки')
    elif TYPES_OF_TRAINING[type_of_training][1] != len(measured_data):
        raise TypeError('Передано неверное количество данных')
    else:
        return TYPES_OF_TRAINING[type_of_training][0](*measured_data)


def main(activity: Training) -> None:
    """Главная функция."""
    print(activity.show_training_info().get_message())


if __name__ == '__main__':
    packages: List[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
