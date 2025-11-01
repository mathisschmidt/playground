from nicegui import ui
import ast
from pathlib import Path

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
        status_label.classes('text-green-600')
    except Exception as ex:
        status_label.text = f'Error: {str(ex)}'
        status_label.classes('text-red-600')

@ui.page('/')
def main():
    ui.markdown('# Python Class Diagram Viewer')
    ui.markdown('Upload a Python file to generate a class diagram')
    
    ui.upload(on_upload=handle_upload, auto_upload=True).props('accept=.py')
    
    global status_label
    status_label = ui.label('Upload a file to begin')
    
    global diagram_container, raw_diagram_container
    raw_diagram_container = ui.code('raw diagram, for now nothing to show', language='mermaid')
    diagram_container = ui.mermaid('graph LR; Start --> Upload;')


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(port=8080)
