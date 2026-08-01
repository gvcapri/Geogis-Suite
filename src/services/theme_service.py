class ThemeManager:
    def __init__(self):
        self.themes = {
            'light': {'primary': '#3498db', 'background': '#f5f6fa', 'text': '#2f3640'},
            'dark': {'primary': '#2980b9', 'background': '#2f3640', 'text': '#f5f6fa'},
            'corporate': {'primary': '#2c3e50', 'background': '#ecf0f1', 'text': '#2c3e50'},
        }
        self.current_theme = 'corporate'
    
    def get_style(self):
        return f"QWidget {{ background-color: {self.themes[self.current_theme]['background']}; color: {self.themes[self.current_theme]['text']}; }}"
