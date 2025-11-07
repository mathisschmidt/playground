from nicegui import ui
from nicegui.events import UploadEventArguments

from python_class_viewer.utils.colors import COLORS
from python_class_viewer.services.class_diagram_generator import ClassDiagramGenerator

class HomePage:

    def __init__(self):
        self._diagram_container = None
        self._raw_diagram_container = None
        self._header = None

    def render(self):
        self.header()
        with ui.row().classes('w-full items-center justify-between mb-8'):
            self.upload_section()

        with ui.row().classes('w-full items-center justify-between mb-8'):
            self.diagram_container()
            self.raw_diagram_container()

        return "Welcome to the Home Page!"

    def diagram_container(self):
        if self._diagram_container is None:
            with ui.column().classes('items-center justify-between mb-8'):
                ui.label('Mermaid Diagram:').style(f'color: {COLORS["text_primary"]}; font-weight: 600; font-size: 1.1rem;')
                self._diagram_container = ui.mermaid('graph LR; Start --> Upload;').classes('mermaid-container')
        return self._diagram_container

    def raw_diagram_container(self):
        if self._raw_diagram_container is None:
            with ui.column().classes('items-center justify-between mb-8'):
                ui.label('Raw Mermaid Code:').style(
                    f'color: {COLORS["text_primary"]}; font-weight: 600; font-size: 1.1rem; margin-top: 2rem;')
                self._raw_diagram_container =  ui.code('# Upload a Python file to see the diagram code', language='mermaid').classes('code-container')
        return self._raw_diagram_container

    def header(self):
        if self._header is None:
            self._header = ui.row().classes('w-full')
            with self._header:
                # Header with title
                ui.markdown('# Python Class Diagram Viewer').style(f'color: {COLORS["text_primary"]}; margin: 0;')
                ui.markdown('Upload a Python file to generate a class diagram').style(
                    f'color: {COLORS["text_secondary"]}; margin: 0;')
        return self._header

    async def handle_upload(self, e: UploadEventArguments):
        print(f"Uploaded event: {e}")
        file_content = await e.file.read()
        try:
            diagram_generator = ClassDiagramGenerator(file_content.decode('utf-8'))
            mermaid_diagram = diagram_generator.get_mermaid_diagram()

            self._diagram_container.set_content(mermaid_diagram)
            self._raw_diagram_container.set_content(mermaid_diagram)
            ui.notify('Diagram generated successfully!', color='positive')
        except Exception as ex:
            ui.notify(f'Error: {str(ex)}', color='negative')

    def upload_section(self):
        # Container for upload buttons
        upload_container = ui.element('div').classes('relative').style('width: 128px; height: 48px;')

        with upload_container:
            # Custom upload button
            custom_upload_div = ui.element('div').classes('relative').style('width: 128px; height: 48px;')
            with custom_upload_div:
                print("Creating custom upload button")
                # Upload component that covers the button area
                custom_upload = ui.upload(on_upload=self.handle_upload, auto_upload=True).props('accept=.py')
                custom_upload.set_visibility(False)

                # Custom styled button (visual only, upload handles interaction)
                button = ui.button(on_click=lambda: custom_upload.run_method('pickFiles')).props('flat').classes('upload-button')
                with button:
                    ui.html('''
                                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <line x1="12" y1="5" x2="12" y2="19"></line>
                                    <line x1="5" y1="12" x2="19" y2="12"></line>
                                </svg>
                                ''', sanitize=False).style(f'color: {COLORS["accent"]}')