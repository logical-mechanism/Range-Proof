# zkInterval: Trustless, Confidential, Fixed-Size Range Proofs

In this repo, we introduce zkInterval, a novel zero-knowledge range proof protocol that delivers fixed-size proofs regardless of the interval size. Combining Pedersen commitments with zero-knowledge proofs, zkInterval securely confirms that a value is within a public interval without revealing it or requiring a trusted setup. The consistent proof size irrespective of the interval length significantly reduces storage, making zkInterval particularly well-suited for privacy-focused applications with variable interval lengths.

## TL;DR

The zkInterval protocol proves the statement $a \geq d \geq b$ where $a$ and $b$ are public, $a \geq b$, and $a, b, d \in \mathbb{Z}^+$. It does not require a trusted setup, is completely confidential, and each proof is fixed-size no matter that interval size.

## In This Repo

### Python

Python code for generating the proofs and Aiken code for on-chain validation of the proofs. The on-chain Cardano form of the proof is about 2.2 Kb.

```bash
# Prove: 100 >= 42 >= 0
python3 zk_interval.py --value 42 --lower 0 --upper 100 --file_path datum.json
```

The python code requires a venv.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Aiken

Import the library with the command:

```bash
aiken packages add logical-mechanism/Range-Proof --version main
```

```rust
use zk_interval.{ZKInterval, prove}
```

Compile your project by running the command `aiken check` in your project directory. If a complete recheck is required then run the command:

```bash
rm -fr build || true
aiken check
```

Current memory and steps estimate with Aiken:

```bash
[mem: 100_336, cpu: 2_226_339_408]

0.0577 * 100336 + 0.0000721 * 2226339408 = 166308 Lovelace
```

Estimate cost is about 166,308 Lovelace to compute on-chain.

## The Paper

[The Paper](paper/zkInterval-2024.pdf) describing the derivation of zkInterval.

Building out the paper:
```bash
pdflatex zkInterval-2025.tex
bibtex zkInterval-2025
pdflatex zkInterval-2025.tex
pdflatex zkInterval-2025.tex
```