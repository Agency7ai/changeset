"""
Changeset - A background WordPress agent with human-in-the-loop approval.

This package provides an agent that scans WooCommerce products, SEO metadata,
and landing pages on a schedule, drafts change sets, and requires human
approval before publishing any changes.
"""

from . import agent

__version__ = '0.1.0'
__all__ = ['agent']
