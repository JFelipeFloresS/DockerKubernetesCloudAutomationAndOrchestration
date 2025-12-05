#### Jose Felipe Flores da Silva

#### Student number: R00293192

#### [GitHub Repository](https://github.com/JFelipeFloresS/DockerKubernetesCloudAutomationAndOrchestration)

# SECTIONS

- [DEPENDENCIES](#dependencies)
- [USER INPUT](#user-input)
- [RUNNING THE APPLICATION](#running-the-application)
- [FEATURES](#features)
    - [Docker Management](#docker-management)
    - [Kubernetes Management](#kubernetes-management)

<div style="background-color: #ffeb3b; padding: 10px; margin-bottom: 16px; color: black">
<strong>WARNING:</strong>
<br>
I haven't tested this project on Windows, so there might be some differences in commands or paths.
<br>
For this README file, I asked ChatGPT to generate the Windows commands based on the Mac/Linux commands I provided, but I cannot guarantee their accuracy.
</div>

## DEPENDENCIES

This project requires the Python packages listed in the [requirements.txt](requirements.txt) file. You can install them
using pip:

- For Windows:

```bash
pip install -r requirements.txt
```

- For Linux/Mac:

```bash
pip3 install -r requirements.txt
```

![img.png](assets/read_me_images/img.png)

## USER INPUT

This is a command-line application that requires user input during execution. Follow the prompts in the terminal to
provide the necessary information.

When a list is provided, you can either type the value directly or select from the numbered options displayed.
For example, if prompted to select an option from a list:

```
Select an option:
1. Option A
2. Option B
3. Option C
```

You can either type "Option A" or just "1" to select it.

If a default value is provided in the prompt, you can simply press Enter to accept the default.
For example, if prompted:

```
Enter your name [Default: John Doe]:
```

Pressing Enter without typing anything will select "John Doe" as the input.

You can cancel any operation at any time by typing "cancel" and pressing Enter. This will abort the current process and
return you to the main menu or exit the application, depending on the context.

On any inner menu, typing "Main menu" or the corresponding number for the main menu option will take you back to the
main menu.

On any menu, typing "exit" or the corresponding number for the exit option will terminate the application.

## RUNNING THE APPLICATION

To run the application, use the following command in your terminal:

- For Windows:

```bash
python -m src.main
```

- For Linux/Mac:

```bash
python3 -m src.main
```

> **Note:**
>
> The `python` vs `python3` command may vary depending on your system's configuration.

## FEATURES

![img_1.png](assets/read_me_images/img_1.png)

The application provides the following sub-systems:

- Docker Management
    - ![img_2.png](assets/read_me_images/img_2.png)
- Kubernetes Management

### Docker Management

The Docker Management sub-system allows you to manage Docker containers and images. You can perform tasks such as:

- List all Docker containers
    - ![img_3.png](assets/read_me_images/img_3.png)
- Start a Docker container
    - ![img_4.png](assets/read_me_images/img_4.png)
    - ![img_5.png](assets/read_me_images/img_5.png)
- Stop a Docker container
    - ![img_6.png](assets/read_me_images/img_6.png)
    - ![img_7.png](assets/read_me_images/img_7.png)
- Remove a Docker container
    - ![img_8.png](assets/read_me_images/img_8.png)
    - ![img_9.png](assets/read_me_images/img_9.png)
- Run a new Docker container from an image
    - ![img_10.png](assets/read_me_images/img_10.png)
    - ![img_11.png](assets/read_me_images/img_11.png)
- Run a command inside a Docker container
    - ![img_12.png](assets/read_me_images/img_12.png)
    - ![img_13.png](assets/read_me_images/img_13.png)
- List all secrets
    - ![img_14.png](assets/read_me_images/img_14.png)
- Create a new secret
    - ![img_15.png](assets/read_me_images/img_15.png)
    - ![img_16.png](assets/read_me_images/img_16.png)
- List all Docker images
    - ![img_17.png](assets/read_me_images/img_17.png)
- Get a Docker image's history
    - ![img_18.png](assets/read_me_images/img_18.png)
    - ![img_19.png](assets/read_me_images/img_19.png)
- Remove a Docker image
    - ![img_20.png](assets/read_me_images/img_20.png)
    - ![img_21.png](assets/read_me_images/img_21.png)
    - ![img_22.png](assets/read_me_images/img_22.png)
- Run a python program inside a Docker container (Assignment Docker Requirement 2)
    - [Test file](src/assets/test.py)
    - ![img_23.png](assets/read_me_images/img_23.png)
- Build and run a Weather Pipeline with Docker (Assignment Docker Requirement 3)
    - ![img_24.png](assets/read_me_images/img_24.png)
    - ![img_25.png](assets/read_me_images/img_25.png)
    - ![img_26.png](assets/read_me_images/img_26.png)
    - ![img_27.png](assets/read_me_images/img_27.png)
    - ![img_28.png](assets/read_me_images/img_28.png)
    - Containers are now running:![img_36.png](assets/read_me_images/img_36.png)
    - Clear frontend:![img_29.png](assets/read_me_images/img_29.png)
    - Adding new city to Redis queue:
        - Frontend visual cue: ![img_30.png](assets/read_me_images/img_30.png)
        - Backend worker receiving request and sending it to Postgres straight
          away:![img_31.png](assets/read_me_images/img_31.png)
    - After clicking refresh:
        - We can see the queue has been processed in the frontend:![img_32.png](assets/read_me_images/img_32.png)
        - Get request in the backend for both the queue and the weather
          DB:![img_33.png](assets/read_me_images/img_33.png)
    - A new POST request:
        - Front end displays queue and Postgres values separately:![img_34.png](assets/read_me_images/img_34.png)
        - New POST request to add item city request to queue + sending it to Postgres straight
          away:![img_35.png](assets/read_me_images/img_35.png)
    - If the number of requests was sufficiently high, we would be able to see the queue processing in the backend
      worker as well.
    - By typing ctrl+c in the terminal where the application is running, we can stop all containers:
        - ![img_37.png](assets/read_me_images/img_37.png)
        - ![img_38.png](assets/read_me_images/img_38.png)

### Kubernetes Management