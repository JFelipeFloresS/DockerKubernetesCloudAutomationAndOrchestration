from src.utils.user_input_handler import get_user_input, InputType


class AbstractMenu:

    def __init__(self, menu_name, options):
        self.menu_name = menu_name
        self.options = options

    def get_user_choice(self):
        """
        Get the user's menu choice.
        :return: int representing the user's choice.
        """
        # add exit option dynamically since 0 is not a valid key in options
        # exit is in options as 99 for ordering purposes
        self.options[0] = "Exit"
        choice = get_user_input("Select an option", InputType.INT, available_options=self.options)
        return choice

    def display_options(self):
        """
        Display the menu options to the user.
        :return: None
        """
        print(f"=== {self.menu_name} ===")
        # display options in the established order
        for key in sorted(self.options.keys()):
            display_key = 0 if key == 99 else key
            print(f"{display_key}. {self.options[key]}")
        print("===================")

    def run(self):
        """
        Run the menu loop, displaying options and executing user choices.
        :return: None
        """
        is_continue = True
        while is_continue:
            try:
                self.display_options()
                choice = self.get_user_choice()
                is_continue = self.execute_choice(choice)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    @staticmethod
    def handle_invalid_choice():
        """
        Handle invalid menu choices.
        :return: None
        """
        print("Invalid choice. Please try again.")

    @staticmethod
    def exit_application():
        """
        Exit the application.
        :return: None
        """
        print("Exiting the application.")
        exit()

    def execute_choice(self, choice):
        """
        Execute the action corresponding to the user's choice.
        This method should be implemented by subclasses.
        :param choice: The user's menu choice.
        :return: bool indicating whether to continue the menu loop.
        """
        raise NotImplementedError("Subclasses must implement this method.")
