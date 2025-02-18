import argparse
import json

from src.range import Range


def save_proof_to_json(data: dict, file_path: str) -> None:

    # Write the proof data to the JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def zk_data(proof: dict, lower: int, upper: int, file_path: str) -> None:
    data = {
        "constructor": 0,
        "fields": [
            {
                "constructor": 0,
                "fields": [
                    {
                        "bytes": proof["Y"]
                    },
                    {
                        "bytes": proof["D"]
                    },
                    {
                        "bytes": proof["R"]
                    },
                    {
                        "bytes": proof["A"]
                    },
                    {
                        "bytes": proof["B"]
                    },
                    {
                        "bytes": proof["W"]
                    },
                    {
                        "bytes": proof["L"]
                    }
                ]
            },
            {
                "constructor": 0,
                "fields": [
                    {
                        "bytes": proof["Za"]
                    },
                    {
                        "bytes": proof["ac"]
                    }
                ]
            },
            {
                "constructor": 0,
                "fields": [
                    {
                        "bytes": proof["Zb"]
                    },
                    {
                        "bytes": proof["bc"]
                    }
                ]
            },
            {
                "int": upper
            },
            {
                "int": lower
            }
        ]
    }
    save_proof_to_json(data, file_path)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a proof based on a value, lower bound, and upper bound.")

    # Define arguments
    parser.add_argument('--value', type=int, required=True,
                        help='The secret value')
    parser.add_argument('--lower', type=int, required=True,
                        help='The lower bound')
    parser.add_argument('--upper', type=int, required=True,
                        help='The upper bound')
    parser.add_argument('--file_path', type=str, required=True,
                        help='The datum file path')

    # Parse arguments
    args = parser.parse_args()

    # Create Range object and generate proof
    print(f"Prove {args.upper} >= {args.value} >= {args.lower}")
    r = Range(secret_value=args.value,
              lower_bound=args.lower, upper_bound=args.upper)
    proof = r.generate_proof()
    print('Is the Proof Valid?', r.verify_proof(proof, args.lower, args.upper))

    zk_data(proof, args.lower, args.upper, args.file_path)


if __name__ == "__main__":
    main()
