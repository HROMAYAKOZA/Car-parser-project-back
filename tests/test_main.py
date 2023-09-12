import os
print(os.getcwd())
from src.main import main_f

def test_hello_world(capsys):
    main_f()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello, World!\nThis is stable branch bersion"