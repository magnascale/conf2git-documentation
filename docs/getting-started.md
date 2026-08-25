# Install and complete the first sync

This guide takes a fresh administrator from installation to a verified one-way **Confluence to
GitHub** mirror. It requires no customer-managed token, GitHub App private key, command line, or
hidden setup step.

## 1. Confirm the prerequisites

You need all of the following:

- a Confluence Cloud site and Confluence site-administrator access;
- an accessible Confluence space to mirror;
- a current paid licence or standard Atlassian Marketplace evaluation for Conf2Git;
- a GitHub repository and a GitHub organization owner or other person authorized to install the
  GitHub App;
- repository-administrator access for the GitHub user who will configure or repair the binding;
- permission to grant the GitHub App **Contents: read and write** access; and
- a dedicated branch name such as `confluence-sync` that is not the repository default branch.

Choose the repository and base path before starting. A repository base path is a non-empty,
repository-relative folder such as `confluence/engineering`. Do not use a leading slash,
backslash, `..`, or an empty path segment. Two mappings cannot overlap on the same repository and
branch.

## 2. Install the Marketplace app

In Confluence, open **Apps**, then **Manage your apps** or the equivalent **Connected apps** view.
Find **Conf2Git – Markdown Sync for Confluence** in Atlassian Marketplace and start the standard
evaluation or subscribe. Installation and licensing are separate from GitHub authorization.

Open the app's **Configure** page as a Confluence site administrator. If synchronization is paused
with `MARKETPLACE_UNLICENSED` or `MARKETPLACE_LICENSE_EXPIRED`, use Atlassian Administration to
start an evaluation, purchase, or renew before the first sync. Existing configuration and output
are preserved while synchronization is paused.

## 3. Install the GitHub App

Use the verified GitHub App installation link displayed by Conf2Git. In GitHub:

1. Choose the intended personal account or organization.
2. Choose **Only select repositories**.
3. Select only the repository or repositories that may receive mirrors.
4. Review the requested permissions: repository **Contents: read and write** and baseline
   **Metadata: read**.
5. Install the App, or request organization-owner approval if GitHub requires it.

This installation grants the App repository access. It does not create a mapping and does not
start synchronization.

## 4. Authorize interactive repository discovery

Select **Authorize GitHub** in Conf2Git and complete the Forge-managed consent flow. When Conf2Git
observes the consent flow returning, it discards the prior status and performs one fresh automatic
authorization-status read. If that return cannot be observed or the fresh read is unavailable,
select **Refresh authorization status** once.

This authorization lets the current administrator discover and verify installations and
repositories during setup. It is not the credential used by background synchronization. Conf2Git
does not receive a token that you can view, copy, or enter into the form.

## 5. Create the draft mapping

Select **Create draft mapping** and complete the fields:

- **Confluence space**: choose an accessible source space.
- **GitHub repository owner** and **GitHub repository name**: identify the intended destination.
  These text fields are format-checked only at this stage.
- **Target branch**: keep `confluence-sync` or choose another dedicated branch. It must not be the
  current default branch.
- **Repository base path**: use a normalized repository-relative path such as
  `confluence/engineering`.

Select **Save draft mapping**. A draft is configuration only: it has no verified GitHub binding and
cannot synchronize. Public v1 permits at most five mappings that have not been removed per
Confluence site. New mappings show **Daily schedule: Disabled** by default. Select **Enable daily
schedule** only when you want the mapping to use Conf2Git's fixed Forge-managed daily opportunity;
the mapping must still become **Ready** before automatic synchronization is eligible.

## 6. Bind and test the repository

On the draft mapping, select **Configure connection**:

1. Select the GitHub App installation returned by the server.
2. Select the intended repository returned by the server.
3. Review the exact repository, target branch, and base path.
4. Select **Test candidate without activating**.
5. After a successful test, select **Activate tested binding**.

The server—not the browser—fully validates the expected App, active installation, stable
repository identity and visibility, current GitHub user's repository-administrator permission,
selected-repository access, required App permissions, and the non-default target branch. It may
create an unreachable Git blob to prove Contents write access. The test does not create a commit,
create or update a branch, publish files, or start synchronization.

A successful activation makes the mapping **Ready**. A rejected or indeterminate candidate leaves
the previous binding unchanged. Repository and installation IDs shown by the UI are correlation
details; they do not authorize access by themselves.

## 7. Start the first synchronization

On a **Ready** mapping, select **Sync now**. The request returns quickly and queues a run. The same
bounded reconciliation engine is used for manual and eligible daily work. **Sync now** remains
available whether the daily schedule is enabled or disabled. Use **Enable daily schedule** or
**Disable daily schedule** on the mapping card to change automatic eligibility; the cadence is
fixed to daily and has no time-of-day or timezone setting.

Do not start another mapping operation while the run is active. In **Mapping overview**, check:

- **Queued** or **In progress** evidence and the current phase when available;
- the run ID;
- discovered and processed counters;
- the latest attempt independently from the last successful mirror; and
- the next scheduled opportunity. A daily schedule is a Forge-managed opportunity, not an exact
  wall-clock promise. If the mapping shows **Schedule disabled**, only manual synchronization is
  available under the current configuration. After changing the setting, confirm the persisted
  enabled or disabled state in the mapping card and overview.

Long runs may continue in the background. While exact run evidence remains **Queued** or **In
progress**, the visible overview automatically performs bounded, non-overlapping status refreshes
and stops when the run becomes terminal or evidence becomes unavailable. It pauses those refreshes
while the page is hidden and checks again when you return. A temporary unavailable-progress
message means Conf2Git cannot prove a coherent current snapshot; refresh later rather than
starting competing work.

## 8. Confirm success

Open **Run history and page outcomes** for the mapping. Select **View exact run details** on a run
to expand its retained detail directly beneath that run's summary. A successful first run is
`SUCCEEDED` or `SUCCEEDED_WITH_WARNINGS` and shows a commit link. The link opens through the Forge
navigation boundary and remains copyable if navigation fails. Warnings do not necessarily mean
publication failed; review each stable diagnostic in [Diagnostics and
troubleshooting](troubleshooting.md).

In GitHub, verify all of the following:

- the configured non-default target branch exists;
- the repository default branch is unchanged;
- the configured base path contains page directories ending in `--<page-id>/index.md`;
- referenced supported images appear under their page's `assets/` directory;
- `<base>/.conf2git/manifest.json` exists; and
- the commit link shown by Conf2Git points to the target branch's published commit.

The ownership manifest is application data; do not edit or replace it. Treat the target branch as
generated output. A later reconciliation may replace human edits to files that the valid manifest
and publication provenance prove are managed.

## 9. Learn the operating boundaries

Before regular use, read:

- [Synchronization and managed-file behavior](synchronization-and-managed-files.md), including
  the exact scale limits and collision rules;
- [Conversion support and image behavior](conversion-support.md);
- [Recovery and lifecycle operations](recovery-and-lifecycle.md); and
- [Backup and disaster-recovery limitations](limitations.md).
