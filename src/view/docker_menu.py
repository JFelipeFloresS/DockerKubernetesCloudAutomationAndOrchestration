from src.controller.docker_controller import DockerController, DockerContainerStatus
from src.utils.list_utils import container_to_string
from src.utils.user_input_handler import get_user_input
from src.view.abstract_menu import AbstractMenu


class DockerMenu(AbstractMenu):
    def __init__(self):
        docker_menu_options = \
            {1: "List Containers",
             2: "Start Container",
             3: "Stop Container",
             4: "Remove Container",
             5: "Run Container",
             6: "Run Command in Container",
             7: "List All Secrets",
             8: "Create Secret",
             9: "List Images",
             10: "Get Image History",
             11: "Remove Image",
             12: "Main Menu",
             99: "Exit"}
        super().__init__("Docker Menu", docker_menu_options)
        self.docker_controller = DockerController()

    def execute_choice(self, choice):
        if choice == 1:
            self.list_containers()
        elif choice == 2:
            self.start_container()
        elif choice == 3:
            self.stop_container()
        elif choice == 4:
            self.remove_container()
        elif choice == 5:
            self.run_container()
        elif choice == 6:
            self.run_command_in_container()
        elif choice == 7:
            self.list_all_secrets()
        elif choice == 8:
            self.create_secret()
        elif choice == 9:
            self.list_images()
        elif choice == 10:
            self.get_image_history()
        elif choice == 11:
            self.remove_image()
        elif choice == 12:
            return False
        elif choice == 99 or choice == 0:
            self.exit_application()
        else:
            self.handle_invalid_choice()
        return True

    def list_containers(self, is_all=True, status=None):
        """
        List Docker containers.
        :param is_all: bool indicating whether to list all containers or only running ones
        :param status: list of DockerContainerStatus to filter by
        :return: list of container IDs
        """
        container_list = self.docker_controller.list_containers(is_all=is_all, status=status)
        for (index, container) in enumerate(container_list):
            print(container_to_string(container, index))

        return [c.id for c in container_list]

    def start_container(self):
        """
        Start a Docker container by its ID.
        :return: None
        """
        stopped_containers = self.list_containers(is_all=False, status=[DockerContainerStatus.EXITED,
                                                                        DockerContainerStatus.CREATED,
                                                                        DockerContainerStatus.PAUSED])
        if not stopped_containers:
            print("No stopped containers available to start.")
            return
        container_id = get_user_input("Enter the Docker container ID to start: ", available_options=stopped_containers)
        if not container_id:
            return
        self.docker_controller.start_container(container_id)
        print(f"Container '{container_id}' started successfully.")

    def stop_container(self):
        """
        Stop a Docker container by its ID.
        :return: None
        """
        running_containers = self.list_containers(is_all=False, status=[DockerContainerStatus.RUNNING])
        if not running_containers:
            print("No running containers available to stop.")
            return
        container_id = get_user_input("Enter the Docker container ID to stop: ", available_options=running_containers)
        if not container_id:
            return
        self.docker_controller.stop_container(container_id)
        print(f"Container '{container_id}' stopped successfully.")

    def remove_container(self):
        """
        Remove a Docker container by its ID.
        :return: None
        """
        all_containers = self.list_containers(is_all=True)
        if not all_containers:
            print("No containers available to remove.")
            return
        container_id = get_user_input("Enter the Docker container ID to remove: ", available_options=all_containers)
        if not container_id:
            return
        self.docker_controller.remove_container(container_id)
        print(f"Container '{container_id}' removed successfully.")

    def run_container(self):
        """
        Run a new Docker container with a specified image.
        :return: None
        """
        image_name = get_user_input("Enter the Docker image name to run: ", default_value='hello-world')
        if not image_name:
            return
        try:
            container = self.docker_controller.run_container(image_name)
            print(f"Container started successfully with ID: {container.id}")
        except Exception as e:
            print(f"Failed to start container: {e}")

    def run_command_in_container(self):
        """
        Run a command in a specified Docker container.
        :return: None
        """
        running_containers = self.list_containers(is_all=False, status=[DockerContainerStatus.RUNNING])
        if not running_containers:
            print("No running containers available to run commands in.")
            return
        container_id = get_user_input("Enter the Docker container ID: ", available_options=running_containers)
        if not container_id:
            return
        command = get_user_input("Enter the command to run inside the container: ")
        if not command:
            return
        try:
            exit_code, output = self.docker_controller.run_command_in_container(container_id, command)
            print(f"Command executed with exit code {exit_code}. Output:\n{output}")
        except Exception as e:
            print(f"Failed to run command in container: {e}")

    def list_all_secrets(self):
        """
        List all Docker secrets.
        :return: None
        """
        try:
            if not self.docker_controller.is_docker_swarm_active():
                self.docker_controller.docker_swarm_init()
            secrets = self.docker_controller.list_secrets()
            if not secrets:
                print("No Docker secrets found.")
                return
            print("Docker Secrets:")
            for secret in secrets:
                print(f"ID: {secret.id} - Name: {secret.name}")
        except Exception as e:
            print(f"Failed to list Docker secrets: {e}")

    def create_secret(self):
        """
        Create a new Docker secret.
        :return: None
        """
        secret_name = get_user_input("Enter the name for the new Docker secret: ")
        if not secret_name:
            return
        secret_data = get_user_input("Enter the secret data: ", is_secret=True)
        if not secret_data:
            return
        try:
            self.docker_controller.create_secret(secret_name, secret_data)
            print(f"Docker secret '{secret_name}' created successfully.")
        except Exception as e:
            print(f"Failed to create Docker secret: {e}")

    def list_images(self):
        """
        List Docker images.
        :return: None
        """
        images = self.docker_controller.list_images()
        if not images:
            print("No Docker images found.")
            return None
        print("Docker Images:")
        for (index, image) in enumerate(images):
            tags = image.tags if image.tags else ["<none>:<none>"]
            print(f"{index + 1}. ID: {image.id} - Tags: {', '.join(tags)}")
        return [image.id for image in images]

    def get_image_history(self):
        """
        Get the history of a specified Docker image.
        :return: None
        """
        images = self.list_images()
        if not images:
            print("No Docker images found.")
            return
        image_id = get_user_input("Enter the Docker image ID to get history: ", available_options=images)
        if not image_id:
            return
        try:
            history = self.docker_controller.get_image_history(image_id)
            print(f"History for image {image_id}:")
            for entry in history:
                print(entry)
        except Exception as e:
            print(f"Failed to get image history: {e}")

    def remove_image(self):
        """
        Remove a specified Docker image.
        :return: None
        """
        images = self.list_images()
        if not images:
            print("No Docker images found.")
            return
        image_id = get_user_input("Enter the Docker image ID to remove: ", available_options=images)
        if not image_id:
            return
        try:
            self.docker_controller.remove_image(image_id)
            print(f"Docker image '{image_id}' removed successfully.")
        except Exception as e:
            print(f"Failed to remove Docker image: {e}")
