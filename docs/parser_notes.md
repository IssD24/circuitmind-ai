# Parser Notes

## broken_01_missing_semicolon
- Status: produces structured diagnostics
- Parser issue: none for basic GCC-style error line
- Fix: current regex captures file, line, column, severity, and message

## broken_02_wrong_wire_signature
- Status: produces diagnostics
- Parser issue: check whether message is specific enough
- Fix: keep current regex unless output is empty

## broken_03_missing_include
- Status: produces diagnostics
- Parser issue: may include nested include/compiler trace lines
- Fix: capture primary error line first; improve later only if needed