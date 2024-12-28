@echo off


REM Create the src directory and subdirectories
mkdir src
cd src
mkdir core
mkdir gui
mkdir utils

REM Create the __init__.py files
copy nul __init__.py
cd core
copy nul __init__.py
copy nul combination_reducer.py
copy nul validator.py
cd ..\gui
copy nul __init__.py
copy nul main_window.py
copy nul components.py
cd ..\utils
copy nul __init__.py
copy nul config.py
cd ..\..

REM Create the tests directory and files
mkdir tests
cd tests
copy nul __init__.py
copy nul test_combination_reducer.py
copy nul test_validator.py
cd ..

REM Create the main.py file
copy nul main.py

REM Finish
echo Directory structure created successfully!