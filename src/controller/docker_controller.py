import platform
import subprocess
import time
from enum import Enum

import docker
from docker.errors import DockerException


class DockerContainerStatus(Enum):
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    RESTARTING = "restarting"
    REMOVING = "removing"
    EXITED = "exited"
    DEAD = "dead"


class DockerController:
    def __init__(self):
        """
        Initialise the Docker controller, starting Docker if it's not running.
        :return: None
        """
        try:
            self.client = docker.from_env()
            self.client.ping()
        except DockerException:
            print("Docker is not running. Attempting to start Docker...")
            self._start_docker()
            self._wait_for_docker()

    def _start_docker(self):
        """
        Start the Docker based on the operating system.
        :return: None
        """
        system = platform.system()
        if system == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "Docker"])
        elif system == "Windows":
            # The path might need to be adjusted depending on the installation location.
            subprocess.Popen(r'start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"', shell=True)
        else:
            print(f"Unsupported OS '{system}'. Please start Docker manually.")
            raise NotImplementedError(f"Automatic Docker start is not supported on '{system}'.")

    def _wait_for_docker(self):
        """
        Wait for Docker to become available.
        :return: None
        """
        print("Waiting for Docker to start...")
        for _ in range(15):  # wait for 30s
            try:
                self.client = docker.from_env()
                self.client.ping()
                print("Docker started successfully.")
                return
            except DockerException:
                time.sleep(2)
        raise RuntimeError("Docker did not start in a reasonable time. Please start it manually.")

    def list_containers(self, is_all=False, status=None):
        """
        List all containers.
        :param is_all: bool indicating whether to list all containers or only running ones
        :param status: list of DockerContainerStatus to filter by
        :return: list of Docker containers
        """
        filters = {}
        containers = []
        if status:
            for curr_status in status:
                filters["status"] = curr_status.value
                containers += self.client.containers.list(all=is_all, filters=filters)
        else:
            containers = self.client.containers.list(all=is_all, filters=filters)
        return containers

    def start_container(self, container_id):
        """
        Start a Docker container by its ID.
        :param container_id: str ID of the Docker container
        :return: None
        """
        container = self.client.containers.get(container_id)
        container.start()

    def stop_container(self, container_id):
        """
        Stop a Docker container by its ID.
        :param container_id: str ID of the Docker container
        :return: None
        """
        container = self.client.containers.get(container_id)
        container.stop()

    def remove_container(self, container_id):
        """
        Remove a Docker container by its ID.
        :param container_id: str ID of the Docker container
        :return: None
        """
        container = self.client.containers.get(container_id)
        container.remove()

    def run_container(self, image_name):
        """
        Run a new Docker container with the specified image.
        :param image_name: str name of the Docker image
        :return: Docker container object
        """
        container = self.client.containers.run(image_name, detach=True)
        return container

    def run_command_in_container(self, container_id, command):
        """
        Run a command in a specified Docker container.
        :param container_id: str ID of the Docker container
        :param command: str command to run inside the container
        :return: tuple of (exit_code, output)
        """
        container = self.client.containers.get(container_id)
        exec_instance = container.exec_run(command)
        return exec_instance.exit_code, exec_instance.output.decode()

    def list_secrets(self):
        """
        List all Docker secrets.
        :return: list of Docker secrets
        """
        secrets = self.client.secrets.list()
        return secrets

    def docker_swarm_init(self):
        """
        Initialize Docker Swarm mode.
        :return: Swarm initialisation response
        """
        response = self.client.swarm.init()
        return response

    def is_docker_swarm_active(self):
        """
        Check if Docker Swarm mode is active.
        :return: bool indicating if Swarm mode is active
        """
        try:
            swarm_info = self.client.swarm.attrs
            return True if swarm_info else False
        except docker.errors.APIError:
            return False

    def create_secret(self, name, data):
        """
        Create a new Docker secret.
        :param name: str name of the secret
        :param data: bytes data of the secret
        :return: Docker secret object
        """
        secret = self.client.secrets.create(name=name, data=data)
        return secret

    def list_images(self):
        """
        List all Docker images.
        :return: list of Docker images
        """
        images = self.client.images.list()
        return images

    def get_image_history(self, image_id):
        """
        Get the history of a Docker image.
        :param image_id: str ID of the Docker image
        :return: list of history entries
        """
        image = self.client.images.get(image_id)
        history = image.history()
        return history

    def remove_image(self, image_id):
        """
        Remove a Docker image.
        :param image_id: str ID of the Docker image
        :return: None
        """
        self.client.images.remove(image_id)
