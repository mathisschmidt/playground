from nicegui import ui
import ast
from pathlib import Path
from colors import COLORS, get_css


class ClassDiagramGenerator:
    def __init__(self):
        self.classes = []

    def format_type_annotation(self, annotation: str) -> str:
        # Replace square brackets with tildes for generic types
        import re
        # Handle Optional[Type] -> Optional~Type~
        annotation = re.sub(r'Optional\[(.*?)\]', r'Optional~\1~', annotation)
        # Handle List[Type] -> List~Type~
        annotation = re.sub(r'List\[(.*?)\]', r'List~\1~', annotation)
        return annotation

    def parse_file(self, file_content: str) -> str:
        self.classes = []
        tree = ast.parse(file_content)

        # Visit all nodes and extract class information
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'bases': [base.id for base in node.bases if isinstance(base, ast.Name)],
                    'methods': [],
                    'attributes': []
                }

                for child in node.body:
                    if isinstance(child, ast.FunctionDef):
                        # Format method without parameters for cleaner diagram
                        method = f'{child.name}()'
                        class_info['methods'].append(method)
                    elif isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
                        attr_type = ast.unparse(child.annotation) if child.annotation else 'Any'
                        attr_type = self.format_type_annotation(attr_type)
                        class_info['attributes'].append(f'{child.target.id}: {attr_type}')

                self.classes.append(class_info)

        return self.generate_mermaid()

    def generate_mermaid(self) -> str:
        mermaid_code = ['classDiagram']

        # Add class definitions
        for class_info in self.classes:
            # Class declaration
            mermaid_code.append(f'class {class_info["name"]} {{')

            # Attributes
            for attr in class_info['attributes']:
                mermaid_code.append(f'    +{attr}')

            # Methods
            for method in class_info['methods']:
                mermaid_code.append(f'    +{method}')

            mermaid_code.append('}')

            # Inheritance relationships
            for base in class_info['bases']:
                mermaid_code.append(f'{base} <|-- {class_info["name"]}')

        return '\n'.join(mermaid_code)


# Initialize the diagram generator
diagram_generator = ClassDiagramGenerator()


async def handle_upload(e):
    print(f"Uploaded event: {e}")
    file_content = await e.file.read()
    try:
        mermaid_diagram = diagram_generator.parse_file(file_content.decode('utf-8'))
        diagram_container.set_content(mermaid_diagram)
        raw_diagram_container.set_content(mermaid_diagram)
        status_label.text = 'Diagram generated successfully!'
        status_label.classes('status-success', remove='status-error')
    except Exception as ex:
        status_label.text = f'Error: {str(ex)}'
        status_label.classes('status-error', remove='status-success')


@ui.page('/')
def main():
    # Add custom CSS
    ui.add_head_html(get_css())

    # Header with title and upload button
    with ui.row().classes('w-full items-center justify-between mb-8'):
        with ui.column().classes('gap-1'):
            ui.markdown('# Python Class Diagram Viewer').style(f'color: {COLORS["text_primary"]}; margin: 0;')
            ui.markdown('Upload a Python file to generate a class diagram').style(
                f'color: {COLORS["text_secondary"]}; margin: 0;')

        # Custom upload button with SVG icon
        with ui.element('div').classes('relative'):
            # Hidden file upload
            upload = ui.upload(on_upload=handle_upload, auto_upload=True).props('accept=.py')
            upload.classes('hidden')

            # Custom styled button
            with ui.button(on_click=lambda: upload.run_method('pickFiles')).props('flat').classes('upload-button'):
                ui.html('''
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                ''', sanitize=False).style(f'color: {COLORS["accent"]}')

        upload2 = ui.upload(on_upload=handle_upload, auto_upload=True).props('accept=.py')
        with upload2:
            ui.button('Upload Python File')
    # Status label
    global status_label
    status_label = ui.label('Upload a file to begin').style(f'color: {COLORS["text_muted"]}; margin-bottom: 1rem;')

    # Diagram containers
    with ui.column().classes('w-full gap-4'):
        ui.label('Mermaid Diagram:').style(f'color: {COLORS["text_primary"]}; font-weight: 600; font-size: 1.1rem;')
        global diagram_container
        diagram_container = ui.mermaid('graph LR; Start --> Upload;').classes('mermaid-container')

        ui.label('Raw Mermaid Code:').style(
            f'color: {COLORS["text_primary"]}; font-weight: 600; font-size: 1.1rem; margin-top: 2rem;')
        global raw_diagram_container
        raw_diagram_container = ui.code('# Upload a Python file to see the diagram code', language='mermaid').classes(
            'code-container')


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(port=8080)