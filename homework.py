"""Домашнее задание по ООП."""

from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message_template = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Получить сообщение со сведениями о тренировке."""
        return self.message_template.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        # Докстринги для __init__ вынужден оставить из-за PEP8
        # Добавление D107 в .flake8 не помогло
        """Конструктор базового класса."""
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод реализуется в дочерних классах')

    def show_training_info(self) -> InfoMessage:
        """Получить информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить затраченные калории для бега."""
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER
             * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight
            / self.M_IN_KM
            * self.duration * self.MIN_IN_H
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    SPORTSWALKING_CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    SPORTSWALKING_CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        """Конструктор дочернего класса SportsWalking."""
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить затраченные калории для спортивной ходьбы."""
        return (
            (self.SPORTSWALKING_CALORIES_WEIGHT_MULTIPLIER * self.weight
             + ((self.get_mean_speed() * self.KMH_IN_MSEC)**2
                / (self.height / self.CM_IN_M))
             * self.SPORTSWALKING_CALORIES_MEAN_SPEED_MULTIPLIER * self.weight)
            * (self.duration * self.MIN_IN_H)
        )


class Swimming(Training):
    """Тренировка: плавание."""

    SWIMMING_CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    SWIMMING_CALORIES_MEAN_SPEED_MULTIPLIER: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        """Конструктор дочернего класса Swimming."""
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость для плавания."""
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить затраченные калории для плавания."""
        return (
            (self.get_mean_speed()
             + self.SWIMMING_CALORIES_MEAN_SPEED_SHIFT)
            * self.SWIMMING_CALORIES_MEAN_SPEED_MULTIPLIER
            * self.weight
            * self.duration
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_classes: dict[str, type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    if workout_type not in workout_classes:
        raise ValueError(f'Не найден тип тренировки {workout_type}')
    return workout_classes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
