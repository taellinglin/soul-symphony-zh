from os import path
import builtins
from setuptools import setup, find_packages 

import pman.build_apps

CONFIG = pman.get_config()

APP_NAME = CONFIG['general']['name']

setup(
    name=APP_NAME,
    packages=find_packages(),
    build_base = "build/",
    setup_requires=[
        'pytest-runner',
        'panda3d',
        'panda3d-keybindings',
        'panda3d-stageflow',
        'panda3d-pman',
    ],
    tests_require=[
        'pytest',
        'pylint~=2.6.0',
        'pytest-pylint',
    ],
    cmdclass={
        'build_apps': pman.build_apps.BuildApps,
    },
    options={
        'build_apps': {
            'platforms':['win_amd64'],
            'include_patterns' : [
                "**/*.png",
                "**/*.ogg",
                "**/*.wav",
                "**/*.egg",
                "**/*.bam",
                "/*"
            ],
            'rename_paths': {
                CONFIG['build']['export_dir']+ 'assets/',
            },
            'gui_apps': {
                APP_NAME: CONFIG['run']['main_file'],
            },
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
            'use_optimized_wheels': True
            
        },
    }
)
