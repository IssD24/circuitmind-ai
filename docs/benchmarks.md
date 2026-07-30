# CircuitMind Benchmarks

| ID | Name | Failure Type | Expected Fix | Status |
|---|---|---|---|---|
| 01 | missing semicolon | syntax error | add semicolon | tested |
| 02 | wrong Wire signature | API/signature error | adjust call | tested |
| 03 | missing include | missing header/library | add include or explain dependency | tested |
| 04 | wrong API | typo/API misuse | `Serial.printline` → `Serial.println` | added/tested |
| 05 | missing include | missing standard header | add `#include <vector>` | added/tested |
| 06 | missing library | missing third-party dependency | explain/install ArduinoJson library | added; missing library error parsed |

## Notes

Benchmarks 01–05 are intended to test source-level fixes.

Benchmark 06 may require installing a missing third-party Arduino library rather than editing source code. CircuitMind should eventually recognize this as an environment/dependency issue.

## Compiler vs Logic Benchmarks

Some benchmarks fail at compile time and can be detected from Arduino CLI diagnostics.

Other benchmarks may compile successfully but still represent common firmware bugs. These require static rules, prompt-based source review, or benchmark metadata.