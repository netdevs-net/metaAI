# MetAIsploit Assistant

AI-powered Metasploit Automation & Module Generation Platform

---

## Overview
MetAIsploit Assistant is an advanced AI-driven automation framework for Metasploit, designed to:
- **Automate exploitation workflows** using RL (Reinforcement Learning) and LLMs (Large Language Models)
- **Generate custom Metasploit modules** from CVEs and vulnerability data
- **Integrate with vulnerable apps (e.g., DVWA) for end-to-end training and testing**
- **Enable secure, reproducible, and rapid development** via Docker Compose

---

## Features
- **Automated Metasploit RPC startup** (no msfrpcd; modern msgrpc method)
- **Persistent PostgreSQL database integration** for Metasploit
- **Python RL Gym environment** for safe, repeatable exploitation experiments
- **LLM integration** (Phi-2 quantized GGUF by default, SecBERT optional)
- **Replay buffer, structured JSON logging, and TensorBoard monitoring** for RL
- **Automated DNS leak/crt.sh checks before scanning**
- **Organized scan output (scans/ directory)**
- **Docker Compose orchestration** (Metasploit, Assistant, DVWA, DB)
- **Rapid development via local source volume mounts**

---

## Architecture

```
[User]
   |
   v
[Assistant (Python, RL, LLM)] <-> [Metasploit (msfconsole+msgrpc)] <-> [PostgreSQL]
   |
   v
[DVWA / Target Apps]
```
- **Assistant**: Python 3.11, Poetry, LangChain, RL, LLMs
- **Metasploit**: Official Docker image, msgrpc plugin, DB support
- **DVWA**: Vulnerable web app for RL/LLM training
- **All services**: Docker Compose, isolated network

---

## Quickstart

1. **Clone the repo**
2. **Copy and edit `.env-dev`**
   - Set `MSGRPC_PASS` and DB credentials
3. **Start all services**
   ```bash
   docker compose up -d --build
   ```
4. **Check service health**
   ```bash
   docker compose ps
   ```
5. **Test Metasploit RPC connectivity**
   ```bash
   docker compose exec metaisploit-assistant poetry run python scripts/test_pymetasploit3.py
   ```

---

## Development Workflow
- **Live code reload** via `.:/app` volume mount (edit code on host, see changes instantly in container)
- **Only restart containers for dependency or config changes**
- **All secrets managed via `.env-dev`** (never hardcode passwords)

---

## RL & LLM Integration
- **RL agent**: Trains to exploit DVWA and other targets using Gym environment
- **LLM**: Phi-2 by default; can switch to SecBERT Instructional for security/NLP tasks
- **Replay buffer**: All RL transitions logged for analysis and offline fine-tuning
- **TensorBoard**: Monitor RL progress (`scripts/run_tensorboard.sh`)

---

## Security & Best Practices
- **No secrets in code or Compose**; use `.env-dev` only
- **Metasploit RPC not exposed outside Docker network**
- **Persistent DB and scan data**
- **Healthchecks on all major services**

---

## Troubleshooting
- **Poetry install errors**: Ensure `README.md` exists, or use `--no-root` flag
- **Metasploit RPC auth errors**: Ensure `MSGRPC_PASS` matches in `.env-dev` and Compose
- **Container build issues**: Rebuild with `docker compose up -d --build`

---

## Contributing
- PRs and issues welcome!
- Please follow best practices for Python, Docker, and security

---

## License
MIT

---

## Authors
- [Your Name Here]
- [Contributors]

---

## References
- [Metasploit Framework](https://github.com/rapid7/metasploit-framework)
- [DVWA](https://github.com/digininja/DVWA)
- [Phi-2](https://huggingface.co/microsoft/phi-2)
- [SecBERT Instructional](https://huggingface.co/jackaduma/SecBERT-Instructional)


This is a placeholder README to satisfy Poetry install requirements.

This project is a study into generating POC / Exploits for the metasploit framework using LLMs.

Assumptions of the project:
1. Metasploit framework has a well defined outcome for a module.
2. The modules have metadata required for each module that would make labeling easier and more consistent.
3. The modules can be broken down into various utilities that (assumed to be similar to defined classes).
3. Most modules are associated with CVE research that can lead to robust prompt generation.

*Success Criteria for Project*: Utilize the commandline chat prompt to generate a guide for install, and usage of a module that can be saved directly into the metasploit framework using a previously unseen CVE.

## Quick Use
For a quick demo on how this is used please run the following commands (assuming you have the pre-reqs installed).

Setup
```sh
pip install poetry
git clone https://github.com/roostercoopllc/metAIsploit-assistant -r
cd metAIsploit-assistant
poetry install
# (Optional) This will download the snoozy binary by default
poetry run init
```

```sh
# If you don't have the snoozy model downloaded
poetry run demo
# if you do have the snoozy model downloaded
poetry run prompt-demo
```

You can run the script interactively by running the following commands:
```sh
export METASPLOIT_ROOT=<your metasploit root>
# Update the .env with your MSF root
poetry run chat
```

*Note* Depending on your hardware you are running this on, this might take a little while to return the response.

## Install / Setup
This project uses poetry to generate manage dependencies and attempts to keep the project clean (we will see for how long)

You can use this module through the poetry commands outlined in the `pyproject.toml`.

However, it is intended to eventually be available through the `msfconsole` to where you can use a digital assistant without needing to start a different terminal and keep the same session alive. 

### Requirements
* python 3.11
* Metasploit-Framework
* git-lfs
* And the below pip packages managed by poetry

Development Setup
```sh
poetry install
```

---

## Quickstart

1. **Clone the repo**
2. **Copy and edit `.env-dev`**
   - Set `MSGRPC_PASS` and DB credentials
3. **Start all services**
   ```bash
   docker compose up -d --build
   ```
4. **Check service health**
   ```bash
   docker compose ps
   ```
5. **Test Metasploit RPC connectivity**
   ```bash
   docker compose exec metaisploit-assistant poetry run python scripts/test_pymetasploit3.py
   ```
    There are two scripts that attempt to make the prompt dataset. These prompts are based off of a collection of the writeups on cves from the mitre collection of cves. They will associate the metasploit modules with ever one of the complete write ups housed in the the mitre datahouse. 

    The prompts for training are the entire white paper and an additional prompt of the phrase `write a metasploit module for cve-xxxx-yyyyy`.
     
    - Automated Labeling will take the CVE code and attempt to search it on the cve database on the MITRE repository for CVEs. It will then search the URLs of the CVE references and create prompts that associate with the Metasploit module the cve goes with. 
    *Note*: Hopeuflly this will create mroe variance on what kind of description of the CVEs will generate a valid module.
  * Manual Labeling:

* *Training*
  * Transfer Learning:
  * Scoring / Performance:

* *Saving Model*
  * Saving Models:

## (TO-DO) Ways to contribute
1. Label Data
2. Create Quality of Life to code
3. Write wiki documents

## FAQs
1. [What are the Metasploit Python Module Guidelines?](https://docs.metasploit.com/docs/development/developing-modules/external-modules/writing-external-python-modules.html)
2. [What do you to to train a model?](https://huggingface.co/blog/how-to-train)

## References
1. [Big thanks to Nomic AI and the gpt4all project](https://github.com/nomic-ai/gpt4all)
2. [Big thanks to Metasploit Framework by Rapid 7](https://github.com/rapid7/metasploit-framework)
3. [Huggingface Dataset for Metasploit Prompts](https://huggingface.co/datasets/icantiemyshoe/cve-to-metasploit-module) 
4. [LLaMA Retraining Evaluation](https://github.com/zetavg/LLaMA-LoRA-Tuner)
5. [GPT4All Prompt Dataset](https://huggingface.co/datasets/nomic-ai/gpt4all-j-prompt-generations)
6. [Base Model used for the gpt4all models](https://github.com/kingoflolz/mesh-transformer-jax)
7. [Training nomic](https://github.com/nomic-ai/gpt4all/blob/main/gpt4all-training/README.md)
8. [Command Stagers](https://docs.metasploit.com/docs/development/developing-modules/guides/how-to-use-command-stagers.html)


## Monitoring RL Training with TensorBoard

To visualize RL training metrics (rewards, losses, etc.), use the provided helper script:

```bash
bash scripts/run_tensorboard.sh
```

This will launch TensorBoard on port 6006 (default). Open http://localhost:6006 in your browser to view live metrics.

You can customize the log directory and port:

```bash
bash scripts/run_tensorboard.sh [logdir] [port]
# Example: bash scripts/run_tensorboard.sh runs 6006
```

