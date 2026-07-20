from dataclasses import dataclass
from typing import Optional


@dataclass
class BuildResult:
    command: list[str]
    exit_code: int
    stdout: str
    stderr: str


@dataclass
class Diagnostic:
    file: Optional[str]
    line: Optional[int]
    column: Optional[int]
    severity: str
    message: str
    raw: str

@dataclass
class DiagnosisResult:
    diagnosis: str
    root_cause: str
    confidence: float
    patch: str
    raw_response: Optional[str] = None