import sys

from pathlib import Path


class PythonPath():
    def __init__(self, path: Path):
        self.path = path

    def __enter__(self):
        sys.path.insert(0, self.path)

    def __exit__(self, exc_type, exc_value, traceback):
        sys.path.remove(self.path)

with PythonPath(Path(__file__).absolute().parents[1]):
    from src import Game
    game = Game()
    game.run()
