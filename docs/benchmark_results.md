# CircuitMind Benchmark Results

CircuitMind was evaluated on 10 broken Arduino firmware benchmarks covering compiler errors, Arduino API misuse, missing dependencies, platform/toolchain constraints, logic issues, and warning-level issues.

The latest benchmark run fixed all 10 cases through the automated repair workflow.

## Summary

- Total benchmark cases: 10
- Fixed by CircuitMind: 10
- Not fixed: 0
- Automated benchmark resolution rate: 100%

## Benchmark Table

| Benchmark | Type | Before | Fix Result | Status | Notes |
|---|---|---|---|---|---|
| broken_01_missing_semicolon | compiler | fail | fixed | ok | Added missing semicolon and rebuilt successfully |
| broken_02_wrong_wire_signature | compiler | fail | fixed | ok | Corrected invalid `Wire.begin(...)` usage |
| broken_03_missing_include | compiler/dependency | fail | fixed | ok | Removed unnecessary ArduinoJson dependency and used Arduino-compatible source-only output |
| broken_04_wrong_api | compiler | fail | fixed | ok | Replaced invalid API call with the correct Arduino serial API |
| broken_05_missing_include | compiler/platform | fail | fixed | ok | Repaired code in a way compatible with the Arduino Uno AVR toolchain |
| broken_06_missing_library | compiler/dependency | fail | fixed | ok | Repaired missing-library issue through a source-compatible workaround |
| broken_07_incorrect_pin | logic | fail | fixed | ok | Repaired logic-level pin issue based on benchmark validation |
| broken_08_wrong_function_signature | compiler | fail | fixed | ok | Fixed missing function argument |
| broken_09_deprecated_api | warning | fail | fixed | ok | Repaired warning/static-analysis-level issue |
| broken_10_forgotten_serial_begin | logic | fail | fixed | ok | Added missing serial initialization logic |

## Resolution Breakdown

| Category | Count | Percentage |
|---|---:|---:|
| Fixed | 10 | 100% |
| Not fixed | 0 | 0% |
| Total | 10 | 100% |

## Multi-Error Stress Tests

These tests are separate from the official 10-case benchmark suite. They evaluate whether CircuitMind can repair larger Arduino sketches with multiple compiler-detectable errors and simple spec-guided logic mistakes.

| Stress Test | Error Count | Result | Notes |
|---|---:|---|---|
| multi_01_led_two_errors | 2 | fixed + uploaded | Missing semicolon and misspelled Arduino API repaired |
| multi_02_led_three_errors | 3 | fixed + uploaded | Missing semicolon, bad argument syntax, and missing `digitalWrite` value repaired |
| multi_03_led_five_errors | 5 | fixed + uploaded | Multiple syntax/API/type errors repaired and uploaded |
| final_serial_led_controller | 8 mixed errors | fixed + uploaded | Realistic Serial-controlled LED firmware repaired and uploaded to Arduino Uno |

## Stress Test Summary

In addition to the official 10-case benchmark suite, CircuitMind repaired and uploaded multiple larger Arduino Uno sketches with 2–8 mixed syntax, API, type, and simple spec-guided logic errors.

## Hardware Upload Demo

CircuitMind was also tested on a physical Arduino Uno using the local Arduino CLI upload path.

| Demo | Board | Result | Notes |
|---|---|---|---|
| broken_01_missing_semicolon upload | Arduino Uno | uploaded | CircuitMind fixed the sketch, rebuilt it, and uploaded it to the board through `arduino-cli compile --upload` |
| hardware_broken_blink | Arduino Uno | uploaded | CircuitMind fixed a broken blink sketch and uploaded the repaired firmware so the onboard LED blinked |
| final_serial_led_controller | Arduino Uno | uploaded | CircuitMind repaired a realistic Serial-controlled LED sketch and uploaded it successfully |

## Notes

`fixed` means CircuitMind generated or applied a repair, rebuilt the benchmark, and the benchmark runner marked the case as fixed.

`fixed + uploaded` means CircuitMind repaired the sketch, rebuilt it, and uploaded the repaired firmware to a connected Arduino Uno.

The 100% result applies to the official 10-case benchmark suite.

The multi-error stress tests are separate from the official benchmark score.

The hardware upload demos show that repaired firmware can be uploaded to a real Arduino Uno.