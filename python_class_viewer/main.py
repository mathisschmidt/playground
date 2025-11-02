from nicegui import ui
from colors import COLORS, get_css
from src.pages.home_page import HomePage


@ui.page('/')
def main():
    # Add custom CSS
    ui.add_head_html(get_css())

    home_page = HomePage()
    home_page.render()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(port=8080)