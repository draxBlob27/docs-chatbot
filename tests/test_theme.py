from backend.app.services.summarizer import generate_themes
from backend.app.services.summarizer import ThemeGroup


def test_generate_themes_structure():
    test_chunks = [
        {
            "text": "The tribunal found delay in disclosure.",
            "citation": "sample.pdf – Page 1 – Para 2 – Sentence 1"
        }
    ]
    themes = generate_themes(test_chunks)
    assert isinstance(themes, list)
    assert isinstance(themes[0], ThemeGroup)
    assert "theme" in themes[0].model_dump()
