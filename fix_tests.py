import subprocess
from pathlib import Path

def run_fix_llm(prompt_file: str, code_file: str, log_file: str, model: str = "tinyllama") -> str:
    try:
        prompt = Path(prompt_file).read_text()
        code = Path(code_file).read_text()
        logs = Path(log_file).read_text()

        full_prompt = (
            f"{prompt}\n\n"
            f"[BUILD LOGS]\n{logs}\n\n"
            f"[BROKEN TEST FILE]\n{code}"
        )

        result = subprocess.run(
            ["ollama", "run", model],
            input=full_prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return result.stdout.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] LLM call failed:\n{e.stderr.decode()}")
        return ""
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return ""

def main():
    code_file = "tests/test_AuthController_refined.cpp"
    log_file = "build.log"
    prompt_file = "build_fix_prompt.yaml"
    fixed_file = "tests/test_AuthController_fixed.cpp"

    print(f"🛠️ Fixing broken tests using logs...")
    output = run_fix_llm(prompt_file, code_file, log_file)

    if output:
        Path(fixed_file).write_text(output)
        print(f"✅ Fixed test written to: {fixed_file}")
    else:
        print("❌ Fix failed. No output generated.")

if __name__ == "__main__":
    main()
