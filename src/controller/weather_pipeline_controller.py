import os


class WeatherPipelineController:
    def __init__(self, docker_controller):
        """
        Initialise the WeatherPipelineController with a DockerController instance.

        I asked ChatGPT what were the best options for this part of the assignment and there were a few suggestions:
        1. Chat relay (Python backend -> RabbitMQ -> Golang microservice -> MongoDB)
        2. Image processing pipeline (Upload -> Queue -> Worker -> Result Store + Viewer)
        3. Weather data pipeline (Python API -> Redis Queue -> Worker -> PostgreSQL -> Frontend Dashboard)
        4. Currency conversion service (Frontend -> API -> MySQL -> Cache)
        5. Logs aggregation demo (Python app -> Fluentd -> Elasticsearch -> Kibana)

        I chose option 3 as it seemed the most relevant to my interests since I'm thinking about implementing Redis in a project in work.

        :param docker_controller: DockerController instance to manage Docker operations.
        :return: None
        """
        self.docker_controller = docker_controller
        absolute_path = os.path.abspath(__file__)

        # get the path to the weather-pipeline directory
        absolute_path = os.path.join(os.path.dirname(absolute_path), '..', 'weather-pipeline')

        self.docker_controller.docker_compose_up_build(absolute_path)
