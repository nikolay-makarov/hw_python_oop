"""Программный модуль фитнес-трекера.
Модуль рассчитывает и отображает результаты тренировки.
"""
from typing import List, Tuple, Dict, ClassVar, Type, Optional
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вывести текст сообщения о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    MIN_IN_HOUR: ClassVar[int] = 60
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    MULTIPLYING_COEFFICIENT: ClassVar[int] = 18
    SUBTRACTING_COEFFICIENT: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.MULTIPLYING_COEFFICIENT * self.get_mean_speed()
                 - self.SUBTRACTING_COEFFICIENT) * self.weight
                / self.M_IN_KM) * self.duration * self.MIN_IN_HOUR


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_COEFFICIENT: ClassVar[float] = 0.035
    SPEED_PER_HEIGHT_COEFFICIENT: ClassVar[float] = 0.029
    height: float

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.WEIGHT_COEFFICIENT * self.weight
                 + (self.get_mean_speed() ** 2 // self.height)
                 * self.SPEED_PER_HEIGHT_COEFFICIENT * self.weight)
                * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    SPEED_COEFFICIENT: ClassVar[float] = 1.1
    WEIGHT_COEFFICIENT: ClassVar[int] = 2
    length_pool: float
    count_pool: int

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM) / self.duration

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.SPEED_COEFFICIENT)
                * self.WEIGHT_COEFFICIENT * self.weight)


TYPES_OF_TRAINING: Dict[str, Type[Training]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking
}


def read_package(type_of_training: str,
                 measured_data: List[int]) -> Optional[Training]:
    """Прочитать данные полученные от датчиков."""
    if type_of_training not in TYPES_OF_TRAINING:
        print('Передан неверный тип тренировки.')
        return None
    try:
        return TYPES_OF_TRAINING[type_of_training](*measured_data)
    except TypeError:
        print('Передано неверное количество данных.')
        return None


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
        if training is not None:
            main(training)
