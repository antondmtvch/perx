import abc
import asyncio
import itertools

from enum import Enum
from datetime import datetime

from app.exceptions import TaskValidationError


class Status(Enum):
    IN_QUEUE = 1
    PROCESS = 2


class Field(abc.ABC):
    def __init__(self, name: str):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self.name] = value

    @abc.abstractmethod
    def validate(self, value):
        pass


class IntegerField(Field):
    def validate(self, value):
        if not isinstance(value, int):
            raise TaskValidationError(f'{self.name} must be int not {value.__class__.__name__}')


class FloatField(Field):
    def validate(self, value):
        if not isinstance(value, float):
            raise TaskValidationError(f'{self.name} must be float not {value.__class__.__name__}')


class TaskMeta(type):
    def __new__(mcs, name, bases, attrs):
        fields = []
        for k, v in attrs.items():
            if isinstance(v, Field):
                fields.append(k)
        attrs['fields'] = fields
        attrs['id'] = itertools.count(0, 1)
        cls = super(TaskMeta, mcs).__new__(mcs, name, bases, attrs)
        return cls


class Task(metaclass=TaskMeta):
    count = IntegerField('count')
    delta = FloatField('delta')
    start = IntegerField('start')
    interval = FloatField('interval')

    def __init__(self, **kwargs):
        for field in self.fields:
            setattr(self, field, kwargs.get(field))
        self.id = self.__class__.__dict__['id'].__next__()
        self.current_value = self.start
        self.started_at = None
        self.status = Status.IN_QUEUE.value

    def __repr__(self):
        attrs = ', '.join([f'{k}={v}' for k, v in self.__dict__.items()])
        return f'<{self.__class__.__name__} [{attrs}]>'

    async def run(self):
        self.started_at = datetime.now().isoformat()
        self.status = Status.PROCESS.value
        for _ in range(1, self.count):
            self.current_value += self.delta
            await asyncio.sleep(self.interval)

    def serialize(self):
        return self.__dict__
