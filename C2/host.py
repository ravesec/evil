from datetime import datetime
from dataclasses import dataclass, field
from cryptography.fernet import Fernet
from collections import deque
import json


@dataclass(slots=True)
class Host:
    _hostname: str
    _address: str
    _cmd_queue: deque = field(init=False)
    _cmd_number: int = field(init=False)
    _cmd_history: dict = field(init=False)  # dict {cmd_number: {'cmd': cmd, 'return_code': return_code}, ...}
    _last_status: int = field(init=False)
    _last_seen: datetime = field(init=False, default_factory=datetime.now)

    def __post_init__(self):
        self._cmd_queue = deque()
        self._cmd_history = {}
        self._last_status = -1
        self._cmd_number = 0

    @property
    def hostname(self):
        return self._hostname

    @property
    def address(self):
        return self._address

    @property
    def last_seen(self):
        return self._last_seen

    @property
    def cmd(self):
        return self._cmd_queue[-1]

    @property
    def cmd_queue(self):
        return self._cmd_queue

    @property
    def cmd_number(self):
        return self._cmd_number

    @property
    def cmd_history(self):
        return self._cmd_history

    @property
    def last_status(self):
        return self._last_status

    @cmd_number.setter
    def cmd_number(self, value):
        self._cmd_number = value

    @last_status.setter
    def last_status(self, value):
        self._last_status = value

    @cmd_history.setter
    def cmd_history(self, value):
        self._cmd_history = value

    @cmd_queue.setter
    def cmd_queue(self, value):
        self._cmd_queue = value

    @last_seen.setter
    def last_seen(self, value):
        self._last_seen = value

    def keep_alive(self) -> None:
        self._last_seen = datetime.now()
