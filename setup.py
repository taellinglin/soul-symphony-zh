from setuptools import setup, find_packages
import pman.build_apps
import toml
import os

# Load the .pman configuration
CONFIG = toml.load(".pman")

# Access configuration values
APP_NAME = CONFIG["general"]["name"]
EXPORT_DIR = CONFIG["build"]["export_dir"]
ASSET_DIR = CONFIG["build"]["asset_dir"]
MAIN_FILE = CONFIG["run"]["main_file"]

# Path to your DLLs
dll_dir = os.path.join(os.getcwd(), "lib")
dll_files = [
    os.path.join(dll_dir, dll)
    for dll in os.listdir(dll_dir)
    if dll.endswith(".dll") or dll.endswith(".pyd")
]

setup(
    name=APP_NAME,
    packages=find_packages(),
    build_base="build/",
    setup_requires=[
        "pytest-runner",
        "panda3d",
        "panda3d-keybindings",
        "panda3d-stageflow",
        "panda3d-pman",
        "direct",
    ],
    tests_require=[
        "pytest",
        "pylint~=2.6.0",
        "pytest-pylint",
    ],
    cmdclass={
        "build_apps": pman.build_apps.BuildApps,
    },
    options={
        "build_apps": {
            "include_modules": {
                "*": [
                    "pyaudio",  # Underlying PortAudio library
                    "numpy",  # Required by sounddevice
                ]
            },
            "platforms": [
                "win32",
                "win_amd64",
                "manylinux2014_x86_64",
                "macosx_10_9_x86_64",
            ],
            "include_patterns": [
                "assets/*.*",
                "**/*.png",
                "**/*.ogg",
                "**/*.wav",
                "**/*.egg",
                "**/*.bam",
                "**/*.otf",
                "**/*.ttf",
                "**.dll",
                "NPCS/**/*.png",
                "lib/*",
            ],
            "exclude_patterns": [".venv/*", "./dist/*", "./build/*"],
            "rename_paths": {
                EXPORT_DIR: "assets/",
            },
            "console_apps": {
                APP_NAME: MAIN_FILE,
            },
            "plugins": [
                "pandagl",
                "p3openal_audio",
            ],
            "icons": {
                APP_NAME: [
                    "./icons/sanny256.png",
                    "./icons/sanny128.png",
                    "./icons/sanny64.png",
                    "./icons/sanny32.png",
                    "./icons/sanny16.png",
                ],
            },
            "use_optimized_wheels": True,
            "log_filename": "./build/logs/output.log",
        },
    },
    data_files=[
        (
            "lib",
            dll_files,
        ),  # This places DLL, PYD, and DYLIB files in the 'lib/' directory of the build
    ],
)
