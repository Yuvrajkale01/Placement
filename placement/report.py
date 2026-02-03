"""Report generation utilities."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from jinja2 import Template

from placement.fraud import SuspiciousOffer


REPORT_TEMPLATE = """
# Placement Cell Report

## Overview
- Total students placed: {{ metrics.total_students }}
- Total offers recorded: {{ metrics.total_offers }}
- Average salary package: {{ metrics.average_salary | round(2) }}
- Median salary package: {{ metrics.median_salary | round(2) }}

## Department Highlights
{% for department, salary in metrics.top_departments.items() %}
- {{ department }}: median salary {{ salary | round(2) }}
{% endfor %}

## Company Engagement
{% for company, count in metrics.offers_by_company.items() %}
- {{ company }}: {{ count }} offers
{% endfor %}

## Suspicious Offers
{% if suspicious_offers %}
The following offers were flagged for review:
{% for offer in suspicious_offers %}
- Student {{ offer.student_id }} at {{ offer.company }} ({{ offer.role }})
  salary {{ offer.salary_package }} with z-score {{ offer.z_score | round(2) }}
{% endfor %}
{% else %}
No suspicious offers were flagged in this dataset.
{% endif %}

## Notes
{{ notes }}
""".strip()


@dataclass
class ReportPayload:
    metrics: dict[str, object]
    suspicious_offers: list[SuspiciousOffer]
    notes: str



def render_report(payload: ReportPayload) -> str:
    """Render a markdown report from placement analytics."""
    template = Template(REPORT_TEMPLATE)
    return template.render(
        metrics=payload.metrics,
        suspicious_offers=payload.suspicious_offers,
        notes=payload.notes,
    )



def write_report(content: str, path: str | Path) -> None:
    """Write the report to disk."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
