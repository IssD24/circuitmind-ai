# CircuitMind Benchmark Results

| Benchmark | Type | Before | Fix Result | Status | Notes |
|---|---|---|---|---|---|
| broken_01_missing_semicolon | compiler | fail | fixed | ok | Live Claude repair added the missing semicolon |
| broken_02_wrong_wire_signature | compiler | fail | fixed | ok | Live Claude repair corrected the invalid `Wire.begin(...)` call |
| broken_03_missing_include | dependency | fail | diagnosed | ok | Identified missing ArduinoJson dependency |
| broken_04_wrong_api | compiler | fail | fixed | ok | Live Claude repair changed `Serial.printline` to `Serial.println` |
| broken_05_missing_include | platform/toolchain | fail | diagnosed | ok | Identified AVR toolchain limitation with `<vector>` |
| broken_06_missing_library | dependency | fail | diagnosed | ok | Identified missing ArduinoJson library in the build environment |
| broken_07_incorrect_pin | logic | pass | compile-pass | ok | Compiler accepts code, but the pin value is logically invalid |
| broken_08_wrong_function_signature | compiler | fail | fixed | ok | Live Claude repair fixed the missing function argument |
| broken_09_deprecated_api | warning | pass | compile-pass | ok | Static/warning-level issue |
| broken_10_forgotten_serial_begin | logic | pass | compile-pass | ok | Compiler accepts code, but `Serial.begin` is missing |

## Summary

- Total benchmarks: 10
- Fixed live with Claude: 4
- Diagnosed dependency/platform issues: 3
- Compile-pass logic/static benchmarks: 3

## Resolution Breakdown

- Fixed live: 4 / 10 = 40%
- Diagnosed but not source-fixable in current environment: 3 / 10 = 30%
- Compile-pass logic/static cases needing metadata-aware evaluation: 3 / 10 = 30%

## Notes

`fixed` means CircuitMind generated a patch, applied it to a copied workspace, rebuilt the firmware, and the build passed.

`diagnosed` means CircuitMind identified the issue, but the fix requires an environment, dependency, or platform/toolchain change rather than a simple source-code patch.

`compile-pass` means the benchmark compiled before repair, so compiler-only scoring is not enough to judge correctness.