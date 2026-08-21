# Changeset

A background WordPress agent for the [AWS Agents for Humans Hackathon](https://agents-for-humans.devpost.com/) (Professional track). Changeset scans WooCommerce products, SEO metadata, and landing pages on a schedule, drafts change sets, and uses Strands HumanInTheLoop intervention to ensure nothing publishes until a human approves.

**Status:** Early hackathon work - working Strands agent skeleton ready for further development.

## What is Changeset?

Changeset is an AI agent built with the [Strands Agents SDK](https://strandsagents.com/) that helps optimize WordPress sites with human oversight:

1. **Scan**: Analyzes WooCommerce products, SEO metadata, and landing pages for optimization opportunities (read-only, no approval required)
2. **Draft**: Creates a structured change set with proposed fixes (no approval required)
3. **Publish**: Applies changes to the live site **only after human approval** via HumanInTheLoop

This ensures automated discovery and planning while maintaining human control over what actually gets published.

## Architecture

- **Agent Framework**: Strands Agents SDK (Python)
- **Model Provider**: Amazon Bedrock with Claude Sonnet 4 (default)
- **Human-in-the-Loop**: Strands `HumanInTheLoop` intervention handler
- **Future Enhancements**:
  - Scheduler integration for automated scans (cron, AWS EventBridge, etc.)
  - Optional AgentCore deployment for stateful workflows
  - WordPress API integration (currently stubbed)
  - WooCommerce API integration (currently stubbed)

## Project Structure

```
changeset/
├── changeset/           # Python package
│   ├── __init__.py     # Package initialization
│   └── agent.py        # Agent definition with tools and HITL config
├── .env.example        # Template for AWS/Bedrock credentials
├── .gitignore          # Python/venv exclusions
├── LICENSE             # MIT License
├── README.md           # This file
├── requirements.txt    # Python dependencies
└── pyproject.toml      # Project metadata
```

## Prerequisites

- **Python 3.10 or higher**
- **AWS Credentials** with access to Amazon Bedrock
- **Model Access** enabled for Claude Sonnet 4 in Bedrock

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/changeset.git
cd changeset
```

### 2. Create and activate a virtual environment

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate

# On Windows (CMD):
.venv\Scripts\activate.bat

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### AWS / Amazon Bedrock Credentials

Changeset uses Amazon Bedrock with Claude Sonnet 4 by default. You need AWS credentials with Bedrock access.

#### Option 1: Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```bash
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-west-2
```

Then load them before running:

```bash
# On macOS/Linux:
export $(cat .env | xargs)

# Or use a tool like python-dotenv
```

#### Option 2: AWS CLI

Configure credentials using the AWS CLI:

```bash
aws configure
```

This stores credentials in `~/.aws/credentials`.

#### Option 3: IAM Roles

If running on AWS (EC2, ECS, Lambda), use IAM roles attached to the instance/service.

### Enable Bedrock Model Access

Make sure you have enabled model access for Claude Sonnet 4 in the Amazon Bedrock console:

1. Go to [Amazon Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Navigate to **Model access**
3. Request access to **Anthropic Claude Sonnet 4**

See the [AWS documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html) for details.

## Running Locally

### Quick Test

Run the agent demo with a fake site scan:

```bash
python -m changeset.agent
```

This will:
1. Scan a demo site (returns structured placeholder data)
2. Draft a change set based on findings
3. Prompt you in the terminal to approve publishing (y/n)

**Note**: The scan and draft steps run without approval. Only the publish step requires human confirmation.

### Interactive Agent

You can also import and use the agent in your own Python code:

```python
from changeset.agent import create_agent

agent = create_agent()
result = agent('Scan https://mysite.com and draft changes')
print(result.message)
```

## Development

### Testing Without AWS Credentials

If you want to test the code structure without AWS credentials, you can verify imports:

```bash
python -c "from changeset import agent; print('Imports successful!')"
```

The actual agent invocation requires valid Bedrock credentials. During development, you can:
- Use placeholder credentials to test import paths
- Configure a different model provider (see Strands docs for OpenAI, Anthropic, Ollama, etc.)

### Adding Real WordPress Integration

The current `scan_site` and `publish_changeset` tools return placeholder data. To integrate with real WordPress sites:

1. Install WordPress API client (e.g., `python-wordpress-xmlrpc` or `requests` with WP REST API)
2. Update tool functions to make live API calls
3. Add authentication handling (API keys, OAuth, etc.)
4. Implement error handling and rate limiting

### Future Scheduler Integration

To run Changeset on a schedule:
- **Cron**: Simple cron job calling the agent script
- **AWS EventBridge**: Trigger Lambda function with the agent
- **AgentCore**: Use AWS Bedrock AgentCore for stateful scheduling

## Hackathon Context

This project is part of the [AWS Agents for Humans Hackathon](https://agents-for-humans.devpost.com/) (Professional track). It demonstrates:

- **Human-in-the-Loop**: Using Strands `HumanInTheLoop` intervention to gate destructive operations
- **Autonomous Scanning**: Safe read-only operations run without approval
- **Structured Workflow**: Scan → Draft → Approve → Publish pattern

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Resources

- [Strands Agents Documentation](https://strandsagents.com/)
- [Strands Python Quickstart](https://strandsagents.com/docs/user-guide/quickstart/python/)
- [HumanInTheLoop Guide](https://strandsagents.com/docs/user-guide/concepts/agents/interventions/human-in-the-loop/)
- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [AWS Agents for Humans Hackathon](https://agents-for-humans.devpost.com/)

## Contributing

This is early hackathon work. Contributions, issues, and feedback are welcome!

## Acknowledgments

Built with the [Strands Agents SDK](https://strandsagents.com/) and inspired by the need for safe, human-supervised automation of WordPress site optimization tasks.
