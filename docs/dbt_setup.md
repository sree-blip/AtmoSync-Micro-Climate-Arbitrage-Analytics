# dbt Core & Snowflake Adapter Setup

This document records the installation and environment setup.

## Environment Details
- **Python Version**: 3.12.10
- **pip Version**: 25.0.1
- **dbt-core**: 1.12.0
- **dbt-snowflake**: 1.12.0

## Installation Steps

1. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   * **Windows (PowerShell)**:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   * **Windows (CMD)**:
     ```cmd
     .\.venv\Scripts\activate.bat
     ```
   * **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Verified Installation

The virtual environment was successfully created at `.venv/` and `dbt` installation was verified using:
```bash
.\.venv\Scripts\dbt --version
```

### Command Output:
```text
Core:
  - installed: 1.12.0

Plugins:
  - snowflake: 1.12.0 - Up to date!
```

