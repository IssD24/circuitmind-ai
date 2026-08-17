from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
import uuid

import patch_ng


@dataclass
class PatchApplyResult:
    success: bool
    message: str
    workspace_dir: Path


def create_workspace(project_path: Path) -> Path:
    project_path = project_path.resolve()
    session_id = uuid.uuid4().hex[:8]

    parts = project_path.parts

    if ".circuitmind" in parts:
        circuitmind_index = parts.index(".circuitmind")
        repo_root = Path(*parts[:circuitmind_index])
    else:
        repo_root = project_path.parent.parent

    workspace_root = repo_root / ".circuitmind"
    workspace_root.mkdir(exist_ok=True)

    session_dir = workspace_root / f"workspace-{session_id}"
    session_dir.mkdir()

    workspace_dir = session_dir / project_path.name
    shutil.copytree(project_path, workspace_dir)

    return workspace_dir


def clean_patch_text(patch_text: str, project_name: str) -> str:
    text = patch_text.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    def normalize_patch_path(path: str) -> str:
        path = path.strip().replace("\\", "/")

        if path.startswith("a/") or path.startswith("b/"):
            path = path[2:]

        if project_name in path:
            path = path.split(project_name + "/")[-1]

        return Path(path).name

    cleaned_lines = []

    for line in text.splitlines():
        if line.startswith("diff --git "):
            parts = line.split()
            if len(parts) >= 4:
                old_file = normalize_patch_path(parts[2])
                new_file = normalize_patch_path(parts[3])
                cleaned_lines.append(f"diff --git a/{old_file} b/{new_file}")
            else:
                cleaned_lines.append(line)
            continue

        if line.startswith("--- ") or line.startswith("+++ "):
            prefix = line[:4]
            path = line[4:].strip()

            if path == "/dev/null":
                cleaned_lines.append(line)
                continue

            filename = normalize_patch_path(path)

            if prefix == "--- ":
                cleaned_lines.append(f"--- a/{filename}")
            else:
                cleaned_lines.append(f"+++ b/{filename}")

            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip() + "\n"


def apply_with_git(patch_text: str, workspace_dir: Path) -> tuple[bool, str]:
    patch_file = workspace_dir.parent / "candidate.patch"
    patch_file.write_text(patch_text, encoding="utf-8")

    completed = subprocess.run(
        ["git", "apply", "--recount", "--whitespace=nowarn", str(patch_file)],
        cwd=workspace_dir,
        capture_output=True,
        text=True,
    )

    if completed.returncode == 0:
        return True, "Patch applied with git apply."

    return False, completed.stderr.strip() or completed.stdout.strip()


def apply_with_patch_ng(patch_text: str, workspace_dir: Path) -> tuple[bool, str]:
    patch_set = patch_ng.fromstring(patch_text.encode("utf-8"))

    if not patch_set:
        return False, "Patch could not be parsed."

    applied = patch_set.apply(root=str(workspace_dir))

    if not applied:
        return False, "Patch could not be applied."

    return True, "Patch applied with patch-ng."


def apply_simple_line_replacements(patch_text: str, workspace_dir: Path) -> tuple[bool, str]:
    replacements: list[tuple[str, str]] = []
    deletions: list[str] = []

    pending_old: str | None = None

    for line in patch_text.splitlines():
        if line.startswith("--- ") or line.startswith("+++ "):
            continue

        if line.startswith("@@"):
            if pending_old is not None:
                deletions.append(pending_old)
                pending_old = None
            continue

        if line.startswith("-") and not line.startswith("---"):
            if pending_old is not None:
                deletions.append(pending_old)

            pending_old = line[1:]
            continue

        if line.startswith("+") and not line.startswith("+++") and pending_old is not None:
            replacements.append((pending_old, line[1:]))
            pending_old = None
            continue

        if pending_old is not None:
            deletions.append(pending_old)
            pending_old = None

    if pending_old is not None:
        deletions.append(pending_old)

    if not replacements and not deletions:
        return False, "No simple line replacements or deletions found."

    candidate_files = []
    for suffix in ("*.ino", "*.cpp", "*.h", "*.hpp", "*.c"):
        candidate_files.extend(workspace_dir.rglob(suffix))

    changed = False

    for file_path in candidate_files:
        text = file_path.read_text(encoding="utf-8")

        for old_line, new_line in replacements:
            if old_line in text:
                text = text.replace(old_line, new_line, 1)
                changed = True

        for old_line in deletions:
            line_with_newline = old_line + "\n"

            if line_with_newline in text:
                text = text.replace(line_with_newline, "", 1)
                changed = True
            elif old_line in text:
                text = text.replace(old_line, "", 1)
                changed = True

        if changed:
            file_path.write_text(text, encoding="utf-8")
            return True, "Patch applied with simple replacement/deletion fallback."

    return False, "Simple fallback could not find matching source lines."


def apply_patch_to_workspace(patch_text: str, project_path: Path) -> PatchApplyResult:
    workspace_dir = create_workspace(project_path)
    cleaned_patch = clean_patch_text(patch_text, project_path.name)

    git_success, git_message = apply_with_git(cleaned_patch, workspace_dir)

    if git_success:
        return PatchApplyResult(True, git_message, workspace_dir)

    fallback_success, fallback_message = apply_simple_line_replacements(
        cleaned_patch,
        workspace_dir,
    )

    if fallback_success:
        return PatchApplyResult(True, fallback_message, workspace_dir)

    patch_ng_success, patch_ng_message = apply_with_patch_ng(
        cleaned_patch,
        workspace_dir,
    )

    if patch_ng_success:
        return PatchApplyResult(True, patch_ng_message, workspace_dir)

    return PatchApplyResult(
        False,
        (
            "Patch could not be applied. "
            f"git apply: {git_message}; "
            f"fallback: {fallback_message}; "
            f"patch-ng: {patch_ng_message}"
        ),
        workspace_dir,
    )