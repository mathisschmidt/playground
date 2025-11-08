I don't know why but the only way to run it. 
`uv run src/python_class_viewer/__main__.py`

Things interesting to check:
- how we handle logs
- How we handle the environment variables

# Things to check and maybe to implement

## How to use NiceGUI's built-in theming
NiceGUI uses Quasar's color system. Here are the main ways to use built-in theming:

**1. Using Quasar color classes:**
```python
ui.element('div').classes('bg-primary text-white')  # Primary background
ui.element('div').classes('bg-secondary text-white')  # Secondary background
ui.element('div').classes('bg-accent')  # Accent color
ui.element('div').classes('bg-positive')  # Success/positive (green)
ui.element('div').classes('bg-negative')  # Error/negative (red)
ui.element('div').classes('bg-warning')  # Warning (orange/yellow)
ui.element('div').classes('bg-info')  # Info (blue)
ui.element('div').classes('bg-dark')  # Dark background
```

**2. Setting custom colors:**
```python
ui.colors(
    primary='#5898d4',
    secondary='#26a69a',
    accent='#9c27b0',
    dark='#1d1d1d',
    positive='#21ba45',
    negative='#c10015',
    info='#31ccec',
    warning='#f2c037'
)
```

**3. Using dark mode:**
```python
ui.dark_mode().enable()  # Enable dark mode
# or
ui.dark_mode().disable()  # Disable dark mode
# or
ui.dark_mode()  # Auto (follows system preference)
```

**4. Accessing Quasar color variables in styles:**
```python
ui.element('div').style('background-color: var(--q-primary); color: var(--q-dark)')
```

The Quasar colors automatically adapt to dark mode, so using these built-in color classes is recommended for a consistent themed experience.