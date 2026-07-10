# PyLogger

A lightweight, high-performance, and thread-safe logging utility for Python. It provides beautiful console output, automatic file persistence, and robust context management to ensure your logs are always captured correctly.

## Features

* **Context Managed**: Automatically handles file opening/closing using the `with` statement.
* **Thread-Safe**: Designed to prevent file corruption in concurrent environments.
* **Automatic Cleanup**: Built-in rotation policy to delete logs older than a specified number of days.
* **Structured Levels**: Supports `DEBUG`, `INFO`, `WARNING`, and `ERROR` levels with color-coded terminal output.
* **Exception Tracking**: Automatically captures and logs full stack traces during exceptions.

## Installation

This project relies on `colorama` for cross-platform terminal colors. You can install it via pip:

```bash
pip install colorama

```

## Example Usage

Wrap your application logic in a `with` block to ensure all resources are cleaned up safely, even if the program crashes.

```python
from logger import Logger

# Initialize with desired configuration
# Using the 'with' statement ensures the file closes automatically
with Logger(colors=True, frame=60, version='full', save=True) as log:

    log.info("System health check initiated...")
    
    # Example of a debug message (only shows if version='full' or debug mode is True)
    log.debug("Initializing background worker components.")

    try:
        # Simulate a dangerous operation
        log.warning("Attempting to access restricted database...")
        data = 100 / 0
        
    except Exception as e:
        # This logs the specific error + captures the full traceback automatically
        log.error(f"Critical failure occurred: {e}")

    log.info("Process execution completed.")

# The log file is automatically closed here

```
![Logger Terminal Output](code.png)

## Configuration

You can customize the logger behavior during initialization:

| Parameter | Default | Description |
| --- | --- | --- |
| `colors` | `True` | Enables ANSI color output in the terminal. |
| `frame` | `50` | Sets the width of the visual decorative borders. |
| `version` | `'test'` | Toggles debug mode (`'full'` disables debug logs). |
| `save` | `False` | When `True`, saves logs to a timestamped file. |
| `min_level` | `0` | Minimum severity level required to print/log. |
| `days` | `7` | Duration to keep logs before auto-cleanup. |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
