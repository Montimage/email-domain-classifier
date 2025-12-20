"""
Streaming processor for large CSV email datasets.

Processes emails in chunks to minimize memory usage while
maintaining progress tracking and logging.
"""

import csv
import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Generator, Optional, Callable, List
from dataclasses import dataclass, field
from collections import defaultdict

from .classifier import EmailClassifier, EmailData
from .domains import get_domain_names


@dataclass
class ProcessingStats:
    """Statistics collected during processing."""
    total_processed: int = 0
    total_classified: int = 0
    total_unsure: int = 0
    domain_counts: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    errors: int = 0
    start_time: datetime = None
    end_time: datetime = None
    
    def to_dict(self) -> Dict:
        """Convert stats to dictionary."""
        return {
            'total_processed': self.total_processed,
            'total_classified': self.total_classified,
            'total_unsure': self.total_unsure,
            'domain_counts': dict(self.domain_counts),
            'errors': self.errors,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': (self.end_time - self.start_time).total_seconds() 
                if self.start_time and self.end_time else None,
        }


class OutputManager:
    """Manages output CSV files for each domain."""
    
    def __init__(self, output_dir: Path, fieldnames: List[str]):
        self.output_dir = output_dir
        self.fieldnames = fieldnames
        self.files = {}
        self.writers = {}
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_writer(self, domain: str):
        """Get or create CSV writer for domain."""
        if domain not in self.writers:
            filename = f"email_{domain}.csv"
            filepath = self.output_dir / filename
            
            # Open file in append mode with newline handling
            file = open(filepath, 'w', newline='', encoding='utf-8')
            self.files[domain] = file
            
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            self.writers[domain] = writer
        
        return self.writers[domain]
    
    def write_email(self, domain: str, email_data: Dict):
        """Write email to appropriate domain file."""
        writer = self._get_writer(domain)
        writer.writerow(email_data)
        self.files[domain].flush()
    
    def close_all(self):
        """Close all open files."""
        for file in self.files.values():
            file.close()
        self.files.clear()
        self.writers.clear()
    
    def get_output_files(self) -> Dict[str, Path]:
        """Return mapping of domains to their output file paths."""
        return {
            domain: self.output_dir / f"email_{domain}.csv"
            for domain in self.writers.keys()
        }


class StreamingProcessor:
    """
    Stream processes large CSV files for email classification.
    
    Features:
    - Memory-efficient chunk-based processing
    - Real-time progress tracking
    - Comprehensive logging
    - Statistics collection
    """
    
    # Default expected CSV columns
    EXPECTED_COLUMNS = ['sender', 'receiver', 'timestamp', 'subject', 'body', 'has_url']
    
    def __init__(
        self,
        classifier: EmailClassifier = None,
        chunk_size: int = 1000,
        logger: logging.Logger = None
    ):
        self.classifier = classifier or EmailClassifier()
        self.chunk_size = chunk_size
        self.logger = logger or logging.getLogger(__name__)
        self.stats = ProcessingStats()
    
    def count_rows(self, input_path: Path) -> int:
        """Count total rows in CSV file for progress tracking."""
        count = 0
        with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
            # Skip header
            next(f, None)
            for _ in f:
                count += 1
        return count
    
    def _stream_emails(self, input_path: Path) -> Generator[Dict, None, None]:
        """Stream emails from CSV file one at a time."""
        with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)
            
            # Validate columns
            if reader.fieldnames:
                missing = set(self.EXPECTED_COLUMNS) - set(reader.fieldnames)
                if missing:
                    self.logger.warning(f"Missing expected columns: {missing}")
            
            for row in reader:
                yield row
    
    def process(
        self,
        input_path: Path,
        output_dir: Path,
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
        include_details: bool = False
    ) -> ProcessingStats:
        """
        Process input CSV and write classified emails to domain-specific files.
        
        Args:
            input_path: Path to input CSV file
            output_dir: Directory for output files
            progress_callback: Optional callback(current, total, status) for progress updates
            include_details: Include classification details in output
        
        Returns:
            ProcessingStats with classification results
        """
        self.stats = ProcessingStats()
        self.stats.start_time = datetime.now()
        
        input_path = Path(input_path)
        output_dir = Path(output_dir)
        
        self.logger.info(f"Starting processing of {input_path}")
        
        # Count total rows for progress
        if progress_callback:
            progress_callback(0, 0, "Counting rows...")
        
        total_rows = self.count_rows(input_path)
        self.logger.info(f"Total emails to process: {total_rows}")
        
        # Determine output fieldnames
        with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames) if reader.fieldnames else self.EXPECTED_COLUMNS.copy()
        
        # Add classification columns
        fieldnames.extend(['classified_domain', 'method1_domain', 'method2_domain'])
        if include_details:
            fieldnames.extend(['method1_confidence', 'method2_confidence', 'agreement'])
        
        # Initialize output manager
        output_manager = OutputManager(output_dir, fieldnames)
        
        try:
            for idx, email_dict in enumerate(self._stream_emails(input_path)):
                try:
                    # Classify email
                    domain, details = self.classifier.classify_dict(email_dict)
                    
                    # Prepare output row
                    output_row = email_dict.copy()
                    output_row['classified_domain'] = domain
                    output_row['method1_domain'] = details['method1']['domain'] or 'none'
                    output_row['method2_domain'] = details['method2']['domain'] or 'none'
                    
                    if include_details:
                        output_row['method1_confidence'] = f"{details['method1']['confidence']:.4f}"
                        output_row['method2_confidence'] = f"{details['method2']['confidence']:.4f}"
                        output_row['agreement'] = details.get('agreement', False)
                    
                    # Write to appropriate file
                    output_manager.write_email(domain, output_row)
                    
                    # Update stats
                    self.stats.total_processed += 1
                    self.stats.domain_counts[domain] += 1
                    
                    if domain != 'unsure':
                        self.stats.total_classified += 1
                    else:
                        self.stats.total_unsure += 1
                    
                    # Log periodically
                    if (idx + 1) % self.chunk_size == 0:
                        self.logger.info(
                            f"Processed {idx + 1}/{total_rows} emails "
                            f"({(idx + 1) / total_rows * 100:.1f}%)"
                        )
                    
                    # Progress callback
                    if progress_callback and idx % 100 == 0:
                        progress_callback(idx + 1, total_rows, f"Processing email {idx + 1}")
                
                except Exception as e:
                    self.stats.errors += 1
                    self.logger.error(f"Error processing email {idx + 1}: {e}")
                    
                    # Still write to unsure if there's an error
                    try:
                        output_row = email_dict.copy()
                        output_row['classified_domain'] = 'unsure'
                        output_row['method1_domain'] = 'error'
                        output_row['method2_domain'] = 'error'
                        if include_details:
                            output_row['method1_confidence'] = '0'
                            output_row['method2_confidence'] = '0'
                            output_row['agreement'] = False
                        output_manager.write_email('unsure', output_row)
                        self.stats.total_unsure += 1
                    except:
                        pass
            
            # Final progress update
            if progress_callback:
                progress_callback(total_rows, total_rows, "Processing complete")
        
        finally:
            output_manager.close_all()
        
        self.stats.end_time = datetime.now()
        
        # Log summary
        duration = (self.stats.end_time - self.stats.start_time).total_seconds()
        self.logger.info(f"Processing complete in {duration:.2f} seconds")
        self.logger.info(f"Total processed: {self.stats.total_processed}")
        self.logger.info(f"Total classified: {self.stats.total_classified}")
        self.logger.info(f"Total unsure: {self.stats.total_unsure}")
        self.logger.info(f"Errors: {self.stats.errors}")
        
        return self.stats
    
    def get_output_summary(self, output_dir: Path) -> Dict[str, int]:
        """Get summary of output files and their row counts."""
        output_dir = Path(output_dir)
        summary = {}
        
        for csv_file in output_dir.glob("email_*.csv"):
            domain = csv_file.stem.replace("email_", "")
            
            # Count rows (excluding header)
            with open(csv_file, 'r', encoding='utf-8') as f:
                count = sum(1 for _ in f) - 1
            
            if count > 0:
                summary[domain] = count
        
        return summary
