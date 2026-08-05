# UV

| Feature                | pip                                                      | uv                                                            |
| ---------------------- | -------------------------------------------------------- | ------------------------------------------------------------- |
| Core Function          | Install python packages                                  | Manages environment and dependencies                          |
| Speed                  | Moderate                                                 | 10 - 100x faster                                              |
| Vir. Env               | Require the manual creation                              | Create, manages and auto activate environment<br />seanlessly |
| Python<br />Management | Require external tools like pyenv                        | Install and manage python version natively                    |
| Cross Platform         | No - generates platform specific<br />requirements.txt  | Yes - generates cross platform uv.lock                        |

### Install the UV env

    uv venv
    uv venv my-name
    uv venv python-version

### To activate

    .venv/Scripts/activate

### To initialized

    uv init

### To install libary

    uv add libary-name
    uv pip install libary-name

### To Uninstall libary

    uv remove libary-name
    uv pip uninstall libary-name
    uv pip install -r requirements.txt

### To export the requirement.txt

    uv export --format requirements-txt > requirements.txt

### To recreate the local environment

    uv sync

### To visualize the dependency folder

    uv tree

### To view the libary and version

    uv pip list
