# zkInterval Proof Generation

# Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Test

Use `pytest` for testing.

```bash
pytest
```


# Use

Use `zk_interval.py` to generate proofs.

```bash
# Prove: 100 >= 42 >= 0
python3 zk_interval.py --value 42 --lower 0 --upper 100 --file_path datum.json
```