# A command that will create a new environment, install the required packages, and start the assistant.

# Create a new environment using pyenv, it's already using python 3.11
pyenv virtualenv 3.11.0 metAIsploit-assistant

# Activate the environment
pyenv activate metAIsploit-assistant

# Install the required packages
poetry install
poetry run init

# Start the assistant
