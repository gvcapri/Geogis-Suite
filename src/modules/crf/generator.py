class DocumentGenerator:
    """
    Template Engine for generating CRF PDF documents.
    """
    def __init__(self, repository):
        self.repository = repository
        
    def generate_draft(self, template_id: int, project_data: dict) -> str:
        """
        Replaces {{Vars}} with real data and generates a mock PDF/HTML path.
        """
        # Mock HTML replacement
        template_text = "Certifico que o projeto {{NomeProjeto}} pertencente a {{Cliente}}..."
        
        output = template_text
        for key, val in project_data.items():
            output = output.replace(f"{{{{{key}}}}}", str(val))
            
        return output
