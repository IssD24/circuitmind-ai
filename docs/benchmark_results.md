# CircuitMind Benchmark Results

| Benchmark | Type | Before | Fix Result | Status | Notes |
|---|---|---|---|---|---|
| broken_01_missing_semicolon | compiler | fail | not fixed | ok | LLM unavailable due to Anthropic credits |
| broken_02_wrong_wire_signature | compiler | fail | not fixed | ok | LLM unavailable due to Anthropic credits |
| broken_03_missing_include | compiler | fail | not fixed | ok | LLM unavailable due to Anthropic credits |
| broken_04_wrong_api | compiler | fail | not fixed | ok | LLM unavailable due to Anthropic credits |
| broken_05_missing_include | compiler | fail | not fixed | ok | LLM unavailable due to Anthropic credits |
| broken_06_missing_library | dependency | fail | not fixed | ok | Requires missing third-party Arduino library |
| broken_07_incorrect_pin | logic | pass | compile-pass | ok | Compiler accepts code, but pin value is logically invalid |
| broken_08_wrong_function_signature | compiler | fail | not fixed | ok | LLM unavailable due to Anthropic credits |
| broken_09_deprecated_api | warning | pass | compile-pass | ok | Static/warning-level issue |
| broken_10_forgotten_serial_begin | logic | pass | compile-pass | ok | Compiler accepts code, but Serial.begin is missing |

## Notes

`Before` shows whether the original benchmark produced compiler diagnostics.

`Fix Result` shows the result of the CircuitMind fix loop. For compiler-error benchmarks, `not fixed` currently reflects that live LLM repair is blocked by Anthropic credits.

For logic/static benchmarks, `compile-pass` means the firmware compiled, not that the bug was truly repaired. These benchmarks require metadata-aware scoring in a future version.