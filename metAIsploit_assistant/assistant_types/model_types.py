from typing import Optional, List
from enum import StrEnum
from pydantic import BaseModel


class HackerModel(BaseModel):
    name: str
    choice_name: str
    url: str
    file_location: Optional[str]


class KnownModels(StrEnum):
    SNOOZY = "ggml-gpt4all-l13b-snoozy.bin"
    PHI2 = "phi-2.Q4_K_M.gguf"  # Example filename for quantized Phi-2


class KnownModelUrls(StrEnum):
    SNOOZY = "http://gpt4all.io/models/ggml-gpt4all-l13b-snoozy.bin"
    PHI2 = "https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf"


class OsOptions(StrEnum):
    WINDOWS = "windows"
    MAC = "mac"
    LINUX = "linux"
    KALI = "kali"


class SupportedScripts(StrEnum):
    BASH = "bash"
    PYTHON = "python"
    PIP = "pip"
    RUBY = "ruby"

    @classmethod
    def has_member(value) -> bool:
        return value in [
            SupportedScripts.BASH.value,
            SupportedScripts.PYTHON.value,
            SupportedScripts.RUBY.value,
            SupportedScripts.PIP.value,
        ]


class LlmFileOutput(BaseModel):
    file_type: SupportedScripts
    content: str


class BASE_MODELS:
    PHI2 = HackerModel(
        name=KnownModels.PHI2.value,
        choice_name=f"{KnownModels.PHI2.value} (Phi-2, Microsoft, GGUF Q4_K_M)",
        url=KnownModelUrls.PHI2.value,
        file_location="/app/models/phi-2.Q4_K_M.gguf",
    )
    # SNOOZY can be kept for fallback or removed entirely
    # SNOOZY = HackerModel(
    #     name=KnownModels.SNOOZY.value,
    #     choice_name=f"{KnownModels.SNOOZY.value} (Nomic.ai)",
    #     url=KnownModelUrls.SNOOZY.value,
    #     file_location=f"examples/models/{KnownModels.SNOOZY.value}",
    # )

    def get_model_inventory() -> List[HackerModel]:
        return [BASE_MODELS.PHI2]  # Only Phi-2 is offered by default


class MSFModuleTypes(StrEnum):
    REMOTE_EXPLOIT_CMD_STAGER = "remote_exploit_cmd_stager"
    CAPTURE_SERVER = "capture_server"
    DOS = "dos"
    SINGLE_SCANNER = "single_scanner"
    MULTI_SCANNER = "multi_scanner"


class MSFModuleCategories(StrEnum):
    AUXILIARY = "auxiliary"
    EXPLOIT = "exploit"
    POST = "post"


class MSFAuxiliaryCategories(StrEnum):
    ADMIN = "admin"
    ANALYZE = "analyze"
    CLIENT = "client"
    DOS = "dos"
    FUZZERS = "fuzzers"
    GATHER = "gather"
    SCANNER = "scanner"
    SERVER = "server"
    SNIFFER = "sniffer"


class MSFExploitCategories(StrEnum):
    ...


class MSFPostCategories(StrEnum):
    ...
