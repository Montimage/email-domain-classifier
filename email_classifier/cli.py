#!/usr/bin/env python3
"""Email Domain Classifier CLI.

A command-line tool for classifying emails by domain using
dual-method validation (keyword taxonomy + structural templates).

Usage:
    email-cli input.csv -o output_dir/
    email-cli classify input.csv -o output_dir/ --verbose
    email-cli info input.csv
    email-cli info input.csv --json
"""

import argparse
import json
import logging
import sys
from pathlib import Path

from .analyzer import DatasetAnalyzer
from .classifier import EmailClassifier
from .domains import get_domain_names
from .processor import StreamingProcessor
from .reporter import ClassificationReporter
from .ui import RICH_AVAILABLE, get_ui


def setup_logging(log_file: Path, verbose: bool = False) -> logging.Logger:
    """Configure logging to file and optionally console."""
    logger = logging.getLogger("email_classifier")
    logger.setLevel(logging.DEBUG)

    # File handler - always detailed
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # Console handler - only if verbose
    if verbose:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)

    return logger


def validate_input(input_path: Path) -> bool:
    """Validate input file exists and is readable."""
    if not input_path.exists():
        return False
    if not input_path.is_file():
        return False
    if input_path.suffix.lower() != ".csv":
        return False
    return True


def cmd_info(args: argparse.Namespace) -> int:
    """Execute the info command to analyze a dataset."""
    ui = get_ui(quiet=args.quiet)

    # Validate input file
    input_path = Path(args.input).resolve()
    if not input_path.exists():
        if args.json:
            print(json.dumps({"error": f"File not found: {args.input}"}))
        else:
            ui.print_error(f"File not found: {args.input}")
        return 1

    if input_path.suffix.lower() != ".csv":
        if args.json:
            print(json.dumps({"error": "Invalid file type. Expected .csv file"}))
        else:
            ui.print_error("Invalid file type. Expected .csv file")
        return 1

    # Initialize analyzer
    analyzer = DatasetAnalyzer(allow_large_fields=args.allow_large_fields)

    # Progress callback for terminal
    def progress_callback(current: int, total: int, status: str) -> None:
        if not args.quiet and not args.json and RICH_AVAILABLE:
            # Progress is handled by the UI
            pass

    try:
        # Run analysis
        if not args.quiet and not args.json:
            ui.print_info(f"Analyzing {input_path.name}...")

        if RICH_AVAILABLE and not args.quiet and not args.json:
            progress = ui.create_progress()
            task_id = None

            def rich_progress(current: int, total: int, status: str) -> None:
                nonlocal task_id
                if progress is not None:
                    if task_id is None and total > 0:
                        task_id = progress.add_task(
                            "[cyan]Analyzing dataset...", total=total
                        )
                    if task_id is not None:
                        progress.update(
                            task_id, completed=current, description=f"[cyan]{status}"
                        )

            with progress:
                result = analyzer.analyze(input_path, progress_callback=rich_progress)
        else:
            result = analyzer.analyze(input_path, progress_callback=progress_callback)

        # Output results
        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            ui.print_analysis_report(result)

        return 0

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            ui.print_error(f"Analysis failed: {e}")
        return 1


def cmd_classify(args: argparse.Namespace) -> int:
    """Execute the classify command."""
    # Initialize UI
    ui = get_ui(quiet=args.quiet)

    # Display banner
    if not args.quiet:
        ui.print_banner()

    # Validate input file
    input_path = Path(args.input).resolve()
    if not validate_input(input_path):
        ui.print_error(f"Invalid input file: {args.input}")
        ui.print_info("File must exist and have .csv extension")
        return 1

    # Setup output directory
    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Setup logging
    log_file = (
        Path(args.log_file) if args.log_file else output_dir / "classification.log"
    )
    logger = setup_logging(log_file, verbose=args.verbose)

    logger.info("=" * 60)
    logger.info("EMAIL DOMAIN CLASSIFIER - Started")
    logger.info("=" * 60)
    logger.info(f"Input file: {input_path}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Chunk size: {args.chunk_size}")
    logger.info(f"Include details: {args.include_details}")
    logger.info(f"Strict validation: {args.strict_validation}")
    if args.max_body_length:
        logger.info(f"Max body length: {args.max_body_length}")

    # Display configuration
    if not args.quiet:
        config_opts = {
            "Chunk Size": args.chunk_size,
            "Include Details": args.include_details,
            "Strict Validation": args.strict_validation,
            "Log File": str(log_file),
        }
        if args.max_body_length:
            config_opts["Max Body Length"] = f"{args.max_body_length:,} chars"
        ui.print_config(
            str(input_path),
            str(output_dir),
            config_opts,
        )

    # Initialize components
    classifier = EmailClassifier()
    processor = StreamingProcessor(
        classifier=classifier,
        chunk_size=args.chunk_size,
        logger=logger,
        allow_large_fields=args.allow_large_fields,
        strict_validation=args.strict_validation,
        max_body_length=args.max_body_length,
    )

    # Process emails with progress tracking
    try:
        if RICH_AVAILABLE and not args.quiet:
            # Use Rich progress bar
            progress = ui.create_progress()
            task_id = None

            def progress_callback(current: int, total: int, status: str) -> None:
                nonlocal task_id
                if progress is not None:
                    if task_id is None and total > 0:
                        task_id = progress.add_task(
                            "[cyan]Classifying emails...", total=total
                        )
                    if task_id is not None:
                        progress.update(
                            task_id, completed=current, description=f"[cyan]{status}"
                        )

            with progress:
                stats = processor.process(
                    input_path=input_path,
                    output_dir=output_dir,
                    progress_callback=progress_callback,
                    include_details=args.include_details,
                )
        else:
            # Simple progress for non-Rich environments
            def simple_progress(current: int, total: int, status: str) -> None:
                if hasattr(ui, "print_progress"):
                    ui.print_progress(current, total, status)

            stats = processor.process(
                input_path=input_path,
                output_dir=output_dir,
                progress_callback=simple_progress if not args.quiet else None,
                include_details=args.include_details,
            )

        logger.info("Processing completed successfully")

    except KeyboardInterrupt:
        ui.print_warning("Processing interrupted by user")
        logger.warning("Processing interrupted by user")
        return 130
    except Exception as e:
        ui.print_error(f"Processing failed: {e}")
        logger.exception("Processing failed with exception")
        return 1

    # Generate reports
    if not args.no_report:
        reporter = ClassificationReporter()
        report = reporter.generate_report(
            stats=stats, output_dir=output_dir, input_file=str(input_path)
        )

        # Save JSON report
        json_report_path = output_dir / "classification_report.json"
        reporter.save_json_report(report, json_report_path)
        logger.info(f"JSON report saved: {json_report_path}")

        # Save text report
        if not args.json_only:
            text_report_path = output_dir / "classification_report.txt"
            reporter.save_text_report(report, text_report_path)
            logger.info(f"Text report saved: {text_report_path}")

        # Display results in terminal
        if not args.quiet:
            ui.print_domain_stats(
                dict(stats.domain_counts),
                stats.total_processed,
                report,
                input_file=input_path.name,
            )
            ui.print_summary_panel(report)

            # Show output files
            file_counts = processor.get_output_summary(output_dir)
            ui.print_output_files(output_dir, file_counts)

            # Show recommendations
            if "recommendations" in report:
                ui.print_recommendations(report["recommendations"])

    # Final success message
    if not args.quiet:
        ui.print_success("Classification complete!")
        ui.print_info(f"Results saved to: {output_dir}")

    logger.info("=" * 60)
    logger.info("EMAIL DOMAIN CLASSIFIER - Finished")
    logger.info("=" * 60)

    return 0


def main() -> int:
    """Execute main CLI entry point with subcommand support."""
    # Create main parser
    parser = argparse.ArgumentParser(
        prog="email-cli",
        description="Classify emails by domain using dual-method validation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  classify    Classify emails in a CSV file by domain (default)
  info        Analyze a dataset and display statistics

Examples:
  email-cli emails.csv -o classified/
  email-cli classify data/input.csv -o results/ --verbose
  email-cli info emails.csv
  email-cli info emails.csv --json

For command-specific help:
  email-cli classify --help
  email-cli info --help
        """,
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    # Handle --list-domains early (before subparsers)
    if "--list-domains" in sys.argv:
        print("\nSupported Domain Categories:")
        print("-" * 40)
        for domain in get_domain_names():
            print(f"  • {domain}")
        print()
        return 0

    # Create subparsers
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # =========================================================================
    # INFO subcommand
    # =========================================================================
    info_parser = subparsers.add_parser(
        "info",
        help="Analyze a dataset and display statistics",
        description="Analyze a CSV dataset and display comprehensive statistics.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  email-cli info emails.csv
  email-cli info emails.csv --json
  email-cli info dataset.csv --no-large-fields  # Restrict to small fields only
        """,
    )

    info_parser.add_argument(
        "input", type=str, help="Path to input CSV file to analyze"
    )

    info_parser.add_argument(
        "--json",
        action="store_true",
        help="Output analysis results in JSON format",
    )

    info_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress progress output (still outputs JSON if --json is set)",
    )

    info_parser.add_argument(
        "--no-large-fields",
        dest="allow_large_fields",
        action="store_false",
        default=True,
        help="Disable processing of CSV fields larger than default limit (131KB)",
    )

    # =========================================================================
    # CLASSIFY subcommand
    # =========================================================================
    classify_parser = subparsers.add_parser(
        "classify",
        help="Classify emails in a CSV file by domain",
        description="Classify emails by domain using dual-method validation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  email-cli classify emails.csv -o classified/
  email-cli classify data/input.csv --output results/ --verbose
  email-cli classify emails.csv -o output/ --include-details --chunk-size 500

Output:
  Creates email_[domain].csv files for each detected domain,
  plus email_unsure.csv for unclassified emails.
  Also generates classification_report.txt and classification_report.json.
        """,
    )

    # Required arguments
    classify_parser.add_argument(
        "input", type=str, help="Path to input CSV file containing email dataset"
    )

    # Output options
    classify_parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Output directory for classified email files",
    )

    # Processing options
    classify_parser.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="Number of emails to process before logging progress (default: 1000)",
    )

    classify_parser.add_argument(
        "--include-details",
        action="store_true",
        help="Include detailed classification scores in output files",
    )

    # Logging options
    classify_parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose console output"
    )

    classify_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress all console output except errors",
    )

    classify_parser.add_argument(
        "--log-file",
        type=str,
        default=None,
        help="Custom log file path (default: output_dir/classification.log)",
    )

    # Report options
    classify_parser.add_argument(
        "--no-report", action="store_true", help="Skip generating summary reports"
    )

    classify_parser.add_argument(
        "--json-only",
        action="store_true",
        help="Generate only JSON report (no text report)",
    )

    # Misc options
    classify_parser.add_argument(
        "--list-domains",
        action="store_true",
        help="List all supported domain categories and exit",
    )

    classify_parser.add_argument(
        "--no-large-fields",
        dest="allow_large_fields",
        action="store_false",
        default=True,
        help="Disable processing of CSV fields larger than default limit (131KB)",
    )

    # Validation options
    classify_parser.add_argument(
        "--strict-validation",
        action="store_true",
        help="Fail processing if any invalid emails are found",
    )

    # Filtering options
    classify_parser.add_argument(
        "--max-body-length",
        type=int,
        default=None,
        metavar="CHARS",
        help="Skip emails with body length exceeding this limit (in characters). "
        "Skipped emails are logged to skipped_emails.csv.",
    )

    # =========================================================================
    # Parse arguments with backward compatibility
    # =========================================================================

    # Check if first arg looks like a file (backward compatibility)
    # If no subcommand is given but a .csv file is provided, treat as classify
    args = None
    if len(sys.argv) > 1:
        first_arg = sys.argv[1]
        # If first arg is not a known command and looks like a file path
        if first_arg not in (
            "info",
            "classify",
            "-h",
            "--help",
            "--version",
            "--list-domains",
        ):
            if first_arg.endswith(".csv") or (
                not first_arg.startswith("-") and "-o" in sys.argv
            ):
                # Insert 'classify' as the command for backward compatibility
                sys.argv.insert(1, "classify")

    args = parser.parse_args()

    # Route to appropriate command
    if args.command == "info":
        return cmd_info(args)
    elif args.command == "classify":
        return cmd_classify(args)
    else:
        # No command specified, show help
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
