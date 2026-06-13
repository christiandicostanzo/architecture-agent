import os
import yaml


PROMPTS_DIR = os.path.dirname(__file__)


def _parse_markdown(path: str) -> dict:
    """Parse a markdown file with optional YAML front matter.

    Returns a dict where 'content' is the markdown body and all front matter
    keys are merged at the top level.
    """
    with open(path) as f:
        raw = f.read()

    if raw.startswith("---"):
        _, front, body = raw.split("---", 2)
        data = yaml.safe_load(front) or {}
        data["content"] = body.strip()
    else:
        data = {"content": raw.strip()}

    return data


def _resolve_file(prompt_dir: str, version: int | None) -> str:
    """Return the path to the best matching version file (.md preferred over .yaml)."""
    all_files = os.listdir(prompt_dir)

    def version_files(ext: str) -> list[str]:
        return sorted(f for f in all_files if f.startswith("v") and f.endswith(ext))

    md_files = version_files(".md")
    yaml_files = version_files(".yaml")

    if not md_files and not yaml_files:
        raise FileNotFoundError(f"No version files found in '{prompt_dir}'")

    if version is not None:
        for ext, candidates in ((".md", md_files), (".yaml", yaml_files)):
            filename = f"v{version}{ext}"
            if filename in candidates:
                return os.path.join(prompt_dir, filename)
        raise FileNotFoundError(
            f"Version {version} not found in '{prompt_dir}' (.md or .yaml)"
        )

    # Latest version: prefer .md, fall back to .yaml
    latest_md = md_files[-1] if md_files else None
    latest_yaml = yaml_files[-1] if yaml_files else None

    if latest_md and latest_yaml:
        # Compare version numbers; prefer .md when tied
        md_ver = int(latest_md[1:-3])
        yaml_ver = int(latest_yaml[1:-5])
        filename = latest_md if md_ver >= yaml_ver else latest_yaml
    else:
        filename = latest_md or latest_yaml

    return os.path.join(prompt_dir, filename)


def load_prompt(name: str, version: int | None = None) -> dict:
    """
    Load a prompt by name and optional version.

    Args:
        name:    Prompt name as a path relative to the prompts/ directory,
                 e.g. "weather_agent" or "llm_tests/correctness".
        version: Specific version number to load. Defaults to the latest version.

    Returns:
        Parsed prompt as a dict with at least a 'content' key.
        YAML files are parsed directly; markdown files have their front matter
        merged into the dict and the body stored under 'content'.
    """
    prompt_dir = os.path.join(PROMPTS_DIR, name)

    if not os.path.isdir(prompt_dir):
        raise FileNotFoundError(f"No prompt directory found for '{name}'")

    path = _resolve_file(prompt_dir, version)

    if path.endswith(".md"):
        return _parse_markdown(path)

    with open(path) as f:
        data = yaml.safe_load(f)

    # Normalise: for YAML prompts the body lives under 'content'
    if "content" not in data:
        raise KeyError(f"YAML prompt '{path}' is missing a 'content' key")

    return data


def get_prompt_content(name: str, version: int | None = None) -> str:
    """Shortcut to load just the prompt body (the 'content' field)."""
    return load_prompt(name, version)["content"]
