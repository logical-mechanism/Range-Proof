import argparse
import json

from src.range import Range
from src.bls12_381 import curve_order


def save_proof_to_json(data: dict, file_path: str) -> None:
    # Write the proof data to the JSON file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def zk_data(proof: dict, lower: int, upper: int, file_path: str) -> None:
    data = {
        "constructor": 0,
        "fields": [
            {
                "constructor": 0,
                "fields": [
                    {"bytes": proof["Y"]},
                    {"bytes": proof["D"]},
                    {"bytes": proof["R"]},
                    {"bytes": proof["A"]},
                    {"bytes": proof["B"]},
                    {"bytes": proof["W"]},
                    {"bytes": proof["L"]},
                ],
            },
            {
                "constructor": 0,
                "fields": [{"bytes": proof["Za"]}, {"bytes": proof["ac"]}],
            },
            {
                "constructor": 0,
                "fields": [{"bytes": proof["Zb"]}, {"bytes": proof["bc"]}],
            },
            {"int": upper},
            {"int": lower},
        ],
    }
    save_proof_to_json(data, file_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a range proof based on a value, lower bound, and upper bound.\n\n"
            "Example:\n"
            "python3 zk_interval.py -v 42 -l 0 -u 100 -f datum.json\n"
            "python3 zk_interval.py --value 42 --lower 0 --upper 100 --file_path datum.json"
        ),
        formatter_class=argparse.RawTextHelpFormatter,  # Preserve formatting
        epilog=(
            f"Ensure that the value falls within the specified lower and upper bounds.\n\n"
            f"Maximum Valid Range: 0 ≤ value ≤ {curve_order-1}"
        )
    )

    # Define arguments
    parser.add_argument(
        "-v", "--value", type=int, required=True, help="The secret value to prove", metavar="VALUE"
    )
    parser.add_argument(
        "-l", "--lower", type=int, required=True, help="The lower bound of the interval", metavar="LOWER_BOUND"
    )
    parser.add_argument(
        "-u", "--upper", type=int, required=True, help="The upper bound of the interval", metavar="UPPER_BOUND"
    )
    parser.add_argument(
        "-f", "--file_path", type=str, required=True, help="Path to the datum file", metavar="FILE_PATH"
    )

    # Parse arguments
    args = parser.parse_args()

    # Create Range object and generate proof
    print(f"Prove: {args.upper} >= {args.value} >= {args.lower}")
    r = Range(secret_value=args.value, lower_bound=args.lower, upper_bound=args.upper)
    proof = r.generate_proof()
    print(f"Is the Proof Valid? {r.verify_proof(proof, args.lower, args.upper)}")
    zk_data(proof, args.lower, args.upper, args.file_path)


if __name__ == "__main__":
    main()
