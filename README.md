# regrader

## Current State
- ZyBooks checks stdout instead of logic
  - Incorrect answer when missing:
    - Spaces
    - New lines
  - Makes students think either:
    - ZyBooks is "broken"
    - Doubt their correct code's functionality
    - Cause stress 🙍


## Usage
- Use Remote Code Execution and predefined test cases to test student homework
- Link directly to MOSS for easy plagiarism checking 🙈
- Need student DB access (currently will store data in MongoDB)
  - CURRENTLY SQLITE3 FOR CLASS USE ONLY
- Integrate with Git for test integration

