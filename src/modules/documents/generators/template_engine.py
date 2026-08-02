import json
from pathlib import Path

class TemplateEngine:
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        
    def populate_template(self, template_name: str, data: dict, output_path: Path):
        """
        Placeholder for template generation.
        In a real scenario, this would use docx-mailmerge or docx-tpl
        to replace tags like {{ project_name }} with actual values.
        """
        # Read mock template text or create a stub document
        text = f"Gerado a partir do template {template_name}\n"
        for k, v in data.items():
            text += f"{k}: {v}\n"
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
            
        return output_path
