"""
Report generation for email classification results.

Generates comprehensive reports with statistics, metrics,
and visualizations (ASCII-based for terminal).
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

from .processor import ProcessingStats
from .domains import DOMAINS


@dataclass
class ReportConfig:
    """Configuration for report generation."""
    include_domain_breakdown: bool = True
    include_timing_metrics: bool = True
    include_confidence_analysis: bool = True
    include_recommendations: bool = True


class ClassificationReporter:
    """
    Generates comprehensive classification reports.
    
    Output formats:
    - JSON (machine-readable)
    - Text (human-readable with ASCII visualization)
    - Markdown (for documentation)
    """
    
    def __init__(self, config: ReportConfig = None):
        self.config = config or ReportConfig()
    
    def generate_report(
        self,
        stats: ProcessingStats,
        output_dir: Path,
        input_file: str = None
    ) -> Dict:
        """Generate full report from processing statistics."""
        report = {
            'meta': {
                'generated_at': datetime.now().isoformat(),
                'input_file': input_file,
                'output_directory': str(output_dir),
            },
            'summary': self._generate_summary(stats),
            'domain_breakdown': self._generate_domain_breakdown(stats),
            'timing': self._generate_timing_metrics(stats),
            'quality_metrics': self._generate_quality_metrics(stats),
        }
        
        if self.config.include_recommendations:
            report['recommendations'] = self._generate_recommendations(stats)
        
        return report
    
    def _generate_summary(self, stats: ProcessingStats) -> Dict:
        """Generate summary statistics."""
        classification_rate = (
            stats.total_classified / stats.total_processed * 100
            if stats.total_processed > 0 else 0
        )
        
        error_rate = (
            stats.errors / stats.total_processed * 100
            if stats.total_processed > 0 else 0
        )
        
        return {
            'total_emails': stats.total_processed,
            'classified': stats.total_classified,
            'unsure': stats.total_unsure,
            'errors': stats.errors,
            'classification_rate_percent': round(classification_rate, 2),
            'error_rate_percent': round(error_rate, 2),
            'unique_domains_found': len([k for k, v in stats.domain_counts.items() if k != 'unsure' and v > 0]),
        }
    
    def _generate_domain_breakdown(self, stats: ProcessingStats) -> Dict:
        """Generate per-domain statistics."""
        total = stats.total_processed
        breakdown = {}
        
        for domain, count in sorted(stats.domain_counts.items(), key=lambda x: -x[1]):
            percentage = count / total * 100 if total > 0 else 0
            
            domain_info = DOMAINS.get(domain)
            display_name = domain_info.display_name if domain_info else domain.title()
            
            breakdown[domain] = {
                'count': count,
                'percentage': round(percentage, 2),
                'display_name': display_name,
            }
        
        return breakdown
    
    def _generate_timing_metrics(self, stats: ProcessingStats) -> Dict:
        """Generate timing and performance metrics."""
        if stats.start_time and stats.end_time:
            duration = (stats.end_time - stats.start_time).total_seconds()
            emails_per_second = stats.total_processed / duration if duration > 0 else 0
        else:
            duration = 0
            emails_per_second = 0
        
        return {
            'start_time': stats.start_time.isoformat() if stats.start_time else None,
            'end_time': stats.end_time.isoformat() if stats.end_time else None,
            'duration_seconds': round(duration, 2),
            'emails_per_second': round(emails_per_second, 2),
        }
    
    def _generate_quality_metrics(self, stats: ProcessingStats) -> Dict:
        """Generate quality and confidence metrics."""
        # Calculate agreement rate (how often both methods agreed)
        agreed = stats.total_classified
        total_attempts = stats.total_processed - stats.errors
        agreement_rate = agreed / total_attempts * 100 if total_attempts > 0 else 0
        
        # Domain distribution evenness (entropy-based)
        domain_counts = [v for k, v in stats.domain_counts.items() if k != 'unsure']
        if domain_counts:
            total_classified = sum(domain_counts)
            if total_classified > 0:
                import math
                probabilities = [c / total_classified for c in domain_counts]
                entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
                max_entropy = math.log2(len(domain_counts)) if len(domain_counts) > 1 else 1
                evenness = entropy / max_entropy if max_entropy > 0 else 0
            else:
                evenness = 0
        else:
            evenness = 0
        
        return {
            'method_agreement_rate': round(agreement_rate, 2),
            'domain_distribution_evenness': round(evenness, 4),
            'unsure_rate': round(stats.total_unsure / stats.total_processed * 100, 2) if stats.total_processed > 0 else 0,
        }
    
    def _generate_recommendations(self, stats: ProcessingStats) -> List[str]:
        """Generate actionable recommendations based on results."""
        recommendations = []
        
        unsure_rate = stats.total_unsure / stats.total_processed * 100 if stats.total_processed > 0 else 0
        
        if unsure_rate > 30:
            recommendations.append(
                "High unsure rate detected (>30%). Consider expanding keyword taxonomies "
                "or adjusting classification thresholds."
            )
        
        if unsure_rate > 50:
            recommendations.append(
                "Very high unsure rate (>50%). The email dataset may contain domains "
                "not currently defined in the taxonomy. Review unsure emails for new domain patterns."
            )
        
        error_rate = stats.errors / stats.total_processed * 100 if stats.total_processed > 0 else 0
        if error_rate > 5:
            recommendations.append(
                f"Error rate of {error_rate:.1f}% detected. Check input data quality "
                "and encoding issues."
            )
        
        # Check for dominant domains
        if stats.domain_counts:
            max_domain = max(stats.domain_counts.items(), key=lambda x: x[1])
            max_percentage = max_domain[1] / stats.total_processed * 100 if stats.total_processed > 0 else 0
            
            if max_percentage > 70 and max_domain[0] != 'unsure':
                recommendations.append(
                    f"Domain '{max_domain[0]}' dominates with {max_percentage:.1f}% of emails. "
                    "Consider if the dataset is representative or if classification is over-fitting."
                )
        
        if not recommendations:
            recommendations.append("Classification completed successfully with balanced results.")
        
        return recommendations
    
    def save_json_report(self, report: Dict, output_path: Path):
        """Save report as JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
    
    def save_text_report(self, report: Dict, output_path: Path):
        """Save report as formatted text with ASCII visualization."""
        lines = []
        
        # Header
        lines.append("═" * 80)
        lines.append("                    EMAIL CLASSIFICATION REPORT")
        lines.append("═" * 80)
        lines.append("")
        
        # Meta info
        lines.append(f"Generated: {report['meta']['generated_at']}")
        if report['meta']['input_file']:
            lines.append(f"Input: {report['meta']['input_file']}")
        lines.append(f"Output: {report['meta']['output_directory']}")
        lines.append("")
        
        # Summary section
        lines.append("─" * 80)
        lines.append("  SUMMARY")
        lines.append("─" * 80)
        summary = report['summary']
        lines.append(f"  Total Emails Processed:  {summary['total_emails']:,}")
        lines.append(f"  Successfully Classified: {summary['classified']:,} ({summary['classification_rate_percent']}%)")
        lines.append(f"  Unsure/Unclassified:     {summary['unsure']:,}")
        lines.append(f"  Errors:                  {summary['errors']:,} ({summary['error_rate_percent']}%)")
        lines.append(f"  Unique Domains Found:    {summary['unique_domains_found']}")
        lines.append("")
        
        # Domain breakdown with bar chart
        lines.append("─" * 80)
        lines.append("  DOMAIN BREAKDOWN")
        lines.append("─" * 80)
        
        breakdown = report['domain_breakdown']
        max_count = max(d['count'] for d in breakdown.values()) if breakdown else 1
        
        for domain, data in breakdown.items():
            bar_length = int(data['count'] / max_count * 30) if max_count > 0 else 0
            bar = "█" * bar_length + "░" * (30 - bar_length)
            lines.append(
                f"  {data['display_name']:<20} {bar} {data['count']:>8,} ({data['percentage']:>5.1f}%)"
            )
        lines.append("")
        
        # Timing metrics
        lines.append("─" * 80)
        lines.append("  PERFORMANCE METRICS")
        lines.append("─" * 80)
        timing = report['timing']
        lines.append(f"  Duration:            {timing['duration_seconds']:.2f} seconds")
        lines.append(f"  Processing Speed:    {timing['emails_per_second']:.2f} emails/second")
        lines.append("")
        
        # Quality metrics
        lines.append("─" * 80)
        lines.append("  QUALITY METRICS")
        lines.append("─" * 80)
        quality = report['quality_metrics']
        lines.append(f"  Method Agreement Rate:      {quality['method_agreement_rate']}%")
        lines.append(f"  Unsure Rate:                {quality['unsure_rate']}%")
        lines.append(f"  Domain Distribution Score:  {quality['domain_distribution_evenness']:.4f}")
        lines.append("")
        
        # Recommendations
        if 'recommendations' in report:
            lines.append("─" * 80)
            lines.append("  RECOMMENDATIONS")
            lines.append("─" * 80)
            for i, rec in enumerate(report['recommendations'], 1):
                # Word wrap recommendations
                words = rec.split()
                current_line = f"  {i}. "
                for word in words:
                    if len(current_line) + len(word) > 76:
                        lines.append(current_line)
                        current_line = "     " + word + " "
                    else:
                        current_line += word + " "
                if current_line.strip():
                    lines.append(current_line)
            lines.append("")
        
        # Footer
        lines.append("═" * 80)
        lines.append("                         END OF REPORT")
        lines.append("═" * 80)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def format_terminal_summary(self, report: Dict) -> str:
        """Format a brief summary for terminal output."""
        summary = report['summary']
        timing = report['timing']
        
        lines = [
            "",
            "┌─────────────────────────────────────────────────────────┐",
            "│              CLASSIFICATION COMPLETE                    │",
            "├─────────────────────────────────────────────────────────┤",
            f"│  Processed: {summary['total_emails']:>10,} emails                       │",
            f"│  Classified: {summary['classified']:>9,} ({summary['classification_rate_percent']:>5.1f}%)                     │",
            f"│  Unsure: {summary['unsure']:>13,}                                │",
            f"│  Duration: {timing['duration_seconds']:>10.2f}s @ {timing['emails_per_second']:.0f} emails/sec       │",
            "└─────────────────────────────────────────────────────────┘",
            "",
        ]
        
        return '\n'.join(lines)
