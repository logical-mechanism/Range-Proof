# ZK Interval Proof Generation

# Setup

```bash
# Create a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required Python packages
pip install -r requirements.txt
```

# Test

Use `pytest` for testing.

```bash
pytest
```

# Use

The python script `zk_interval.py` is designed to output the datum / redeemer file for a smart contract.

```bash
python3 zk_interval.py --value 42 --lower 0 --upper 100 --file_path datum.json
```