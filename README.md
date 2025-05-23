# Python Utils

A collection of reusable Python utilities for common tasks.

## Logging Utility

A flexible logging utility that supports both console and file logging with JSON and text formats.

### Installation

No installation required - just import the module:

```python
from utils.logging import get_logger
```

### Parameters

- `name` (str | None): Logger name. If None, uses the root logger.
- `log_level` (int | str): Logging level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
- `log_file` (str | Path | None): Path to the log file. If None, logs only to console.
- `log_format` (Literal['json', 'text']): Output format. 'json' for structured logs, 'text' for human-readable.
- `max_bytes` (int): Maximum log file size in bytes before rotation (default: 10MB).
- `backup_count` (int): Number of backup log files to keep (default: 5).

### Basic Usage

```python
logger = get_logger("my_app")
logger.info("Application started")
```

### Advanced Configuration

```python
logger = get_logger(
    name="my_app",
    log_level="DEBUG",
    log_file="logs/app.log",
    log_format="json",
    max_bytes=5 * 1024 * 1024,  
    backup_count=3               
)
```

### Best Practices

1. **Logger Naming**: Use `__name__` to automatically use the module's name as the logger name:

   ```python
   logger = get_logger(__name__)
   ```

2. **Structured Logging**: Use the `extra` parameter to add context to your logs:

   ```python
   logger.info("Processing user", extra={"user_id": user.id, "action": "process"})
   ```

3. **Exception Handling**: Use `logger.exception` in exception handlers to automatically include stack traces:
   ```python
   try:
       # risky operation
   except Exception as e:
       logger.exception("Operation failed")
   ```

### Example Output

**Text Format**:

```
2023-05-23 15:30:45 - my_app - INFO - User logged in
2023-05-23 15:30:46 - my_app - ERROR - Division by zero
```

**JSON Format**:

```json
{"timestamp": "2023-05-23 15:30:45", "level": "INFO", "message": "User logged in", "module": "app", "function": "login", "line": 42, "user_id": 123}
{"timestamp": "2023-05-23 15:30:46", "level": "ERROR", "message": "Division by zero", "module": "app", "function": "calculate", "line": 24, "exception": "Traceback (most recent call last):\n  File \"app.py\", line 22, in calculate\n    1/0\nZeroDivisionError: division by zero"}
