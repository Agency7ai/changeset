"""
Changeset Agent - WordPress site optimization with human-in-the-loop approval.

This module implements a Strands agent that:
1. Scans WordPress sites (Woo products, SEO metadata, landing pages)
2. Drafts change sets based on findings
3. Requires human approval before publishing (via HumanInTheLoop)
"""

from strands import Agent, tool
from strands.vended_interventions.hitl import HumanInTheLoop


@tool
def scan_site(site_url: str) -> dict:
    """
    Scan a WordPress site for optimization opportunities.

    Analyzes WooCommerce products, SEO metadata, and landing pages to identify
    areas for improvement. This is a read-only operation that does not modify
    the site.

    Args:
        site_url (str): The URL of the WordPress site to scan

    Returns:
        dict: Scan results with identified issues and opportunities
    """
    return {
        'site_url': site_url,
        'scan_completed': True,
        'findings': {
            'products': {
                'total_scanned': 42,
                'issues': [
                    {
                        'product_id': 'prod_123',
                        'title': 'Wireless Mouse',
                        'issues': ['Missing alt text on image', 'Short description needed']
                    },
                    {
                        'product_id': 'prod_456',
                        'title': 'USB-C Cable',
                        'issues': ['Price formatting inconsistent', 'Category missing']
                    }
                ]
            },
            'seo': {
                'pages_scanned': 15,
                'issues': [
                    {
                        'page': '/landing/summer-sale',
                        'issues': ['Meta description too short', 'H1 tag missing']
                    },
                    {
                        'page': '/product-category/electronics',
                        'issues': ['Duplicate title tags', 'Missing canonical URL']
                    }
                ]
            },
            'landing_pages': {
                'total': 8,
                'issues': [
                    {
                        'page': '/promo/new-arrivals',
                        'issues': ['CTA button text unclear', 'Load time > 3s']
                    }
                ]
            }
        },
        'summary': 'Found 9 optimization opportunities across products, SEO, and landing pages'
    }


@tool
def draft_changeset(scan_results: dict) -> dict:
    """
    Draft a change set based on scan results.

    Creates a structured set of proposed changes to address issues found during
    the site scan. This does not apply any changes to the live site.

    Args:
        scan_results (dict): Results from scan_site containing identified issues

    Returns:
        dict: Drafted change set with proposed modifications
    """
    site_url = scan_results.get('site_url', 'unknown')
    findings = scan_results.get('findings', {})

    changeset = {
        'site_url': site_url,
        'created': True,
        'changes': []
    }

    if 'products' in findings:
        for issue in findings['products'].get('issues', []):
            changeset['changes'].append({
                'type': 'product_update',
                'product_id': issue['product_id'],
                'product_title': issue['title'],
                'proposed_changes': issue['issues']
            })

    if 'seo' in findings:
        for issue in findings['seo'].get('issues', []):
            changeset['changes'].append({
                'type': 'seo_update',
                'page': issue['page'],
                'proposed_changes': issue['issues']
            })

    if 'landing_pages' in findings:
        for issue in findings['landing_pages'].get('issues', []):
            changeset['changes'].append({
                'type': 'landing_page_update',
                'page': issue['page'],
                'proposed_changes': issue['issues']
            })

    changeset['summary'] = f"Drafted {len(changeset['changes'])} changes for {site_url}"

    return changeset


@tool
def publish_changeset(changeset: dict) -> dict:
    """
    Publish the approved change set to the live WordPress site.

    REQUIRES HUMAN APPROVAL via HumanInTheLoop. This is a write operation that
    will modify the live site with the proposed changes.

    Args:
        changeset (dict): The change set to publish (from draft_changeset)

    Returns:
        dict: Publication results with success status
    """
    site_url = changeset.get('site_url', 'unknown')
    changes = changeset.get('changes', [])

    return {
        'site_url': site_url,
        'published': True,
        'changes_applied': len(changes),
        'status': 'success',
        'message': f'Successfully published {len(changes)} changes to {site_url}',
        'note': 'This is a placeholder. In production, this would apply changes via WordPress API.'
    }


def create_agent() -> Agent:
    """
    Create and configure the Changeset agent with human-in-the-loop approval.

    The agent is configured so that:
    - scan_site: Runs without approval (read-only)
    - draft_changeset: Runs without approval (no writes)
    - publish_changeset: REQUIRES human approval (writes to live site)

    Returns:
        Agent: Configured Strands agent ready to use
    """
    agent = Agent(
        tools=[scan_site, draft_changeset, publish_changeset],
        interventions=[
            HumanInTheLoop(
                ask='stdio',
                allowed_tools=['scan_site', 'draft_changeset']
            )
        ],
        system_prompt=(
            'You are Changeset, a background WordPress optimization agent. '
            'Your role is to scan WordPress sites for optimization opportunities, '
            'draft change sets, and help humans approve changes before publishing. '
            'Always scan first, draft changes second, and only publish after '
            'explicit human approval.'
        )
    )
    return agent


if __name__ == '__main__':
    print('=== Changeset Agent Demo ===')
    print('Demonstrating a local workflow with a fake site scan.\n')

    agent = create_agent()

    demo_prompt = (
        'Scan the site at https://demo-shop.example.com, '
        'draft a change set based on the findings, '
        'and then publish the changes.'
    )

    print(f'Agent prompt: {demo_prompt}\n')
    print('Note: The publish step will require your approval (y/n) in the terminal.\n')
    print('-' * 60)

    try:
        result = agent(demo_prompt)
        print('-' * 60)
        print('\n=== Demo Complete ===')
        print(f'Final response: {result.message}')
    except KeyboardInterrupt:
        print('\n\nDemo interrupted by user.')
    except Exception as e:
        print(f'\n\nError during demo: {e}')
        print('This is expected if AWS/Bedrock credentials are not configured.')
        print('See README.md for setup instructions.')
