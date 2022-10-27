@echo off

call %~dp0atika_bot\env\Scripts\activate

cd %~dp0atika_bot

set TOKEN=5665037280:AAHElxy6focqao7Rux_MFBlbgCoac0KQ05I

python bot_telegram.py

pause