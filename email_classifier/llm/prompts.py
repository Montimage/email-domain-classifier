"""System prompts and domain definitions for LLM classification."""

from ..domains import DOMAINS, DomainProfile

# Domain descriptions for the LLM agent
DOMAIN_DESCRIPTIONS: dict[str, str] = {
    "finance": (
        "Banking, financial transactions, account management, payments, investments, "
        "loans, credit cards, wire transfers, and financial alerts or notifications."
    ),
    "technology": (
        "Software services, cloud platforms, account security, password resets, "
        "subscription management, API access, and technical notifications."
    ),
    "retail": (
        "E-commerce, online shopping, order confirmations, purchase receipts, "
        "product shipments, returns, refunds, and promotional offers."
    ),
    "logistics": (
        "Shipping carriers, package tracking, delivery notifications, freight, "
        "courier services, customs, and shipment status updates."
    ),
    "healthcare": (
        "Medical appointments, prescriptions, lab results, health insurance, "
        "patient communications, pharmacy notifications, and HIPAA-related messages."
    ),
    "government": (
        "Tax notices, regulatory compliance, government agencies, official forms, "
        "licenses, permits, and federal/state/municipal communications."
    ),
    "hr": (
        "Human resources, employee benefits, payroll, PTO requests, performance reviews, "
        "onboarding, company policies, and internal personnel matters."
    ),
    "telecommunications": (
        "Mobile carriers, phone bills, data plans, wireless services, device upgrades, "
        "account management, and telecom provider notifications."
    ),
    "social_media": (
        "Social networking platforms, profile updates, friend/follow notifications, "
        "direct messages, security alerts, and community guidelines."
    ),
    "education": (
        "Universities, colleges, schools, course enrollment, tuition, financial aid, "
        "grades, transcripts, and academic communications."
    ),
}


def get_domain_list_for_prompt() -> str:
    """Generate a formatted list of domains with descriptions for the prompt.

    Returns:
        A formatted string listing all domains and their descriptions.
    """
    lines = []
    for domain_name, profile in DOMAINS.items():
        description = DOMAIN_DESCRIPTIONS.get(domain_name, profile.display_name)
        lines.append(f"- **{domain_name}**: {description}")
    lines.append("- **unsure**: Use when the email does not clearly match any domain")
    return "\n".join(lines)


SYSTEM_PROMPT = """You are an expert email classification agent. Your task is to analyze emails and classify them into business domain categories.

## Available Domains

{domain_list}

## Classification Guidelines

1. **Analyze the email content** including:
   - Sender address patterns (e.g., noreply@bank.com suggests finance)
   - Subject line keywords and patterns
   - Body content, terminology, and context
   - URLs and links if mentioned

2. **Assign confidence scores** between 0.0 and 1.0:
   - 0.7-1.0: High confidence - clear domain match with strong indicators
   - 0.5-0.7: Medium confidence - likely match but some ambiguity
   - 0.3-0.5: Low confidence - possible match but uncertain
   - Below 0.3: Very low confidence - weak or no match

3. **Handle ambiguous cases**:
   - If an email could belong to multiple domains, include all relevant domains with their confidence scores
   - Order classifications by confidence (highest first)
   - Use "unsure" only when no domain clearly matches

4. **Provide reasoning**:
   - Explain what indicators led to each classification
   - Be specific about keywords, patterns, or structural elements

## Output Format

Return a structured classification with:
- A list of domain classifications with confidence scores
- The primary (most confident) domain
- A brief analysis explaining your reasoning"""


def get_classification_prompt(
    sender: str, subject: str, body: str, max_body_chars: int = 2000
) -> str:
    """Generate the user prompt for classifying an email.

    Args:
        sender: Email sender address.
        subject: Email subject line.
        body: Email body content.
        max_body_chars: Maximum characters to include from body.

    Returns:
        Formatted prompt for the LLM.
    """
    # Truncate body if needed
    if len(body) > max_body_chars:
        body = body[:max_body_chars] + "... [truncated]"

    return f"""Classify the following email into the appropriate domain category.

## Email Details

**From:** {sender}

**Subject:** {subject}

**Body:**
{body}

## Instructions

1. Analyze the email content carefully
2. Identify the most appropriate domain category
3. Provide confidence scores for all relevant domains
4. Explain your reasoning

Classify this email now."""


def get_system_prompt() -> str:
    """Get the complete system prompt with domain list.

    Returns:
        The full system prompt for the classification agent.
    """
    domain_list = get_domain_list_for_prompt()
    return SYSTEM_PROMPT.format(domain_list=domain_list)
