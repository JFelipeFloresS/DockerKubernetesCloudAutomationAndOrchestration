import os
import platform
import subprocess
import time
import webbrowser
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
        Run a new Docker container with the specified image and output its logs.
        :param image_name: str name of the Docker image
        :return: Docker container object
        """
        container = self.client.containers.run(image_name, detach=True)
        print(f"Started container {container.short_id} from image '{image_name}'. Streaming logs:")
        try:
            for log in container.logs(stream=True):
                print(log.decode('utf-8'), end='')
        except Exception as e:
            print(f"Error streaming logs: {e}")
        return container

    def run_command_in_container(self, container_id, command):
        """
        Run a command in a specified Docker container by opening a new terminal window for full interactivity.
        :param container_id: str ID of the Docker container
        :param command: str or list command to run inside the container
        :return: None
        """
        if isinstance(command, list):
            command_str = ' '.join(command)
        else:
            command_str = command
        docker_cmd = f"docker exec -it {container_id} {command_str}"
        system = platform.system()
        try:
            if system == "Darwin":  # macOS
                # Open a new Terminal window and run the command there (no activate, no set newWindow)
                script = f'''tell application "Terminal"
    do script "{docker_cmd}"
end tell'''
                subprocess.run(["osascript", "-e", script])
                print(f"Opened new Terminal window with: {docker_cmd}")
            elif system == "Windows":
                # Use start to open a new cmd window and run the command directly (no cmd /k)
                cmd = f'start "" {docker_cmd}'
                subprocess.run(cmd, shell=True)
                print(f"Opened new Command Prompt window with: {docker_cmd}")
            else:
                print(f"Unsupported OS '{system}'. Please run this command manually:")
                print(docker_cmd)
        except Exception as e:
            print(f"Error opening new terminal window: {e}")
        return None

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

    def run_python_program(self, python_path, python_version, image_name):
        """
        Build and run a Docker container that executes a Python program.
        :param python_path: The absolute path to the python program
        :param python_version: The version of python the program is written in (2.7 or 3.14)
        :param image_name: The name for the new Docker image
        :return: None
        """
        dockerfile_content = f"FROM python:{python_version}\n"
        if python_version.startswith("3"):
            dockerfile_content += "RUN pip install boto3\n"

        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        dockerfile_path = os.path.join(project_root, "Dockerfile")

        print("Copying Python program into Docker image from path:", python_path)
        dockerfile_content += f"COPY {os.path.basename(python_path)} /app/program.py\n"
        dockerfile_content += "CMD [\"python\", \"/app/program.py\"]\n"

        with open(dockerfile_path, "w") as dockerfile:
            dockerfile.write(dockerfile_content)

        print("Building Docker image...")
        image, build_logs = self.client.images.build(path=os.path.dirname(python_path), tag=image_name, rm=True)
        for chunk in build_logs:
            if 'stream' in chunk:
                print(chunk['stream'].strip())

        print("Running Docker container...")
        container = self.client.containers.run(image=image_name, detach=True)

        # Wait for the container to finish execution
        result = container.wait()
        output = container.logs()

        print("Output from the container:")
        print(output.decode('utf-8'))

        if result['StatusCode'] == 0:
            print("Python program executed successfully.")
        else:
            print(f"Python program exited with error code: {result['StatusCode']}")

        container.remove()

        return container

    def docker_compose_up_build(self, directory_path):
        """
        Run 'docker-compose up --build' for the specified docker-compose file.
        :param directory_path: The directory containing the docker-compose.yml file
        :return: None
        """
        compose_file = os.path.join(directory_path, "docker-compose.yml")
        if not os.path.exists(compose_file):
            raise FileNotFoundError(f"No docker-compose.yml found in {directory_path}")

        print("Running 'docker-compose up --build'...")
        process = subprocess.Popen(
            ["docker-compose", "-f", compose_file, "up", "--build"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        printed_url = False

        try:
            # Stream logs line-by-line
            for line in process.stdout:
                print(line, end="")  # keep showing live logs

                # Detect API ready message
                if ("Uvicorn running on http://0.0.0.0:8000" in line
                    or "Application startup complete" in line) and not printed_url:
                    frontend_url = "http://localhost:8080"
                    print(f"\nFrontend available at: {frontend_url}\n")
                    printed_url = True

                    webbrowser.open(frontend_url)
            process.wait()
        except KeyboardInterrupt:
            print("\nProcess interrupted by user. Shutting down docker-compose...")
            try:
                process.terminate()
            except Exception as e:
                print(f"Error terminating process: {e}")
            process.wait()
            print("docker-compose process terminated.")
