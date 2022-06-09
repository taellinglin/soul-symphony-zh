from setuptools import setup, find_packages

setup(
    name="soulsymphony",
    packages=find_packages(),
    build_base = "build/",
    setup_requires=[
        'panda3d',
        'panda3d-keybindings',
        'panda3d-stageflow',
        'panda3d-pman',
        'panda3d-logos'

    ],
    options = {
        'build_apps': {
            'platforms':['manylinux2010_x86_64', 'macosx_10_9_x86_64', 'win_amd64', 'win32'],
            'include_patterns' : [
                "**/*.png",
                "**/*.ogg",
                "**/*.wav",
                "**/*.egg",
                "**/*.bam",
                "/*",
                "**/*.otf",
            ],
            'console_apps': {
                'soulsymphony': 'main.py',
            },
            'log_filename': '$USER_APPDATA/SoulSymphony/output.log',
            'log_append': True,
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
        }
    }
)