from src.view.abstract_menu import AbstractMenu


def open_docker_menu():
    from src.view.docker_menu import DockerMenu
    docker_menu = DockerMenu()
    docker_menu.run()


def open_kubernetes_menu():
    raise NotImplementedError("Kubernetes management menu is not yet implemented.")


class MainMenu(AbstractMenu):
    def __init__(self):
        main_menu_options = \
            {1: "Docker Management",
             2: "Kubernetes Management",
             99: "Exit"}
        super().__init__("Main Menu", main_menu_options)

    def execute_choice(self, choice):
        if choice == 1:
            open_docker_menu()
        elif choice == 2:
            open_kubernetes_menu()
        elif choice == 99 or choice == 0:
            self.exit_application()
        else:
            self.handle_invalid_choice()

        return True
