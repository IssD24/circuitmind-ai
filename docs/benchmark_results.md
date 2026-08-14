# CircuitMind Benchmark Results

CircuitMind was evaluated on 10 broken Arduino firmware benchmarks covering compiler errors, API misuse, logic issues, warning-level issues, missing dependencies, and platform/toolchain limitations.

## Summary

- Total benchmark cases: 10
- Fixed by CircuitMind: 7
- Not fixed: 3
- Automated benchmark resolution rate: 70%

## Benchmark Table

| Benchmark | Type | Before | Fix Result | Status | Notes |
|---|---|---|---|---|---|
| broken_01_missing_semicolon | compiler | fail | fixed | ok | Added missing semicolon and rebuilt successfully |
| broken_02_wrong_wire_signature | compiler | fail | fixed | ok | Corrected invalid `Wire.begin(...)` usage |
| broken_03_missing_include | compiler/dependency | fail | not fixed | ok | Diagnosed ArduinoJson include/dependency issue, but environment/library setup is required |
| broken_04_wrong_api | compiler | fail | fixed | ok | Replaced invalid API call with the correct Arduino serial API |
| broken_05_missing_include | compiler/platform | fail | not fixed | ok | Diagnosed STL/toolchain limitation with AVR Arduino target |
| broken_06_missing_library | compiler/dependency | fail | not fixed | ok | Diagnosed missing ArduinoJson library in the build environment |
| broken_07_incorrect_pin | logic | fail | fixed | ok | Repaired logic-level pin issue based on benchmark validation |
| broken_08_wrong_function_signature | compiler | fail | fixed | ok | Fixed missing function argument |
| broken_09_deprecated_api | warning | fail | fixed | ok | Repaired warning/static-analysis-level issue |
| broken_10_forgotten_serial_begin | logic | fail | fixed | ok | Added missing serial initialization logic |

## Resolution Breakdown

| Category | Count | Percentage |
|---|---:|---:|
| Fixed | 7 | 70% |
| Not fixed | 3 | 30% |
| Total | 10 | 100% |

## Hardware Upload Demo

CircuitMind was also tested on a physical Arduino Uno using the local Arduino CLI upload path.

| Demo | Board | Result | Notes |
|---|---|---|---|
| broken_01_missing_semicolon upload | Arduino Uno | uploaded | CircuitMind fixed the sketch, rebuilt it, and uploaded it to the board through `arduino-cli compile --upload` |
| hardware_broken_blink | Arduino Uno | uploaded | CircuitMind fixed a broken blink sketch and uploaded the repaired firmware so the onboard LED blinked |

## Notes

`fixed` means CircuitMind generated or applied a repair, rebuilt the benchmark, and the benchmark runner marked the case as fixed.

`not fixed` means CircuitMind attempted or diagnosed the issue, but the benchmark was not repaired end-to-end in the current environment.

Dependency and platform/toolchain issues may require environment changes, library installation, or target-specific rewrites instead of simple source-code patching.

The hardware upload demo is separate from the 10-case benchmark suite and shows that repaired firmware can be uploaded to a real Arduino Uno.