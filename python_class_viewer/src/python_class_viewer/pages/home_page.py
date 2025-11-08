import logging

from nicegui import ui
from nicegui.events import UploadEventArguments

from python_class_viewer.services.database_manager import DatabaseManager
from python_class_viewer.model.upload_info import UploadInfo
from python_class_viewer.utils.colors import COLORS
from python_class_viewer.services.class_diagram_generator import ClassDiagramGenerator

logger = logging.getLogger(__name__)

class HomePage:

    def __init__(self):
        self._mermaid_data = None
        self._raw_diagram_container = None
        self._header = None
        self._uploaded_file: UploadInfo | None = None

    def render(self):
        self.header()
        with ui.row().classes('w-full items-center justify-between mb-8'):
            self.upload_section()
            self.upload_info_card()

        with ui.row().classes('w-full items-center mb-8'):
            self.diagram_container()
            self.raw_diagram_container()

        return "Welcome to the Home Page!"

    def show_mermaid_diagram_dialog(self):
        with ui.dialog() as dialog:
            with ui.card().classes('w-[calc(100vw-2rem)] h-[calc(100vh-2rem)] m-4 p-0'):
                with ui.row().classes('w-full justify-between items-center px-4 py-2 bg-primary/10'):
                    ui.label('Class Diagram').classes('text-2xl font-bold')
                    ui.button('Close', on_click=dialog.close, icon='close').props('flat round')

                # Scrollable container for large diagrams
                with ui.scroll_area().classes('w-full h-[calc(100%-3rem)]'):
                    if self._mermaid_data:
                        ui.mermaid(self._mermaid_data).classes('w-full')
                    else:
                        ui.mermaid('graph LR; Start --> Upload;').classes('w-full')
        dialog.open()

    def show_mermaid_raw_data_dialog(self):
        with ui.dialog() as dialog:
            with ui.card().classes('w-[calc(100vw-2rem)] h-[calc(100vh-2rem)] m-4 p-0'):
                with ui.row().classes('w-full justify-between items-center px-4 py-2 bg-primary/10'):
                    ui.label('Class Diagram').classes('text-2xl font-bold')
                    ui.button('Close', on_click=dialog.close, icon='close').props('flat')

                # Scrollable container for large diagrams
                with ui.scroll_area().classes('w-full h-[calc(100%-3rem)]'):
                    if self._mermaid_data:
                        ui.code(self._mermaid_data).classes('w-full bg-[var(--surface)]')
                    else:
                        ui.code('# Upload a Python file to see the diagram code').classes('w-full bg-[var(--surface)]')
        dialog.open()

    def diagram_container(self):
        with ui.column().classes('items-center justify-between mb-8'):
            ui.label('Mermaid Diagram:').style(f'color: {COLORS["text_primary"]}; font-weight: 600; font-size: 1.1rem;')
            ui.button("Open mermaid diagrams", on_click=self.show_mermaid_diagram_dialog)

    def raw_diagram_container(self):
        with ui.column().classes('items-center justify-between mb-8'):
            ui.label('Raw mermaid data:').style(f'color: {COLORS["text_primary"]}; font-weight: 600; font-size: 1.1rem;')
            ui.button("Open mermaid diagrams", on_click=self.show_mermaid_raw_data_dialog)

    def header(self):
        if self._header is None:
            self._header = ui.row().classes('w-full')
            with (self._header):
                with ui.element("h1").classes("text-3xl font-bold text-center w-full"):
                    ui.label('Python Class Diagram Viewer')
        return self._header

    async def handle_upload(self, e: UploadEventArguments):
        logger.debug(f"Uploaded event: {e}")
        file_content = await e.file.read()
        try:
            # Generate class diagram
            diagram_generator = ClassDiagramGenerator(file_content.decode('utf-8'))
            self._mermaid_data = diagram_generator.get_mermaid_diagram()

            # Analyze file and store upload info
            self._uploaded_file = UploadInfo(
                file_name=e.file.name,
                file_size=len(file_content) / 1024,
                number_class=len(diagram_generator.classes),
                number_relation=sum(len(cls.bases) for cls in diagram_generator.classes),
                number_property=sum(len(cls.attributes) for cls in diagram_generator.classes),
                number_methods=sum(len(cls.methods) for cls in diagram_generator.classes)
            )
            await self.upload_info_card.refresh()
            with DatabaseManager.get_session() as session:
                session.add(self._uploaded_file)
                session.commit()
                logger.debug(f"Uploaded file: {self._uploaded_file.file_name}")

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

    @ui.refreshable
    def upload_info_card(self):
        with ui.card().classes('w-full max-w-md p-4 mt-8 bg-[var(--surface)] border-2 border-[var(--border)] color-[var(--text-primary)]'):
            ui.label('Info about uploaded file').classes('text-lg mb-2 text-center w-full')
            if self._uploaded_file is None:
                ui.label('No file uploaded yet.').classes('color-[var(--text-secondary)] text-center w-full')
            else:
                ui.label('File Name: ' + self._uploaded_file.file_name)
                ui.label(f'File Size: {self._uploaded_file.file_size} KB')
                ui.label(f'Number of Classes: {self._uploaded_file.number_class}')
                ui.label(f'Number of Relationships: {self._uploaded_file.number_relation}')
                ui.label(f'Number of Properties: {self._uploaded_file.number_property}')
                ui.label(f'Number of Methods: {self._uploaded_file.number_methods}')
                ui.label(f'Created At: {self._uploaded_file.created_at}')
