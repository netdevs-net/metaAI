# MetAIsploit Assistant

**A hackable lab that turns CVEs into real exploits — practice pentesting safely, hands-on.**

Reading about exploits only gets you so far. MetAIsploit Assistant gives you a real Metasploit setup, a vulnerable app to attack, and AI that turns a CVE into a working module — so instead of just studying an exploit, you run it, watch it work, and see why it works.

- **Your own hackable lab.** Metasploit, an AI assistant, and a vulnerable target (DVWA), all wired together in Docker.
- **AI turns CVEs into working exploits.** Feed it vulnerability data and it generates the Metasploit module.
- **Practice safely, end to end.** Everything runs isolated and reproducible, so you can break things without breaking anything real.

---

## How it works

MetAIsploit Assistant is an AI-driven automation framework for Metasploit:
- **Automates exploitation workflows** using RL (Reinforcement Learning) and LLMs (Large Language Models)
- **Generates custom Metasploit modules** from CVEs and vulnerability data
- **Integrates with vulnerable apps (e.g., DVWA)** for end-to-end training and testing
- **Runs secure, reproducible, and fast** via Docker Compose

---

## Features
- **Automated Metasploit RPC startup** (no msfrpcd; modern msgrpc method)
- **Persistent PostgreSQL database integration** with automatic connection handling
- **Direct database configuration** for reliable Metasploit DB connectivity
- **Python RL Gym environment** for safe, repeatable exploitation experiments
- **LLM integration** (Phi-2 quantized GGUF by default, SecBERT Instructional optional via `LLM_MODEL` env var)
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

## Service Health & Testing
- **Service Healthcheck:**
  - Use `scripts/healthcheck.py` to verify the Metasploit RPC and DB services are up and responding.
  - Healthchecks are integrated into `docker-compose.yml` for automated status checks.
- **Metasploit DB Service:**
  - `scripts/metasploit_db_service.py` runs as a background service to monitor and reconnect the Metasploit DB if needed.
  - See `docker/metasploit-db.service` for systemd integration details.
- **Testing Metasploit Integration:**
  - Use `scripts/test_pymetasploit3.py` to verify RPC connectivity and DB status.
  - Use `scripts/msf_client.py` for advanced RPC client tests and development.
- **Performance Testing:**
  - `scripts/test_msf_performance.py` benchmarks Metasploit RPC client performance (basic vs optimized).

---

## Development Workflow
- **Live code reload** via `.:/app` volume mount (edit code on host, see changes instantly in container)
- **Database configuration** is handled automatically on container startup via `init-msf-db.sh`
- **Environment variables** in `.env-dev` control database and RPC settings
- **All scan outputs, logs, models, and data directories are gitignored by default**
- **Only restart containers for dependency or config changes**
- **All secrets managed via `.env-dev`** (never hardcode passwords)
- **Utility scripts:**
  - `scripts/crtsh_dns_leak.py`: Automated DNS leak check before scanning
  - `scripts/run_tensorboard.sh`: Launch TensorBoard for RL monitoring
  - `scripts/test_pymetasploit3.py`: Test Metasploit RPC connectivity

---

## RL & LLM Integration
- **RL agent**: Trains to exploit DVWA and other targets using Gym environment
- **LLM**: Phi-2 by default (models/phi-2.Q4_K_M.gguf); can switch to SecBERT Instructional (HuggingFace) by setting `LLM_MODEL=SecBERT-Instructional` in `.env-dev`
- **Replay buffer**: All RL transitions logged for analysis and offline fine-tuning
- **TensorBoard**: Monitor RL progress (`scripts/run_tensorboard.sh`)

---

## Security & Best Practices
- **No secrets in code or Compose**; use `.env-dev` only
- **Metasploit RPC not exposed outside Docker network**
- **Persistent DB, scan, log, and model data**
- **Healthchecks on all major services**
- **Project structure and generated files are organized for best practice (see below)**

---

## Docker Image & Build Management
- **Prebuilt Base Image:**
  - If you change system dependencies or Metasploit version, rebuild the base image:
    ```bash
    docker build -f Dockerfile.msfbase -t metasploit-base:latest .
    ```
  - For normal development, use:
    ```bash
    docker compose build
    docker compose up -d
    ```
  - Avoid `--no-cache` unless you change system dependencies or the base image.
- **Volume Mounts for Live Reload:**
  - Source code and models are mounted from the host for instant reloads and rapid iteration.
- **Environment Variables:**
  - All credentials (DB, msgrpc) are managed via `.env-dev` and passed securely to containers.

---

## Troubleshooting

### Database Connection Issues
If Metasploit fails to connect to the database:
1. Verify the PostgreSQL container is running:
   ```bash
   docker compose ps | grep db
   ```
2. Check container logs for errors:
   ```bash
   docker compose logs metasploit
   ```
3. Manually test the database connection:
   ```bash
   docker compose exec metasploit /usr/src/metasploit-framework/msfconsole -x 'db_status; exit'
   ```

### Common Issues
- **Poetry install errors**: Ensure `README.md` exists, or use `--no-root` flag
- **Metasploit RPC auth errors**: Ensure `MSGRPC_PASS` matches in `.env-dev` and Compose
- **Container build issues**: Rebuild with `docker compose up -d --build`
- **Database initialization issues**: If the database fails to initialize, try:
  ```bash
  docker compose down -v  # Warning: This will delete all data
  docker compose up -d
  ```

---

## Contributing
- PRs and issues welcome!
- Please follow best practices for Python, Docker, and security

---

## License
MIT

---

## Authors
- Net Devs


---

## References
- [Metasploit Framework](https://github.com/rapid7/metasploit-framework)
- [DVWA](https://github.com/digininja/DVWA)
- [Phi-2](https://huggingface.co/microsoft/phi-2)
- [SecBERT Instructional](https://huggingface.co/jackaduma/SecBERT-Instructional)




## Project Goals

This project aims to enhance Metasploit with AI/ML capabilities through:
1. **Automated Module Generation**: Create Metasploit modules from CVE data using LLMs
2. **Reinforcement Learning**: Train agents to automate exploitation workflows
3. **Intelligent Automation**: Combine LLMs with Metasploit's capabilities for guided security testing

### Key Assumptions
1. Metasploit's modular architecture allows for consistent module structure
2. CVE data combined with LLMs can generate valid Metasploit modules
3. RL agents can learn effective exploitation strategies through interaction

### Success Metrics
- Generate functional Metasploit modules from CVE descriptions
- Demonstrate automated exploitation of vulnerable targets
- Provide clear documentation and  usage examples
- Maintain security best practices throughout the development process


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

