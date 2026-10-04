# Stripe Billing Ops

Invoices from real work, failed-payment follow-ups, revenue sheets and dispute evidence.

An MCP server with **14 workflows** across Google Calendar, GitHub, Stripe, Gmail, Slack, Google Sheets, Shopify, Google Drive, Linear, Google Docs and Notion. Each workflow is a prompt your agent runs as a slash command, over the 37 tools it needs and no others.

```bash
uv tool install https://github.com/r28ai/stripe-billing-ops-mcp/releases/download/v0.1.0/stripe_billing_ops_mcp-0.1.0-py3-none-any.whl
claude mcp add billing -- stripe-billing-ops-mcp
```

It installs with [uv](https://docs.astral.sh/uv/) from this repository's release, with no git and nothing to build; nothing but Charter and the libraries it uses comes from PyPI. To update, run the install line from the [latest release](https://github.com/r28ai/stripe-billing-ops-mcp/releases/latest). If a desktop app cannot find `stripe-billing-ops-mcp`, give it the full path from `which stripe-billing-ops-mcp` (`where stripe-billing-ops-mcp` on Windows).

Then ask your agent to **connect your apps**, or run `/mcp__billing__setup`.

## Connect your apps

Ask the agent to connect one ("connect Linear"). It tells you where to get that app's key and the command that stores it, and the next call works, with no restart. The agent never asks for a key in the chat.

Or connect everything this server uses from a terminal:

```bash
stripe-billing-ops-mcp login            # each app in turn
stripe-billing-ops-mcp login github     # just one
stripe-billing-ops-mcp status           # what is connected
```

Tokens and keys go to your operating system's keychain (macOS Keychain, Windows Credential Manager, the Secret Service on Linux), and are checked with one read-only call to the app's own API before they are kept. Every key, token and OAuth client is yours: we register no app with any of these services, and nothing passes through a server of ours, because there isn't one.

| App | How it connects | Or set |
|---|---|---|
| Google | Browser sign-in, over your own OAuth client ([make one](https://docs.r28.ai/charter/auth/setup/google)). | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` |
| GitHub | Your own key ([get one](https://github.com/settings/tokens/new?description=Charter&scopes=repo,read:user)), entered once. | `GITHUB_TOKEN` |
| Stripe | Your own key ([get one](https://dashboard.stripe.com/apikeys)), entered once. | `STRIPE_API_KEY` |
| Slack | Your own key ([get one](https://docs.r28.ai/charter/auth/setup/slack)), entered once. A bot token from your own Slack app, which the guide sets up in about three minutes. | `SLACK_BOT_TOKEN` |
| Shopify | Your own key ([get one](https://dev.shopify.com/dashboard)), entered once. | `SHOPIFY_SHOP`, `SHOPIFY_CLIENT_ID`, `SHOPIFY_CLIENT_SECRET` |
| Linear | Your own key ([get one](https://linear.app/settings/account/security)), entered once. | `LINEAR_API_KEY` |
| Notion | Your own key ([get one](https://www.notion.so/profile/integrations)), entered once. Then share the pages it should see with the integration. | `NOTION_API_KEY` |

A variable set in your client's config always wins over the keychain.

## Workflows

| Workflow | What you get | Apps |
|---|---|---|
| **Freelancer invoice from the week's work** <br>`freelancer_invoice_from_the_week_s_work` | Client meetings and commits become line items and a sent invoice. | Google Calendar, GitHub, Stripe |
| **Failed payment follow-up** <br>`failed_payment_follow_up` | Past-due invoices get a human email and the account owner is told. | Stripe, Gmail, Slack |
| **Revenue sheet** <br>`revenue_sheet` | MRR, new, churned and fees appended daily to the sheet finance already uses. | Stripe, Google Sheets |
| **Payout reconciliation** <br>`payout_reconciliation` | Each payout broken into the charges, refunds and fees inside it. | Stripe, Google Sheets |
| **Dispute evidence pack** <br>`dispute_evidence_pack` | Correspondence and fulfillment proof assembled and submitted before the deadline. | Stripe, Gmail, Shopify |
| **Receipts → Drive and the expense sheet** <br>`receipts_to_drive_and_the_expense_sheet` | Every receipt filed and logged without forwarding emails to anyone. | Gmail, Google Drive, Google Sheets |
| **Vendor invoice inbox → approval** <br>`vendor_invoice_inbox_to_approval` | Bills land in a sheet with the PDF and an approval request to the budget owner. | Gmail, Google Drive, Google Sheets, Slack |
| **Plan change by email** <br>`plan_change_by_email` | 'Please move us to annual' handled from the email, with confirmation drafted. | Gmail, Stripe |
| **Investor update draft** <br>`investor_update_draft` | Numbers from billing and progress from the tracker, in your template. | Stripe, Linear, Google Docs, Gmail |
| **Price change rollout** <br>`price_change_rollout` | New price created, affected customers listed and notice drafted, with an FAQ page. | Stripe, Gmail, Notion |
| **Platform fee report** <br>`platform_fee_report` | Fees per connected account per month, for marketplaces on Connect. | Stripe, Google Sheets |
| **SaaS spend audit** <br>`saas_spend_audit` | Every recurring vendor charge in the inbox, with an owner asked to justify it. | Gmail, Google Sheets, Slack |
| **Bulk refunds from a sheet** <br>`bulk_refunds_from_a_sheet` | A list of affected orders after an incident, refunded and marked row by row. | Google Sheets, Stripe |
| **Price list from a sheet** <br>`price_list_from_a_sheet` | The pricing sheet the team agreed on becomes the products Stripe sells. | Google Sheets, Stripe |

Every prompt takes one optional argument, `details`: the repo, team, channel, customer or date range you mean, so the agent does not have to ask. In Claude Code, put it in quotes, or only its first word arrives:

```
/mcp__billing__freelancer_invoice_from_the_week_s_work "client Acme, repo acme/site, last week"
```

Reads run without asking. Before anything that creates, sends, changes or deletes, the prompt tells the agent to show you the call and wait.

0 of the 14 workflows need no Google or Granola credential.

## Other clients

**Claude Desktop**: install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you have not, since Claude Desktop starts the server with it, then open the `.mcpb` from the [latest release](https://github.com/r28ai/stripe-billing-ops-mcp/releases/latest). Claude asks for any keys in its own settings and keeps them in your keychain. The first start takes a few seconds longer, while uv installs it.

**VS Code** (`.vscode/mcp.json`): VS Code asks for each key the first time the server starts and stores it securely. Leave out any you stored with `login`.

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "google-client-secret",
      "description": "Google: OAuth client secret",
      "password": true
    },
    {
      "type": "promptString",
      "id": "github-token",
      "description": "GitHub: Personal access token",
      "password": true
    },
    {
      "type": "promptString",
      "id": "stripe-api-key",
      "description": "Stripe: Secret or restricted key",
      "password": true
    },
    {
      "type": "promptString",
      "id": "slack-bot-token",
      "description": "Slack: Bot token (xoxb-\u2026)",
      "password": true
    },
    {
      "type": "promptString",
      "id": "shopify-client-secret",
      "description": "Shopify: App client secret",
      "password": true
    },
    {
      "type": "promptString",
      "id": "linear-api-key",
      "description": "Linear: Personal API key",
      "password": true
    },
    {
      "type": "promptString",
      "id": "notion-api-key",
      "description": "Notion: Integration secret (ntn_\u2026)",
      "password": true
    }
  ],
  "servers": {
    "billing": {
      "type": "stdio",
      "command": "stripe-billing-ops-mcp",
      "env": {
        "GOOGLE_CLIENT_SECRET": "${input:google-client-secret}",
        "GITHUB_TOKEN": "${input:github-token}",
        "STRIPE_API_KEY": "${input:stripe-api-key}",
        "SLACK_BOT_TOKEN": "${input:slack-bot-token}",
        "SHOPIFY_CLIENT_SECRET": "${input:shopify-client-secret}",
        "LINEAR_API_KEY": "${input:linear-api-key}",
        "NOTION_API_KEY": "${input:notion-api-key}",
        "GOOGLE_CLIENT_ID": "",
        "SHOPIFY_SHOP": "",
        "SHOPIFY_CLIENT_ID": ""
      }
    }
  }
}
```

**Cursor** (`.cursor/mcp.json`) starts it the same way:

```json
{
  "mcpServers": {
    "billing": {
      "command": "stripe-billing-ops-mcp"
    }
  }
}
```

**Codex** (`~/.codex/config.toml`) starts a turn without waiting for a server unless it is `required`, and then the agent has none of its tools. `required = true` makes the session wait for it, and `startup_readiness = "catalog"` waits for its tool list rather than just its connection:

```toml
[mcp_servers.billing]
command = "stripe-billing-ops-mcp"
required = true
startup_readiness = "catalog"
startup_timeout_sec = 30
```

Name the server `billing`. A host builds each tool's name from that key, and a longer one can push a tool past the 64 characters a function name allows.

## Built with Charter

Every tool here is a [Charter](https://github.com/r28ai/charter) declaration: a Pydantic schema saying where each field goes on the wire. Charter's runtime builds the request, attaches and refreshes the credential, and trims the response before the model reads it. It runs in your process, with no proxy and no telemetry.

The 37 tool schemas come to 32,273 tokens.

The same tools work in your own agent, without MCP:

```python
from charter.adapters.openai import to_openai_tools
from charter_packs_mcp import FAMILIES

tools = FAMILIES["finance"].tools()
definitions = to_openai_tools(tools)   # or charter.adapters.langchain
```

Need an API that isn't here? [Write a pack](https://docs.r28.ai/charter/start/coding-agents): your coding agent writes the declarations, and Charter's conformance suite checks them.

<details>
<summary>All 37 tools</summary>

- **Google Calendar**: `gcalendar_events_list`
- **GitHub**: `github_search_commits`
- **Stripe**: `stripe_invoice_items_create`, `stripe_invoices_create`, `stripe_invoices_send`, `stripe_invoices_list`, `stripe_customers_retrieve`, `stripe_subscriptions_list`, `stripe_balance_transactions_list`, `stripe_payouts_list`, `stripe_disputes_list`, `stripe_disputes_retrieve`, `stripe_disputes_update`, `stripe_customers_list`, `stripe_subscriptions_update`, `stripe_balance_retrieve`, `stripe_prices_create`, `stripe_accounts_list`, `stripe_application_fees_list`, `stripe_charges_list`, `stripe_refunds_create`, `stripe_products_create`
- **Gmail**: `gmail_drafts_create`, `gmail_threads_list`, `gmail_messages_list`, `gmail_messages_attachments_get`, `gmail_threads_get`
- **Slack**: `slack_chat_post_message`, `slack_users_list`
- **Google Sheets**: `gsheets_spreadsheets_values_append`, `gsheets_spreadsheets_values_update`, `gsheets_spreadsheets_values_get`
- **Shopify**: `shopify_order_get`
- **Google Drive**: `gdrive_files_create`
- **Linear**: `linear_projects_list`
- **Google Docs**: `gdocs_documents_create`
- **Notion**: `notion_pages_create`

</details>

## License

Apache 2.0.
