import sys
import os
from contextlib import contextmanager

@contextmanager
def suppress_stdout_stderr():
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr


try:
    from pymetasploit3.msfrpc import MsfRpcClient
    print("[DEBUG] Attempting direct msgrpc connection before imports...")
    client = MsfRpcClient(password='Meta2025SecurePass', username='msf', port=55552, server='metasploit')
    print("[DEBUG] SUCCESS: Connected to Metasploit RPC at startup!")
except Exception as e:
    print(f"[DEBUG] ERROR: msgrpc connection failed at startup: {e}")

from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import LlamaCpp
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from metAIsploit_assistant.types import BASE_MODELS
from metAIsploit_assistant.utilities.formatters import (
    has_script_in_response,
    splice_out_file,
    save_response_output_to_file,
)
from metAIsploit_assistant.utilities.models import (
    get_available_models,
    model_choices_prompt,
    model_selection,
)

from langchain_community.llms import LlamaCpp
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from metAIsploit_assistant.types import BASE_MODELS
from metAIsploit_assistant.utilities.formatters import (
    has_script_in_response,
    splice_out_file,
    save_response_output_to_file,
)
from metAIsploit_assistant.utilities.models import (
    get_available_models,
    model_choices_prompt,
    model_selection,
)
from metAIsploit_assistant.utilities.executor import MetasploitExecutor
import json
import os
from datetime import datetime


def setup_model() -> LLMChain:
    # Callbacks support token-wise streaming
    callbacks = [StreamingStdOutCallbackHandler()]

    # Fully automate: always use Phi-2, no prompt
    phi2_model = BASE_MODELS.PHI2
    print(f"[INFO] Using model: {phi2_model.choice_name} at {phi2_model.file_location}")

    with suppress_stdout_stderr():
        llm = LlamaCpp(
            model_path=phi2_model.file_location,
            callbacks=callbacks,
            verbose=True,
            n_ctx=2048,  # match model context length
            temperature=0.7,  # reasonable default
        )

    template = """You are an expert penetration tester using Metasploit. When asked to scan a target, always generate the Metasploit console command db_nmap (not shell nmap), with all required flags. For example: db_nmap -Pn -T5 --max-retries=1 <target_ip>.\n\nQuestion: {question}\n\nAnswer: Let's think step by step. Always respond with a db_nmap command if the user asks for any network scan."""

    prompt = PromptTemplate(template=template, input_variables=["question"])

    # Use the new RunnableSequence API
    return prompt | llm


def perform_chat() -> None:
    import socket
    import re
    prompt_text = None
    llm_chain = setup_model()
    executor = MetasploitExecutor()
    log_file = "chat_execution_log.json"
    session_log = []

    def automated_test_mode():
        """If METAISPLOIT_AUTOTEST=1, run a full nmap scan workflow on localhost automatically."""
        import os
        if os.environ.get("METAISPLOIT_AUTOTEST") == "1":
            print("[AUTOTEST] Running automated nmap scan on localhost...")
            # Simulate a user prompt for nmap scan
            user_prompt = "Scan DVWA and all top 1000 ports for open ports and recommend next Metasploit modules."
            target_domain = "dvwa"
            target_ip = "dvwa"
            # Scan top 1000 ports (default)
            from datetime import datetime
            import subprocess
            import shlex
            from metAIsploit_assistant.utilities.nmap_xml_utils import parse_nmap_xml, summarize_nmap_findings
            now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            xml_filename = f"nmap_{now_str}.xml"
            nmap_cmd = f"nmap -Pn -T5 --max-retries=1 -d -oX {xml_filename} {target_ip}"
            print(f"[AUTOTEST] Executing nmap: {nmap_cmd}")
            try:
                result = subprocess.run(shlex.split(nmap_cmd), capture_output=True, text=True, timeout=90)
                print(f"[AUTOTEST] nmap scan complete. Output saved to {xml_filename}\n")
                print("[AUTOTEST NMAP STDOUT]:\n" + result.stdout)
                print("[AUTOTEST NMAP STDERR]:\n" + result.stderr)
            except Exception as e:
                print(f"[AUTOTEST ERROR] nmap execution failed: {e}")
                return
            # Parse and summarize nmap XML
            parsed = parse_nmap_xml(xml_filename)
            summary = summarize_nmap_findings(parsed)
            print("[AUTOTEST] Nmap scan summary:")
            print(summary)
            # Ask LLM for Metasploit scan recommendations
            rec_prompt = f"Given this nmap scan summary, recommend the next Metasploit auxiliary or scanner modules (with options) to run for further enumeration. Only suggest valid Metasploit modules and API options.\n\nScan Summary:\n{summary}"
            rec_response_obj = llm_chain.invoke({'question': rec_prompt})
            rec_response = rec_response_obj['text'] if isinstance(rec_response_obj, dict) and 'text' in rec_response_obj else str(rec_response_obj)
            print("\n[AUTOTEST LLM Recommendations for Metasploit Scans]:\n" + rec_response)
            print("[AUTOTEST] Done.")
            exit(0)

    automated_test_mode()

    while prompt_text != "exit":
        prompt_text = input("\nWhat do you want to know? (enter: exit to stop): ")
        if prompt_text == "exit":
            break

        # Try to extract a domain from the prompt
        domain_regex = r"([a-zA-Z0-9][-a-zA-Z0-9]*\.[a-zA-Z]{2,})(?![\w.])"
        domain_match = re.search(domain_regex, prompt_text)
        if domain_match:
            target_domain = domain_match.group(1)
            print(f"[INFO] Extracted domain from prompt: {target_domain}")
        else:
            # Prompt for domain if not found in prompt
            while True:
                target_domain = input("Enter the target domain for this request: ").strip()
                if target_domain:
                    break
        # Try to resolve domain to IP
        while True:
            try:
                target_ip = socket.gethostbyname(target_domain)
                print(f"[INFO] Resolved {target_domain} to {target_ip}")
                break
            except Exception as e:
                print(f"[ERROR] Could not resolve domain: {e}")
                target_domain = input("Enter a valid target domain: ").strip()

        llm_response_obj = llm_chain.invoke({'question': prompt_text})
        llm_response = llm_response_obj['text'] if isinstance(llm_response_obj, dict) and 'text' in llm_response_obj else str(llm_response_obj)
        print(f"\n[LLM Response]:\n{llm_response}\n")
        session_log.append({
            "timestamp": datetime.now().isoformat(),
            "user_prompt": prompt_text,
            "llm_response": llm_response,
            "target_domain": target_domain,
            "target_ip": target_ip
        })

        # Check if the user wants to run an nmap shell command
        if "nmap" in llm_response.lower() and ("shell" in llm_response.lower() or "terminal" in llm_response.lower()):
            shell_command = None
            # Nmap workflow: run nmap with -d (debug), show raw output, analyze XML, get LLM recommendations
            import subprocess
            import shlex
            from metAIsploit_assistant.utilities.nmap_xml_utils import parse_nmap_xml, summarize_nmap_findings
            now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            xml_filename = f"nmap_{now_str}.xml"
            nmap_cmd = f"nmap -Pn -T5 --max-retries=1 -d -oX {xml_filename} {target_ip}"
            print(f"[INFO] Executing nmap: {nmap_cmd}")
            try:
                result = subprocess.run(shlex.split(nmap_cmd), capture_output=True, text=True, timeout=90)
                print(f"[INFO] nmap scan complete. Output saved to {xml_filename}\n")
                print("[NMAP STDOUT]:\n" + result.stdout)
                print("[NMAP STDERR]:\n" + result.stderr)
                session_log[-1]["nmap_scan"] = {
                    "success": result.returncode == 0,
                    "command": nmap_cmd,
                    "output_file": xml_filename,
                    "stdout": result.stdout[:2000],
                    "stderr": result.stderr[:2000]
                }
            except Exception as e:
                print(f"[ERROR] nmap execution failed: {e}")
                session_log[-1]["nmap_scan"] = {"success": False, "error": str(e)}
                with open(log_file, "w") as f:
                    json.dump(session_log, f, indent=2)
                return
            # Parse and summarize nmap XML
            parsed = parse_nmap_xml(xml_filename)
            summary = summarize_nmap_findings(parsed)
            print("[INFO] Nmap scan summary:")
            print(summary)
            # Ask LLM for Metasploit scan recommendations
            rec_prompt = f"Given this nmap scan summary, recommend the next Metasploit auxiliary or scanner modules (with options) to run for further enumeration. Only suggest valid Metasploit modules and API options.\n\nScan Summary:\n{summary}"
            rec_response_obj = llm_chain.invoke({'question': rec_prompt})
            rec_response = rec_response_obj['text'] if isinstance(rec_response_obj, dict) and 'text' in rec_response_obj else str(rec_response_obj)
            print("\n[LLM Recommendations for Metasploit Scans]:\n" + rec_response)
            session_log[-1]["llm_recommendations"] = {
                "prompt": rec_prompt,
                "response": rec_response
            }
            with open(log_file, "w") as f:
                json.dump(session_log, f, indent=2)
        else:
            # Prompt for Metasploit execution as before
            exec_prompt = input("Would you like to execute this as a Metasploit command? (y/n): ")
            if exec_prompt.strip().lower() in ["y", "yes"]:
                success, output, error = executor.execute_command(llm_response)
                print("\n[Metasploit Output]:")
                if success:
                    print(output)
                else:
                    print(f"[ERROR]: {error}")
                session_log[-1]["execution"] = {
                    "success": success,
                    "output": output,
                    "error": error
                }
                # Save log after each execution
                with open(log_file, "w") as f:
                    json.dump(session_log, f, indent=2)

        # Existing code for script extraction and file saving
        if has_script_in_response(llm_response):
            script_cut_out = splice_out_file(llm_response)
            for cut_out in script_cut_out:
                save_to_file = input(
                    f"\nWould you like to save the {cut_out.file_type} script to a file? (y/n)"
                )
                if save_to_file == "y" or save_to_file == "yes":
                    os_system = input("System Type: (windows/mac/linux): ")
                    save_filename = input(
                        f"""\n{cut_out.content}\nWhere would you like to save the file (file endings will be added automatically)? (default: <METASPLOIT_ROOT>/modules/linux/custom/default_output.py) """
                    )
                    if save_filename == "":
                        save_filename = "default_output.py"
                    save_response_output_to_file(cut_out, save_filename, os_system)

    print("\nHappy Hacking!")

if __name__ == "__main__":
    perform_chat()
