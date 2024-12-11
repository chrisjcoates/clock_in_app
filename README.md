# SEM1 PERSONAL PROJECT
UClan Sem1 Programming Personal project

Employee Clock-in / Clock-out application

## Dependencys

- Python3.12
- Kivy (only works with python3.12)

## Info
- App doesn't scale well on Windows for some reason, scales perfect on mac and android.
- Scaled it best I could to run on windows, but widgets will appear larger than intented. (tested at 1920x1980 on windows)
- The code for making the app open to full screen height won't work on windows also for smoe reason, so manual resize is needed. (again works perfect on mac and android)
- Tabbing between controls is not enabled as app is design for touch screen device.

## To run
- Create a virtual environment with python 3.12 'python3.12 -m venv venv' on mac | 'py -3.12 -m venv venv' on windows
- To activate 'source venv/bin/activate' on mac | venv\Scripts\activate' on windows
- Install Kivy 'pip install kivy'
- Run main.py to execute program

- Passcode for creating employees is 1234