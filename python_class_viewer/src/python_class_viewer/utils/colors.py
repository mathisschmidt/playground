# Color configuration for the application
# Dark theme color palette

COLORS = {
    # Primary colors
    'primary': '#1e1e2e',  # Dark blue-gray
    'secondary': '#313244',  # Lighter dark blue-gray
    'accent': '#89b4fa',  # Light blue

    # Background colors
    'background': '#11111b',  # Very dark background
    'surface': '#1e1e2e',  # Card/surface background
    'elevated': '#313244',  # Elevated elements

    # Text colors
    'text_primary': '#cdd6f4',  # Light gray text
    'text_secondary': '#a6adc8',  # Muted text
    'text_muted': '#6c7086',  # Very muted text

    # Status colors
    'success': '#a6e3a1',  # Green
    'error': '#f38ba8',  # Red
    'warning': '#f9e2af',  # Yellow
    'info': '#89dceb',  # Cyan

    # Border colors
    'border': '#313244',  # Subtle border
    'border_focus': '#89b4fa',  # Focused border
}


def get_css():
    """Generate CSS for the color scheme"""
    return f"""
    <style>
        :root {{
            --primary: {COLORS['primary']};
            --secondary: {COLORS['secondary']};
            --accent: {COLORS['accent']};
            --background: {COLORS['background']};
            --surface: {COLORS['surface']};
            --elevated: {COLORS['elevated']};
            --text-primary: {COLORS['text_primary']};
            --text-secondary: {COLORS['text_secondary']};
            --text-muted: {COLORS['text_muted']};
            --success: {COLORS['success']};
            --error: {COLORS['error']};
            --border: {COLORS['border']};
            --border-focus: {COLORS['border_focus']};
        }}

        body {{
            background-color: var(--background) !important;
            color: var(--text-primary) !important;
        }}

        .q-page {{
            background-color: var(--background) !important;
        }}

        .upload-button {{
            width: 128px;
            height: 48px;
            background-color: var(--surface);
            border: 2px solid var(--border);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .upload-button:hover {{
            background-color: var(--elevated);
            border-color: var(--accent);
            transform: translateY(-2px);
        }}

        .normal-upload {{
            background-color: var(--surface) !important;
            border: 2px solid var(--border) !important;
            border-radius: 8px !important;
        }}

        .normal-upload:hover {{
            border-color: var(--accent) !important;
        }}

        .q-toggle__thumb {{
            background-color: var(--accent) !important;
        }}

        .border-accent {{
            border-color: var(--accent) !important;
            background-color: var(--elevated) !important;
        }}

        .border-border {{
            border-color: var(--border) !important;
        }}

        .upload-button svg {{
            transition: transform 0.3s ease;
        }}

        .upload-button:hover svg {{
            transform: scale(1.1);
        }}

        .status-success {{
            color: var(--success) !important;
        }}

        .status-error {{
            color: var(--error) !important;
        }}

        .code-container {{
            background-color: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
        }}
    </style>
    """