"""
Terminal UI components for email classifier.

Provides a polished, visually distinctive CLI experience using
the Rich library for beautiful terminal output.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    from rich import box
    from rich.console import Console
    from rich.layout import Layout
    from rich.live import Live
    from rich.panel import Panel
    from rich.progress import (
        BarColumn,
        Progress,
        SpinnerColumn,
        TaskProgressColumn,
        TextColumn,
        TimeElapsedColumn,
        TimeRemainingColumn,
    )
    from rich.style import Style
    from rich.table import Table
    from rich.text import Text
    from rich.theme import Theme

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


# Custom theme for distinctive look
CLASSIFIER_THEME = Theme(
    {
        "info": "cyan",
        "warning": "yellow",
        "error": "bold red",
        "success": "bold green",
        "domain.finance": "green",
        "domain.technology": "blue",
        "domain.retail": "magenta",
        "domain.logistics": "yellow",
        "domain.healthcare": "cyan",
        "domain.government": "red",
        "domain.hr": "white",
        "domain.telecommunications": "bright_blue",
        "domain.social_media": "bright_magenta",
        "domain.education": "bright_cyan",
        "domain.unsure": "dim white",
        "header": "bold bright_white on dark_blue",
        "accent": "bold cyan",
    }
)


class TerminalUI:
    """
    Rich terminal UI for email classification.

    Features:
    - Animated progress bars
    - Real-time statistics
    - Color-coded domain display
    - Formatted tables and panels
    """

    def __init__(self, quiet: bool = False):
        self.quiet = quiet

        if RICH_AVAILABLE and not quiet:
            self.console = Console(theme=CLASSIFIER_THEME)
        else:
            self.console = None

    def print_banner(self):
        """Display application banner."""
        if self.quiet or not self.console:
            return

        banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ███████╗███╗   ███╗ █████╗ ██╗██╗         ██████╗██╗      █████╗ ███████╗   ║
║   ██╔════╝████╗ ████║██╔══██╗██║██║        ██╔════╝██║     ██╔══██╗██╔════╝   ║
║   █████╗  ██╔████╔██║███████║██║██║        ██║     ██║     ███████║███████╗   ║
║   ██╔══╝  ██║╚██╔╝██║██╔══██║██║██║        ██║     ██║     ██╔══██║╚════██║   ║
║   ███████╗██║ ╚═╝ ██║██║  ██║██║███████╗   ╚██████╗███████╗██║  ██║███████║   ║
║   ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝    ╚═════╝╚══════╝╚═╝  ╚═╝╚══════╝   ║
║                                                                               ║
║                    Domain Classification System v1.0                          ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
        self.console.print(banner, style="bold cyan")

    def print_config(self, input_file: str, output_dir: str, options: Dict = None):
        """Display configuration panel."""
        if self.quiet or not self.console:
            return

        table = Table(show_header=False, box=box.ROUNDED, border_style="cyan")
        table.add_column("Setting", style="bold")
        table.add_column("Value", style="white")

        table.add_row("📁 Input File", input_file)
        table.add_row("📂 Output Directory", output_dir)

        if options:
            for key, value in options.items():
                icon = "⚙️ " if not key.startswith("�") else ""
                table.add_row(f"{icon}{key}", str(value))

        panel = Panel(
            table,
            title="[bold]Configuration[/bold]",
            border_style="cyan",
            padding=(1, 2),
        )

        self.console.print(panel)
        self.console.print()

    def create_progress(self) -> Optional[Progress]:
        """Create progress bar context manager."""
        if self.quiet or not self.console:
            return None

        return Progress(
            SpinnerColumn(spinner_name="dots12", style="cyan"),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40, style="cyan", complete_style="green"),
            TaskProgressColumn(),
            TextColumn("•"),
            TimeElapsedColumn(),
            TextColumn("•"),
            TimeRemainingColumn(),
            console=self.console,
            expand=True,
        )

    def print_domain_stats(
        self,
        domain_counts: Dict[str, int],
        total: int,
        enhanced_stats: Optional[Dict] = None,
    ):
        """Display domain statistics table."""
        if self.quiet or not self.console:
            return

        table = Table(
            title="Classification Results by Domain",
            box=box.DOUBLE_EDGE,
            border_style="cyan",
            header_style="bold white on dark_blue",
            show_lines=True,
        )

        table.add_column("Domain", style="bold", width=25)
        table.add_column("Count", justify="right", width=12)
        table.add_column("Percentage", justify="right", width=12)
        table.add_column("Distribution", width=30)

        # Sort by count descending
        sorted_domains = sorted(domain_counts.items(), key=lambda x: -x[1])
        max_count = max(domain_counts.values()) if domain_counts else 1

        for domain, count in sorted_domains:
            percentage = count / total * 100 if total > 0 else 0
            bar_width = int(count / max_count * 25) if max_count > 0 else 0
            bar = "█" * bar_width

            # Get domain style
            style = (
                f"domain.{domain}"
                if domain
                in [
                    "finance",
                    "technology",
                    "retail",
                    "logistics",
                    "healthcare",
                    "government",
                    "hr",
                    "telecommunications",
                    "social_media",
                    "education",
                    "unsure",
                ]
                else "white"
            )

            # Format domain name
            domain_display = domain.replace("_", " ").title()
            if domain == "unsure":
                domain_display = "⚠️  Unsure"

            table.add_row(
                Text(domain_display, style=style),
                f"{count:,}",
                f"{percentage:.1f}%",
                Text(bar, style=style),
            )

        self.console.print()
        self.console.print()

        # Enhanced statistics if available
        if enhanced_stats:
            # Combined Enhanced Statistics Table
            enhanced_table = Table(
                title="Enhanced Classification Statistics",
                box=box.ROUNDED,
                border_style="cyan",
                header_style="bold white on dark_blue",
                show_lines=True,
            )

            enhanced_table.add_column("Domain", style="bold", width=18)
            enhanced_table.add_column("Count", justify="right", width=8)
            enhanced_table.add_column("Percentage", justify="right", width=10)
            enhanced_table.add_column("Distribution", width=15)
            enhanced_table.add_column("Top Labels", width=25)
            enhanced_table.add_column("URL Rate", justify="right", width=10)

            # Sort by count descending
            sorted_domains = sorted(domain_counts.items(), key=lambda x: -x[1])
            max_count = max(domain_counts.values()) if domain_counts else 1

            # Get enhanced analysis data
            label_analysis = enhanced_stats.get("label_distribution_analysis", {})
            url_analysis = enhanced_stats.get("url_distribution_analysis", {})

            for domain, count in sorted_domains:
                percentage = count / total * 100 if total > 0 else 0
                bar_width = (
                    int(count / max_count * 15) if max_count > 0 else 0
                )  # Reduced width for other columns
                bar = "█" * bar_width + "░" * (15 - bar_width)

                # Get domain style
                style = (
                    f"domain.{domain}"
                    if domain
                    in [
                        "finance",
                        "technology",
                        "retail",
                        "logistics",
                        "healthcare",
                        "government",
                        "hr",
                        "telecommunications",
                        "social_media",
                        "education",
                        "unsure",
                    ]
                    else "white"
                )

                # Format domain name
                domain_display = domain.replace("_", " ").title()
                if domain == "unsure":
                    domain_display = "⚠️  Unsure"

                # Get label information
                label_info = ""
                if domain in label_analysis:
                    data = label_analysis[domain]
                    # Get top 2 labels for this domain (to fit in table)
                    top_labels = sorted(
                        data["distribution"].items(), key=lambda x: -x[1]["percentage"]
                    )[:2]
                    label_parts = [
                        f"{label} ({info['percentage']:.0f}%)"
                        for label, info in top_labels
                    ]
                    label_info = ", ".join(label_parts)

                # Get URL information
                url_info = ""
                if domain in url_analysis:
                    url_data = url_analysis[domain]
                    url_info = f"{url_data['with_urls']['percentage']:.0f}%"

                enhanced_table.add_row(
                    Text(domain_display, style=style),
                    f"{count:,}",
                    f"{percentage:.1f}%",
                    Text(bar, style=style),
                    label_info if label_info else "No data",
                    url_info if url_info else "N/A",
                )

            self.console.print(enhanced_table)
            self.console.print()

    def print_summary_panel(self, stats: Dict):
        """Display final summary panel."""
        if self.quiet or not self.console:
            return

        summary = stats.get("summary", {})
        timing = stats.get("timing", {})
        quality = stats.get("quality_metrics", {})

        # Create summary text
        content = Text()
        content.append("📊 Processing Summary\n\n", style="bold cyan")

        content.append("  Total Emails:      ", style="dim")
        content.append(f"{summary.get('total_emails', 0):,}\n", style="bold white")

        content.append("  Classified:        ", style="dim")
        content.append(f"{summary.get('classified', 0):,}", style="bold green")
        content.append(
            f" ({summary.get('classification_rate_percent', 0)}%)\n", style="green"
        )

        content.append("  Unsure:            ", style="dim")
        content.append(f"{summary.get('unsure', 0):,}\n", style="yellow")

        content.append("  Errors:            ", style="dim")
        error_style = "red" if summary.get("errors", 0) > 0 else "green"
        content.append(f"{summary.get('errors', 0):,}\n", style=error_style)

        content.append("\n⏱️  Performance\n\n", style="bold cyan")

        content.append("  Duration:          ", style="dim")
        content.append(f"{timing.get('duration_seconds', 0):.2f}s\n", style="white")

        content.append("  Speed:             ", style="dim")
        content.append(
            f"{timing.get('emails_per_second', 0):.0f} emails/sec\n", style="white"
        )

        content.append("\n📈 Quality Metrics\n\n", style="bold cyan")

        content.append("  Agreement Rate:    ", style="dim")
        agreement = quality.get("method_agreement_rate", 0)
        agreement_style = (
            "green" if agreement > 70 else "yellow" if agreement > 50 else "red"
        )
        content.append(f"{agreement}%\n", style=agreement_style)

        panel = Panel(
            content,
            title="[bold white]Results[/bold white]",
            border_style="green",
            padding=(1, 3),
        )

        self.console.print(panel)

    def print_output_files(self, output_dir: Path, file_counts: Dict[str, int]):
        """Display list of output files created."""
        if self.quiet or not self.console:
            return

        table = Table(
            title="Output Files Generated",
            box=box.ROUNDED,
            border_style="green",
            show_lines=False,
        )

        table.add_column("📄 File", style="cyan")
        table.add_column("Emails", justify="right", style="white")
        table.add_column("Status", justify="center")

        for domain, count in sorted(file_counts.items()):
            filename = f"email_{domain}.csv"
            status = "✅" if count > 0 else "⚪"
            table.add_row(filename, f"{count:,}", status)

        self.console.print()
        self.console.print(table)
        self.console.print()

        # Print output directory
        self.console.print(
            f"  📂 All files saved to: [bold cyan]{output_dir}[/bold cyan]\n"
        )

    def print_recommendations(self, recommendations: List[str]):
        """Display recommendations panel."""
        if self.quiet or not self.console or not recommendations:
            return

        content = Text()
        for i, rec in enumerate(recommendations, 1):
            icon = "💡" if "success" in rec.lower() else "⚠️"
            content.append(f"  {icon} ", style="yellow")
            content.append(f"{rec}\n\n", style="white")

        panel = Panel(
            content,
            title="[bold]Recommendations[/bold]",
            border_style="yellow",
            padding=(1, 2),
        )

        self.console.print(panel)

    def print_error(self, message: str):
        """Display error message."""
        if self.console:
            self.console.print(f"\n[bold red]✖ Error:[/bold red] {message}\n")
        else:
            print(f"\nError: {message}\n", file=sys.stderr)

    def print_warning(self, message: str):
        """Display warning message."""
        if self.console:
            self.console.print(f"[yellow]⚠ Warning:[/yellow] {message}")
        else:
            print(f"Warning: {message}", file=sys.stderr)

    def print_success(self, message: str):
        """Display success message."""
        if self.console:
            self.console.print(f"[bold green]✔[/bold green] {message}")
        else:
            print(f"✓ {message}")

    def print_info(self, message: str):
        """Display info message."""
        if self.console:
            self.console.print(f"[cyan]ℹ[/cyan] {message}")
        else:
            print(f"ℹ {message}")

    def confirm(self, message: str) -> bool:
        """Ask for user confirmation."""
        if self.console:
            self.console.print(
                f"\n[yellow]?[/yellow] {message} [dim](y/n)[/dim] ", end=""
            )
        else:
            print(f"\n? {message} (y/n) ", end="")

        response = input().strip().lower()
        return response in ("y", "yes")


class SimpleUI:
    """Fallback simple UI when Rich is not available."""

    def __init__(self, quiet: bool = False):
        self.quiet = quiet

    def print_banner(self):
        if self.quiet:
            return
        print("\n" + "=" * 60)
        print("       EMAIL DOMAIN CLASSIFIER v1.0")
        print("=" * 60 + "\n")

    def print_config(self, input_file: str, output_dir: str, options: Dict = None):
        if self.quiet:
            return
        print(f"Input:  {input_file}")
        print(f"Output: {output_dir}")
        if options:
            for k, v in options.items():
                print(f"{k}: {v}")
        print()

    def print_progress(self, current: int, total: int, status: str = ""):
        if self.quiet:
            return
        pct = current / total * 100 if total > 0 else 0
        bar_len = 40
        filled = int(bar_len * current / total) if total > 0 else 0
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"\r[{bar}] {pct:5.1f}% - {status}", end="", flush=True)
        if current >= total:
            print()

    def print_domain_stats(self, domain_counts: Dict[str, int], total: int):
        if self.quiet:
            return
        print("\n" + "-" * 50)
        print("Domain Classification Results:")
        print("-" * 50)
        for domain, count in sorted(domain_counts.items(), key=lambda x: -x[1]):
            pct = count / total * 100 if total > 0 else 0
            print(f"  {domain:<20} {count:>8,} ({pct:>5.1f}%)")
        print("-" * 50 + "\n")

    def print_error(self, message: str):
        print(f"ERROR: {message}", file=sys.stderr)

    def print_warning(self, message: str):
        print(f"WARNING: {message}", file=sys.stderr)

    def print_success(self, message: str):
        print(f"✓ {message}")

    def print_info(self, message: str):
        if not self.quiet:
            print(f"ℹ {message}")


def get_ui(quiet: bool = False) -> TerminalUI:
    """Get appropriate UI based on available libraries."""
    if RICH_AVAILABLE:
        return TerminalUI(quiet=quiet)
    else:
        return SimpleUI(quiet=quiet)
