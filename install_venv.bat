python -m pip install --upgrade pip
python -m venv venv
call %~dp0\venv\Scripts\activate
cd ../..
python -m pip install --upgrade pip
pip install -r libs.txt
pause
