# -*- coding: utf-8 -*-
"""wrap environment settings"""
from dataclasses import dataclass
from os import environ
from typing import Optional


@dataclass
class Config():
    """Base configuration"""
    name: str
    log_level: Optional[str] = environ.get('MYPCH_LOG_LEVEL', 'DEBUG')

    def __post_init__(self) -> None:
        if self.name == 'dev' and self.log_level == '':
            self.log_level = 'DEBUG'
        if self.name == 'test' and self.log_level == '':
            self.log_level = 'DEBUG'
        if self.name == 'test' and self.log_level == '':
            self.log_level = 'INFO'
