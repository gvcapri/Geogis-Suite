from pathlib import Path

class FileValidator:
    @staticmethod
    def validate_excel(path: Path) -> bool:
        return path.is_file() and path.suffix in [".xlsx", ".xls"]
        
    @staticmethod
    def validate_word(path: Path) -> bool:
        return path.is_file() and path.suffix in [".docx", ".doc"]
        
    @staticmethod
    def validate_pdf(path: Path) -> bool:
        return path.is_file() and path.suffix == ".pdf"
