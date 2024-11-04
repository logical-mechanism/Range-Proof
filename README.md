# zkInterval: Trustless, Confidential, Fixed-Size Range Proofs

In this repo, we introduce zkInterval, a zero-knowledge range proof protocol that delivers trustless fixed-size proofs regardless of the interval size. Combining Pedersen commitments with zero-knowledge proofs, zkInterval securely confirms that a value is within a public interval without revealing the value in the process.

## tl;dr

The zkInterval protocol proves the statement $a \geq d \geq b$ where $a$ and $b$ are public, $a \geq b$, and $a, b, d \in \mathbb{Z}^+$. It does not require a trusted setup, is completely confidential, and each proof is fixed-size no matter that interval size.

## In This Repo

Python code for generating the proofs and Aiken code for on-chain validation of the proofs. The on-chain Cardano json form of the proof is about 2.1 Kb. The proof can be compressed to 992 bytes as a single string if required.

Current memory and steps estimate with Aiken:

```
[mem: 116670, cpu: 2687440785]
```

Estimate cost is about 200,000 Lovelace to compute on-chain.

## The Paper

[The Paper](paper/zkInterval-2024.pdf) describing the derivation of zkInterval.
