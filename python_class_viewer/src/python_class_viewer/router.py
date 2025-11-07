from nicegui import ui
from .utils.colors import get_css
from .pages.home_page import HomePage

def router():
    @ui.page('/')
    def home_page():
        ui.add_head_html(get_css())
        HomePage().render()