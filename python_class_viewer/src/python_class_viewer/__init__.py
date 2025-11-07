from nicegui import ui
from .router import router

def main():
    router()
    ui.run(port=8080)