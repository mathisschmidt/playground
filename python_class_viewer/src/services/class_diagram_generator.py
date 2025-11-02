import ast
from dataclasses import dataclass


@dataclass
class ClassInfo:
    name: str
    bases: list[str]
    methods: list[str]
    attributes: list[str]


class ClassDiagramGenerator:
    def __init__(self, file_content: str):
        self.classes: list[ClassInfo] = []
        self._parse_file(file_content)

    def _parse_file(self, file_content: str) -> None:
        self.classes = []
        tree = ast.parse(file_content)

        # Visit all nodes and extract class information
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = []
                attributes = []

                for child in node.body:
                    if isinstance(child, ast.FunctionDef):
                        # Format method without parameters for cleaner diagram
                        method = f'{child.name}()'
                        methods.append(method)
                    elif isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
                        attr_type = ast.unparse(child.annotation) if child.annotation else 'Any'
                        attr_type = self.format_type_annotation(attr_type)
                        attributes.append(f'{child.target.id}: {attr_type}')

                self.classes.append(ClassInfo(
                    name=node.name,
                    bases=[base.id for base in node.bases if isinstance(base, ast.Name)],
                    methods=methods,
                    attributes=attributes
                ))

    def get_mermaid_diagram(self) -> str:
        mermaid_code = ['classDiagram']

        # Add class definitions
        for class_info in self.classes:
            # Class declaration
            mermaid_code.append(f'class {class_info.name} {{')

            # Attributes
            for attr in class_info.attributes:
                mermaid_code.append(f'    +{attr}')

            # Methods
            for method in class_info.methods:
                mermaid_code.append(f'    +{method}')

            mermaid_code.append('}')

            # Inheritance relationships
            for base in class_info.bases:
                mermaid_code.append(f'{base} <|-- {class_info.name}')

        return '\n'.join(mermaid_code)

    @staticmethod
    def format_type_annotation(annotation: str) -> str:
        # Replace square brackets with tildes for generic types
        import re
        # Handle Optional[Type] -> Optional~Type~
        annotation = re.sub(r'Optional\[(.*?)\]', r'Optional~\1~', annotation)
        # Handle List[Type] -> List~Type~
        annotation = re.sub(r'List\[(.*?)\]', r'List~\1~', annotation)
        return annotation