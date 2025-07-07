# 🚀 C++ Unit Test Generator using LLM (Ollama + GoogleTest)

This project auto-generates unit tests for a Drogon-based C++ REST API (`orgChartApi`) using a locally hosted Large Language Model (LLM) like `tinyllama` via [Ollama](https://ollama.com/).

---

## 📁 Folder Structure

cpp-unit-test-gen/
├── orgChartApi/ # Original source code (controllers/)
│ └── controllers/
│ ├── AuthController.cc
│ ├── PersonsController.cc
│ └── ...
├── tests/ # Generated + refined GoogleTest files
│ └── test_AuthController.cpp
├── prompts/
│ ├── initial_prompt.yaml # Prompt for test generation
│ └── refine_prompt.yaml # Prompt for test refinement
├── generate_tests.py # LLM-based test generation script
├── refine_tests.py # LLM-based test refinement script
├── run_pipeline.sh # Full pipeline to run everything
├── CMakeLists.txt # Build configuration
└── README.md # This file

yaml
Copy
Edit

---

## 🧱 Prerequisites

- ✅ CMake (≥ 3.10)
- ✅ GCC with `--coverage` support
- ✅ Python 3.8+
- ✅ [Ollama](https://ollama.com/) + `tinyllama` model:
  ```bash
  ollama pull tinyllama
✅ GoogleTest installed system-wide

⚙️ Setup
bash
Copy
Edit
# Clone repo and navigate
cd cpp-unit-test-gen

# Optional: Create build directory
mkdir -p build
▶️ Run the Full Pipeline
This will:

🧪 Generate unit tests from source

🧹 Refine them

🏗️ Build with CMake

✅ Run all tests

📊 Show coverage (if available)

bash
Copy
Edit
./run_pipeline.sh
You should see output like:

bash
Copy
Edit
✅ Saved test: tests/test_AuthController.cpp
✅ Saved refined test: tests/test_AuthController.cpp
[==========] Running 1 test from 1 test suite.
[  PASSED  ] 1 test.
🧪 Run Tests Only
bash
Copy
Edit
cd build
./runTests
📈 Generate Code Coverage Report
bash
Copy
Edit
# Generate coverage info
lcov --capture --directory . --output-file coverage.info

# Generate HTML report
genhtml coverage.info --output-directory coverage/

# View in browser
xdg-open coverage/index.html
🔍 Debugging Tips
If test generation fails: check tmp/refine_failed_*.txt

If tests are skipped: your prompt or LLM response may not contain #include or TEST(...)

If no coverage: ensure you built with --coverage and ran runTests

🧠 Example LLM Prompt Files
See prompts/initial_prompt.yaml and refine_prompt.yaml for examples of what is sent to the LLM.

You can tweak the prompts to:

Add test structure

Add mocking behavior

Change assertion styles

📬 Maintainer
Built for the Keploy AI Fellowship - Session 5
Author: Ayush @MK001