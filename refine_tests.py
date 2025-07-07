import subprocess
from pathlib import Path
import re

CONTROLLERS = [
    "AuthController",
    "PersonsController",
    "DepartmentsController",
    "JobsController"
]

def run_ollama(prompt_file: str, test_file: str, model="tinyllama") -> str:
    prompt = Path(prompt_file).read_text()
    test_code = Path(test_file).read_text()
    full_prompt = prompt + "\n\n" + test_code
    result = subprocess.run(
        ["ollama", "run", model],
        input=full_prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode()

def clean_llm_output(text: str) -> str:
    # Remove markdown-style blocks
    text = re.sub(r"```(?:cpp)?\n(.*?)\n```", r"\1", text, flags=re.DOTALL)
    text = re.sub(r"^[-*]\s+", "", text, flags=re.MULTILINE)
    text = text.replace("`", "")

    # Remove everything before the first valid C++ line
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines)
                  if re.match(r'^\s*(#include|TEST|TEST_F|class)', line)), -1)
    return "\n".join(lines[start:]) if start != -1 else ""

def main():
    prompt_file = "refine_prompt.yaml"
    Path("tmp").mkdir(exist_ok=True)

    for controller in CONTROLLERS:
        input_file = f"tests/test_{controller}.cpp"
        output_file = f"tests/test_{controller}.cpp"

        print(f"🧹 Refining {input_file}...")

        raw_output = run_ollama(prompt_file, input_file)
        Path(f"tmp/raw_refine_{controller}.txt").write_text(raw_output)

        cleaned_output = clean_llm_output(raw_output)

        if "#include" in cleaned_output and "TEST" in cleaned_output:
            Path(output_file).write_text(cleaned_output)
            print(f"✅ Saved refined test: {output_file}")
        else:
            print(f"❌ Skipped {controller} — output not valid C++ test.")
            Path(f"tmp/refine_failed_{controller}.txt").write_text(cleaned_output)

if __name__ == "__main__":
    main()
