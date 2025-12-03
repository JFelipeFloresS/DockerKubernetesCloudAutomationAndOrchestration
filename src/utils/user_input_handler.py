from enum import Enum
from getpass import getpass


class InputType(Enum):
    STRING = 1
    INT = 2


def get_user_input(prompt, input_type: InputType = InputType.STRING, default_value='', available_options: list = None,
                   is_secret=False):
    """
    Get user input from the console with validation and default value support.
    :param prompt: The prompt message to display to the user.
    :param input_type: The expected type of the input (STRING, INT).
    :param default_value: The default value to use if the user provides no input.
    :param available_options: The list of valid options for the input.
    :return: The validated user input, or False if the operation was cancelled.
    """
    try:
        full_prompt = prompt
        if default_value:
            full_prompt += f" [Default: {default_value}]"
        if available_options and not all(isinstance(option, int) for option in available_options):
            full_prompt += f" or input the number corresponding to one of the available options"
        full_prompt += " (type 'cancel' to cancel): "
        if is_secret:
            response = getpass(full_prompt).strip() or default_value
        else:
            response = input(full_prompt).strip() or default_value

        # Allow user to cancel the operation. check if response is string before checking as ints can't be .lower()
        if isinstance(response, str) and response.lower() == 'cancel':
            print("Operation cancelled by user.")
            return False

        # Validate int input
        if input_type == InputType.INT:
            try:
                response = int(response)
            except ValueError:
                print("Invalid input. Expected an integer.")
                return get_user_input(prompt, InputType.INT, default_value, available_options, is_secret)

        # Validate against available options if provided
        if available_options is not None and response not in available_options:
            try:
                index = int(response) - 1  # Adjust for zero-based index
                if 0 <= index < len(available_options):
                    print(f"Selected option: {available_options[index]}")
                    return available_options[index]
            except Exception as e:
                print(f"Invalid input. Available options are: {', '.join(map(str, available_options))}")
                return get_user_input(prompt, input_type, default_value, available_options, is_secret)

        return response

    # Handle user interrupt (Ctrl+C) and stopping program gracefully
    except KeyboardInterrupt:
        print("Input cancelled by user.")
        return False

    # Handle any other unexpected exceptions
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
