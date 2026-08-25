# Conf2Git customer documentation

**Conf2Git – Markdown Sync for Confluence**

Automatically mirror Confluence spaces to GitHub as Markdown.

Conf2Git is a one-way **Confluence to GitHub** mirror for Confluence Cloud. Confluence remains the
source of truth. Conf2Git never writes back to Confluence.

## Start here

If this is your first installation, follow [Install and complete the first
sync](getting-started.md). It covers the complete administrator journey from Marketplace
installation through verifying the generated GitHub branch.

Before setup, make sure you have:

- Confluence site-administrator access;
- a current paid licence or standard Atlassian Marketplace evaluation;
- a GitHub organization owner or authorized GitHub App installer available;
- repository-administrator access for the GitHub user who will verify the connection; and
- a dedicated target branch name that is not the repository default branch.

## Guides

- [Install and complete the first sync](getting-started.md)
- [GitHub authorization and branch behavior](github-authorization.md)
- [Data flow, scopes, permissions, storage, and retention](security-and-data-flow.md)
- [Synchronization and managed-file behavior](synchronization-and-managed-files.md)
- [Conversion support and image behavior](conversion-support.md)
- [Diagnostics and troubleshooting](troubleshooting.md)
- [Recovery and lifecycle operations](recovery-and-lifecycle.md)
- [Backup and disaster-recovery limitations](limitations.md)

## What Conf2Git does not do

Conf2Git does not provide two-way synchronization, real-time synchronization, publishing changes
back to Confluence, a complete Confluence backup, or a general disaster-recovery system. It supports
GitHub only. Read [Backup and disaster-recovery limitations](limitations.md) before depending on
the generated output for continuity planning.

## Getting help safely

Start with the stable code shown in **Run details**, the mapping ID, and the run ID. The
[diagnostic inventory](troubleshooting.md#diagnostic-inventory) maps every production run or item
code to a safe action. Never send support a private key, OAuth secret, JWT, user or installation
token, authorization header, raw provider response, licence context, page or Markdown body, or
attachment or image bytes.
