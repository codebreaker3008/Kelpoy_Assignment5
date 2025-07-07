#!/bin/bash

set -e
CONTROLLERS=("AuthController" "PersonsController" "DepartmentsController" "JobsController")

echo "🧪 Generating tests for all controllers"
python3 generate_tests.py

echo "🧹 Refining tests"
python3 refine_tests.py

echo "🏗️ Building project"
mkdir -p build && cd build
cmake -DCMAKE_CXX_FLAGS="--coverage" ..
if ! make | tee ../build.log; then
    echo "❌ Build failed. Attempting fixes..."
    cd ..
    python3 fix_tests.py
    echo "🔁 Rebuilding with fixed tests..."
    for controller in "${CONTROLLERS[@]}"; do
        cp "tests/test_${controller}_fixed.cpp" "tests/test_${controller}.cpp"
    done
    cd build
    make | tee ../build.log
fi

echo "✅ Build passed"

echo "📊 Running tests and collecting coverage"
cd ..
cd build
ctest || true
lcov --capture --directory . --output-file coverage.info
genhtml coverage.info --output-directory ../coverage
cd ..

echo "✅ Coverage generated at coverage/index.html"
xdg-open coverage/index.html 2>/dev/null || echo "📂 Open coverage/index.html manually"
