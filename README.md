# zkInterval: Trustless, Confidential, Fixed-Size Range Proofs

In this repo, we introduce zkInterval, a novel zero-knowledge range proof protocol that delivers fixed-size proofs regardless of the interval size. Combining Pedersen commitments with zero-knowledge proofs, zkInterval securely confirms that a value is within a public interval without revealing it or requiring a trusted setup. The consistent proof size irrespective of the interval length significantly reduces storage, making zkInterval particularly well-suited for privacy-focused applications with variable interval lengths.

## TL;DR

The zkInterval protocol proves the statement $a \geq d \geq b$ where $a$ and $b$ are public, $a \geq b$, and $a, b, d \in \mathbb{Z}^+$. It does not require a trusted setup, is completely confidential, and each proof is fixed-size no matter that interval size.

## In This Repo

Python code for generating the proofs and Aiken code for on-chain validation of the proofs. The on-chain Cardano form of the proof is about 2.2 Kb.

Current memory and steps estimate with Aiken:

```
[mem: 100336, cpu: 2226339408]

0.0577 * 100336 + 0.0000721 * 2226339408 = 166308
```

Estimate cost is about 167,000 Lovelace to compute on-chain.

## The Paper

[The Paper](paper/zkInterval-2024.pdf) describing the derivation of zkInterval.
