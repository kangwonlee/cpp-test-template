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
1. Edit `tests/test_build.py` if you need to customize build checks.
1. Customize `tests/test_dynamic.c` and `tests/test_dynamic.py` to define the expected test cases.
1. Push to GitHub : `build-image.yml` builds your image and pushes to GHCR (GitHub Container Registry).
* `src_file_path`, `obj_file_path`, and `my_src_folder` fixtures will be available if your test script in the `tests/` folder imports `pytest` (see `conftest.py`).
* Currently `requirements.txt` is for documentation purpose. If you want to install additional Python packages, add them to `requirements.txt` and uncomment the `COPY` and `RUN` lines in the `Dockerfile`.

## CI/CD Workflow

- `build-image.yml`: Builds and pushes a multi-arch grader image to GHCR.
- Uses GHCR for privacy and GitHub integration—swap to Docker Hub by updating `registry` and `tags` if preferred.
- Requires `Dockerfile` in repo root.

## Dockerfile

- Builds a lightweight grader image with `pytest`.
- Currently `requirements.txt` is for documentation purpose only.
  + If you want to install additional python packages:
    + add them to `requirements.txt`,
    + and uncomment the `COPY` and `RUN` lines in the `Dockerfile`.
    + Please test whether `python` can import the packages you added.
- Customize `CMD` to run your tests (e.g., `python3 -m pytest tests/`).

## Instructor Setup — Detailed Guide

### How This Repo Fits in the Grading Pipeline

This is the **grader template** — the instructor-facing half of a two-repo pattern:

1. **This repo** (grader) — you customize the test files, push, and GitHub Actions builds a Docker image containing your tests. The image is published to GHCR.
2. **[cpp-hw-template](https://github.com/kangwonlee/cpp-hw-template)** (student-facing) — contains `src/main.c`, `include/main.h`, and a `classroom.yml` workflow. When a student pushes, `classroom.yml` pulls your grader image and runs the tests.

### GitHub Permissions

This repo uses `secrets.GITHUB_TOKEN` (automatically provided by GitHub Actions) to:
- Log in to GHCR and **push** the grader Docker image
- Pass as `GIT_AUTH_TOKEN` during Docker build for cloning dependencies

No manual token setup is needed, but you must enable write access:

> **Settings > Actions > General > Workflow permissions > "Read and write permissions"**

Without this, the Docker image push will fail with a 403 error.

### Files to Customize Per Assignment

| File | What to Change |
|:-----|:---------------|
| `tests/test_build.py` | Usually no changes needed (checks if student code compiles) |
| `tests/test_style.py` | Usually no changes needed (checks clang-format style) |
| `tests/test_commit_msg.py` | Usually no changes needed (validates commit message quality) |
| `tests/test_dynamic.py` | Customize to define which C test functions to run |
| `tests/test_dynamic.c` | Write the actual C test cases for the assignment |
| `CMakeLists.txt` | Update if the assignment uses different source file names |
| `tests/conftest.py` | Usually no changes needed (provides path fixtures) |

### Connecting to the Homework Template

After your grader image builds (check the Actions tab), note the image URL:

```
ghcr.io/{your-username}/{this-repo-name}:latest
```

In the student homework repository, set this as a **repository variable**:

> **Settings > Secrets and variables > Actions > Variables**

Variable name: `CPP_GRADER_???` (replace `???` with the assignment identifier, e.g., `CPP_GRADER_201`)
Value: `ghcr.io/{your-username}/{this-repo-name}:latest`

### Required Secrets in the Homework Repo (not this repo)

The following secrets are set on the **homework template** side (or as organization secrets):

#### `CR_PAT` (required)

A GitHub fine-grained Personal Access Token that allows the homework repo's workflow to **pull** the grader image from GHCR.

1. Go to **GitHub > Settings (user) > Developer settings > Personal access tokens > Fine-grained tokens**.
2. Click **Generate new token**.
3. Set the following permission:

| Permission | Access | Purpose |
|:----------:|:------:|:--------|
| Packages   | Read   | Pull grader Docker images from GHCR |

4. Save as a secret named `CR_PAT` in the homework repo or organization.

> `GITHUB_TOKEN` cannot be used for this because it is scoped to the current repo and cannot read packages from a different repo.

#### LLM API Keys (at least one required)

These power the AI tutor feedback step in the homework repo. At least one must be set.

| Secret Name | Service | Where to Obtain |
|:-----------:|:-------:|:----------------|
| `CLAUDE_API_KEY` | Anthropic Claude | https://console.anthropic.com/ |
| `GOOGLE_API_KEY` | Google Gemini | https://aistudio.google.com/ |
| `XAI_API_KEY` | xAI Grok | https://console.x.ai/ |
| `NVIDIA_NIM_API_KEY` | NVIDIA NIM | https://build.nvidia.com/ |
| `PERPLEXITY_API_KEY` | Perplexity | https://perplexity.ai/settings/api |

#### `DEFAULT_MODEL` (optional)

Specifies the preferred LLM model. If unset, the AI tutor defaults to Gemini or uses whichever single key is available.

## Notes

- Copyright © 2025 Kangwon Lee. Registered at the Korea Copyright Commission under #C-2025-027967 (as one of derivative works from original registration #C-2025-016393).
- Various LLMs and AI tools helped implementing the templates for this assignment.
  - Google Gemini Flash / Pro 2.5
  - xAI Grok3
  - Perplexity Sonar
  - Claude.ai 4.0 Sonnet
