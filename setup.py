from __future__ import annotations

from setuptools import find_packages
from setuptools import setup

setup(
    name='meu_checklist_tarefas',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)
