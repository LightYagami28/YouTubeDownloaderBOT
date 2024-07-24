#Changed Made by @LightYagami28

## Logging Setup
- Added `import logging` and set up basic logging.
- Reason: To provide detailed error information and improve debugging.

## Button Creation
- Simplified the creation of resolution buttons using list comprehension in the `create_resolution_buttons` function.
- Reason: To make the code cleaner and more concise.

## Global Variable Reduction
- Moved `LINK` to a local variable where possible in the `handle_link` and `callback` functions.
- Reason: To reduce the use of global variables and improve code readability.

## Exception Handling
- Enhanced error handling in the `download_and_send_video` function to include logging of exceptions.
- Reason: To provide more robust error management and detailed logging for easier debugging.

## Resolution Deduplication
- Used `set` to remove duplicate resolutions in the `handle_link` function.
- Reason: To ensure the list of resolutions presented to the user is unique.

## Function Parameter Refinement
- Modified `download_and_send_video` to accept `chat_id` and `link` as parameters.
- Reason: To avoid relying on global state, enhancing function modularity and making the code more maintainable.

## Redundant Imports
- Removed unused imports from the code.
- Reason: To clean up the code and improve efficiency by eliminating unnecessary dependencies.