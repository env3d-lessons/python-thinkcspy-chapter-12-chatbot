#!/bin/bash
export LLAMA_CPP_LIB=/workspaces/$(basename $(pwd))/.devcontainer/libllama.so
pip install llama-cpp-python --no-build-isolation --no-cache-dir

# wget https://huggingface.co/Qwen/Qwen3-0.6B-GGUF/resolve/main/Qwen3-0.6B-Q8_0.gguf
# smallest qwen model
wget https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q2_k.gguf

echo ""
echo "✅ DevContainer setup complete!"
echo "You can now start working on your assignment."