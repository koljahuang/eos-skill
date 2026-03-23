"""
Main entry point for EOS scan.
Called by the skill or CLI.
"""

import argparse
import sys
from datetime import datetime
from .scanners import run_scan, SCANNERS
from .report import generate_report


VALID_RESOURCE_TYPES = list(SCANNERS.keys())


def main():
    parser = argparse.ArgumentParser(
        description="AWS End-of-Support Resource Scanner"
    )
    parser.add_argument(
        "--accounts",
        required=True,
        nargs="+",
        help="AWS account ID(s) to scan",
    )
    parser.add_argument(
        "--regions",
        required=True,
        nargs="+",
        help="AWS region(s) to scan (e.g. us-east-1 ap-northeast-1)",
    )
    parser.add_argument(
        "--resource-types",
        nargs="+",
        default=VALID_RESOURCE_TYPES,
        choices=VALID_RESOURCE_TYPES,
        help=f"Resource types to scan (default: all). Options: {VALID_RESOURCE_TYPES}",
    )
    # Authentication options
    auth_group = parser.add_mutually_exclusive_group()
    auth_group.add_argument(
        "--profile",
        default=None,
        help="AWS CLI profile name (e.g. my-profile)",
    )
    auth_group.add_argument(
        "--access-key",
        default=None,
        help="AWS Access Key ID (must also provide --secret-key)",
    )
    parser.add_argument(
        "--secret-key",
        default=None,
        help="AWS Secret Access Key (used with --access-key)",
    )
    parser.add_argument(
        "--role-name",
        default="OrganizationAccountAccessRole",
        help="IAM role name for cross-account access (default: OrganizationAccountAccessRole)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output Excel file path (default: eos_report_<timestamp>.xlsx)",
    )

    args = parser.parse_args()

    # Validate AK/SK pair
    if args.access_key and not args.secret_key:
        parser.error("--secret-key is required when using --access-key")
    if args.secret_key and not args.access_key:
        parser.error("--access-key is required when using --secret-key")

    if args.output is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"eos_report_{ts}.xlsx"

    auth_method = "AK/SK" if args.access_key else (f"profile:{args.profile}" if args.profile else "default credentials")
    print(f"EOS Scanner")
    print(f"  Auth:           {auth_method}")
    print(f"  Accounts:       {args.accounts}")
    print(f"  Regions:        {args.regions}")
    print(f"  Resource Types: {args.resource_types}")
    print(f"  Role Name:      {args.role_name}")
    print(f"  Output:         {args.output}")
    print()

    rows = run_scan(
        accounts=args.accounts,
        regions=args.regions,
        resource_types=args.resource_types,
        role_name=args.role_name,
        profile=args.profile,
        access_key=args.access_key,
        secret_key=args.secret_key,
    )

    if not rows:
        print("\nNo resources found.")
        sys.exit(0)

    output = generate_report(rows, args.output)
    print(f"\nReport generated: {output}")
    print(f"Total resources: {len(rows)}")


if __name__ == "__main__":
    main()
