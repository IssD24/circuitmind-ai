# CircuitMind Benchmarks

| ID | Name | Failure Type | Expected Fix | Status |
|---|---|---|---|---|
| 01 | missing semicolon | syntax error | add semicolon | tested |
| 02 | wrong Wire signature | API/signature error | adjust call | tested |
| 03 | missing include | missing header/library | add include or explain dependency | tested |
| 04 | wrong API | typo/API misuse | `Serial.printline` → `Serial.println` | added/tested |
| 05 | missing include | missing standard header | add `#include <vector>` | added/tested |
| 06 | missing library | missing third-party dependency | explain/install ArduinoJson library | added; missing library error parsed |
| 07 | incorrect pin | logic/static issue | `-1` → `LED_BUILTIN` | added; may compile |
| 08 | wrong function signature | function call error | pass `LED_BUILTIN` | added/tested |

## Notes

Benchmarks 01–05 are intended to test source-level fixes.

Benchmark 06 may require installing a missing third-party Arduino library rather than editing source code. CircuitMind should eventually recognize this as an environment/dependency issue.

Benchmark 07 is a logic/static-analysis case. It may compile successfully because the compiler does not know that `-1` is an invalid practical output pin.

Benchmark 08 is a compiler-error case because `blinkLed` is called without the required argument.

## Compiler vs Logic Benchmarks

Some benchmarks fail at compile time and can be detected from Arduino CLI diagnostics.

Other benchmarks may compile successfully but still represent common firmware bugs. These require static rules, prompt-based source review, or benchmark metadata.