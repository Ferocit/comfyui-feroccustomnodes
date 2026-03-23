"""pytest configuration: expose project modules for direct import in tests."""
import sys
import os

# Add project root to sys.path so test files can import modules directly
sys.path.insert(0, os.path.dirname(__file__))
