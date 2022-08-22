"""Программный модуль фитнес-трекера.
Модуль рассчитывает и отображает результаты тренировки.
"""
from __future__ import annotations
from typing import Callable


class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.mean_speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вывести текст сообщения о тренировке."""
        return f'Тип тренировки: {self.training_type}; ' \
               f'Длительность: {self.duration:.3f} ч.; ' \
               f'Дистанция: {self.distance:.3f} км; ' \
               f'Ср. скорость: {self.mean_speed:.3f} км/ч; ' \
               f'Потрачено ккал: {self.calories:.3f}.'


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    action: int
    duration: float
    weight: float

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        calories = ((coeff_calorie_1 * self.get_mean_speed()
                     - coeff_calorie_2) * self.weight
                    / self.M_IN_KM) * self.duration * 60
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    calories: float

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
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        calories = (coeff_calorie_1 * self.weight
                    + (self.get_mean_speed() ** 2 // self.height)
                    * coeff_calorie_2 * self.weight) * self.duration * 60
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    length_pool: float
    count_pool: int
    calories: float
    mean_speed: float

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
        mean_speed: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM) / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: int = 2
        calories: float = (self.get_mean_speed()
                           + coeff_calorie_1) * coeff_calorie_2 * self.weight
        return calories


def read_package(type_of_training: str, measured_data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_of_training: dict[str, Callable] = {'SWM': Swimming,
                                              'RUN': Running,
                                              'WLK': SportsWalking
                                              }
    return types_of_training[type_of_training](*measured_data)


def main(activity: Training) -> None:
    """Главная функция."""
    info: InfoMessage = activity.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
