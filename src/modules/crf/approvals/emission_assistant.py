class EmissionAssistantService:
    def __init__(self, crf_repository):
        self.crf_repo = crf_repository
        
    def analyze(self, process_id: int) -> dict:
        """
        Cross-checks Territorial, Environmental, and Comparisons modules.
        Returns a diagnostic dictionary.
        """
        # Mock diagnosis
        return {
            "score": 82,
            "items": [
                {"text": "Cadastro Territorial concluído", "status": "ok"},
                {"text": "Comparativos aprovados", "status": "ok"},
                {"text": "Documentação anexada", "status": "ok"},
                {"text": "Memorial preenchido", "status": "ok"},
                {"text": "Licença ambiental vence em 15 dias", "status": "warning"},
                {"text": "Revisão técnica pendente", "status": "error"},
                {"text": "Aprovação do gestor pendente", "status": "error"}
            ],
            "next_action": "Enviar o processo para Revisão Técnica."
        }
