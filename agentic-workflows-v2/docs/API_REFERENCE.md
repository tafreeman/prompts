## API Reference (auto-generated)

This project uses docstrings to generate API reference documentation. The recommended tooling is Sphinx (with autodoc) or MkDocs with mkdocstrings. Below are minimal setup notes so maintainers can generate docs.

Sphinx (recommended):

- Install: `pip install sphinx sphinx-autodoc-typehints myst-parser`
- Quick init (from repo root):

```bash
python -m sphinx.cmd.quickstart docs/_build/sphinx -q -p "agentic_v2" -a "Team" --ext-autodoc --makefile
```

- In `docs/conf.py` enable:

  - `sphinx.ext.autodoc`
  - `sphinx.ext.napoleon`
  - `sphinx_autodoc_typehints`
  - `myst_parser` for markdown support

- Add an `api` to `docs/index.rst` or `docs/index.md` that runs `.. automodule:: agentic_v2` or per-package modules.

MkDocs alternative:

- Install: `pip install mkdocs mkdocstrings mkdocs-material`
- Configure `mkdocs.yml` with `plugins: - mkdocstrings.handlers.python` and point to `src/` packages.

CI / Local invocation examples:

```bash
# Build Sphinx
sphinx-build -b html docs docs/_build/html
# or build MkDocs
mkdocs build -f mkdocs.yml -d site/
```

Include the generated HTML in release artifacts or publish via GitHub Pages.
