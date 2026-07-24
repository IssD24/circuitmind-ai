from dataclasses import dataclass
from pathlib import Path
import shutil
import uuid

import patch_ng


@dataclass
class PatchResult:
    success: bool
    workspace_dir: Path
    message: str


def create_workspace(project_path: Path) -> Path:
    project_path = project_path.resolve()
    session_id = uuid.uuid4().hex[:8]

    workspace_root = project_path.parent.parent / ".circuitmind"
    workspace_root.mkdir(exist_ok=True)

    workspace_dir = workspace_root / f"workspace-{session_id}"
    shutil.copytree(project_path, workspace_dir)

    return workspace_dir


def apply_patch_to_workspace(patch_text: str, project_path: Path) -> PatchResult:
    workspace_dir = create_workspace(project_path)

    patch_set = patch_ng.fromstring(patch_text.encode("utf-8"))

    if not patch_set:
        return PatchResult(
            success=False,
            workspace_dir=workspace_dir,
            message="Patch could not be parsed.",
        )

    success = patch_set.apply(root=str(workspace_dir))

    return PatchResult(
        success=success,
        workspace_dir=workspace_dir,
        message="Patch applied." if success else "Patch failed to apply.",
    )