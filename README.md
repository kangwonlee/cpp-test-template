# cpp-pytest-template

Template for grader image builders for c/c++ assignments

## Purpose

* To provide a template for creating a grader image for c/c++ assignments
* To automate the programming assignment grading process so that educators can focus more on teaching

## Setup & Customization
1. Fork this repository.
1. Go to the `Settings` tab of your repository and click on `Actions` on the left sidebar.
    1. Click on `General` and go to `Workflow permissions`.
    1. Choose `Read and write permissions` and <kbd>Save</kbd>.
1. Edit `tests/test_syntax.py` to set allowed modules and functions.
1. Customize `tests/test_results.py` to define the expected results.
1. Push to GitHub : `build.yml` builds your image and pushes to GHCR (GitHub Container Repository).
* `script_path` fixture will be available if your test script in the `tests/` folder imports `pytest`.
* Currently `requirements.txt` is for documentation purpose.

## CI/CD Workflow

- `build.yml`: Builds and pushes a multi-arch grader image to GHCR.
- Uses GHCR for privacy and GitHub integration—swap to Docker Hub by updating `registry` and `tags` if preferred.
- Requires `Dockerfile` in repo root (see [Dockerfile docs](#)). Set `BUILDER_PAT` in secrets for optional dispatch.

## Dockerfile

- Builds a lightweight grader image with `pytest`.
- Currently `requirements.txt` is for documentation purpose only.
  + If you want to install additional python packages:
    + add them to `requirements.txt`,
    + and uncomment the `COPY` and `RUN` lines in the `Dockerfile`.
    + Please test whether `python` can import the packages you added.
- Customize `CMD` to run your tests (e.g., `python3 -m pytest tests/`).

## Notes

- Copyright © 2025 Kangwon Lee. Registered at the Korea Copyright Commission under #C-2025-027967 (as one of derivative works from original registration #C-2025-016393).
- Various LLMs and AI tools helped implemeting the templates for this assignment.
  - Google Gemini Flash / Pro 2.5
  - xAI Grok3
  - Perplexity Sonar
  - Claude.ai 4.0 Sonnet
