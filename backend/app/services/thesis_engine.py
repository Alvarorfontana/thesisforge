from app.core.prompts import META_PROMPT
from app.models.schemas import ThesisRef

def build_prompt(topic: str, module: str, ideas: str, references: list[ThesisRef]) -> str:
    blocks = []
    for ref in references[:8]:
        blocks.append(
            f"<tesis origen='{ref.origin}' fuente='{ref.source}' institucion='{ref.institution}' anio='{ref.year}'>\n"
            f"Titulo: {ref.title}\nAutores: {ref.authors}\nResumen: {ref.abstract}\n</tesis>")
    return (META_PROMPT
            .replace("{{TESIS}}", "\n".join(blocks))
            .replace("{{MODULO}}", module)
            .replace("{{TEMA}}", topic)
            .replace("{{IDEAS}}", ideas or "N/A"))
