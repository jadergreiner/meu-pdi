#!/usr/bin/env python3
"""
Script de inicializacao para o servidor FastAPI Meu PDI.
"""

import sys
import os

# Adicionar o diretorio atual ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)