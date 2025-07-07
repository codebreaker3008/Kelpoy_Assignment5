import subprocess
from pathlib import Path

CONTROLLERS = [
    "AuthController",
    "PersonsController",
    "DepartmentsController",
    "JobsController"
]

def run_ollama(prompt_file: str, code_file: str, model="tinyllama") -> str:
    prompt = Path(prompt_file).read_text()
    code = Path(code_file).read_text()
    full_prompt = prompt + "\n\n" + code
    result = subprocess.run(
        ["ollama", "run", model],
        input=full_prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode()

def main():
    prompt_file = "initial_prompt.yaml"
    for controller in CONTROLLERS:
        input_path = f"orgChartApi/controllers/{controller}.cc"
        output_path = f"tests/test_{controller}.cpp"
        print(f"🔄 Generating tests for {controller}...")
        result = run_ollama(prompt_file, input_path)
        Path(output_path).write_text(result)

if __name__ == "__main__":
    main()
