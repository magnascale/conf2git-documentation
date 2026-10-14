# Frequently asked questions

Conf2Git – Markdown Sync for Confluence automatically mirrors Confluence spaces to GitHub as
Markdown. These answers describe the currently supported product.

## How well does it handle Confluence-specific elements when converting to Markdown?

Conf2Git converts Confluence's Atlas Doc Format (ADF) into Markdown. It preserves supported
content and makes unsupported content visible, but it does not reproduce every Confluence layout
or interactive feature.

| Element                                 | What to expect                                                                                                                                                                                                                                                           |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Text, headings, lists, quotes, and code | Converted to Markdown. Task lists and code blocks have documented limitations for malformed or complex content.                                                                                                                                                          |
| Macros                                  | Dynamic Jira and other macros are not executed or enriched. Include and excerpt macros do not expand referenced content. Visible text, a safe source link, or a labelled placeholder is retained with a warning.                                                         |
| Panels, expands, and columns            | Informational panels become labelled block quotes. Expand sections and columns are flattened into reading order with a warning; their interactive or visual layout is not preserved.                                                                                     |
| Tables                                  | Simple rectangular tables become Markdown pipe tables. Merged cells, mixed block content, and irregular tables are flattened into a visible quoted representation with a warning.                                                                                        |
| Images and attachments                  | Referenced PNG, JPEG, GIF, and WebP images are mirrored under the page's assets folder within the image limits. SVG and unsupported or unavailable images use a safe source link or placeholder. General attachments such as PDFs and Office documents are not mirrored. |
| Page hierarchy and links                | Nested page directories retain stable page IDs. In-scope links become relative links; moves and renames update affected paths and links together. Out-of-scope or unresolved links retain a safe source link when available, or visible fallback text.                   |
| Live Docs                               | Live Doc and legacy-authored ADF use the same converter and support rules. This exports content, not live collaboration, editor behavior, or a complete Confluence version history.                                                                                      |

Confluence source-access restrictions and app-access rules still apply. **Confluence page
permissions are not reproduced in GitHub.** Access to the exported Markdown and images is governed
by the destination repository's GitHub permissions. Choose a repository and reader access that
are appropriate for the source content before mirroring it.

Review the [conversion support table](conversion-support.md#support-table) for the detailed
supported set. A successful run can contain conversion warnings: use the
[fallback review steps](conversion-support.md#reviewing-conversion_unsupported_node) to decide
whether the generated result is adequate. Content that cannot be converted safely prevents a
mirror update; it is not silently omitted from a successful mirror.

## Is synchronization one-way only, or does it support bidirectional sync and conflict handling?

Synchronization is **one-way: Confluence to GitHub**. Confluence remains authoritative. Conf2Git
does not send GitHub edits back to Confluence or merge competing edits into the source.

There are safeguards for changes in GitHub:

- A later sync may replace human edits to files that Conf2Git can prove it manages, and reports
  `GITHUB_MANAGED_FILE_MODIFIED`. Treat those files as generated output.
- Unowned repository files are preserved. A generated path that collides with an unowned file
  prevents publication rather than overwriting that file.
- If another writer changes the target branch during publication, Conf2Git retries within its
  bounded policy or fails safely. It never force-pushes or writes the default branch.
- An unchanged mirror creates no new commit.

These are publication and ownership safeguards, not bidirectional conflict resolution. See
[managed-file behavior](synchronization-and-managed-files.md#managed-and-unowned-files) and
[publication races](synchronization-and-managed-files.md#no-change-runs-and-publication-races).

## What about scheduling, webhooks, rate limits, private repositories, and deletes, moves, or renames?

**Scheduling and webhooks:** Use **Sync now** for a manual run, or enable the fixed daily schedule
for a ready mapping. New mappings have daily scheduling disabled. The daily opportunity is
managed by Forge and has no exact local-time guarantee. Custom schedules, cron expressions,
webhook-triggered synchronization, and real-time synchronization are not supported. Source
changes are reflected by a subsequent successful sync, not immediately when they happen.

**Rate limits and scale:** Runs honor supported Confluence and GitHub rate-limit guidance and
use bounded retries with backoff. Provider throttling can delay a run; exhausted retries are
reported instead of retrying indefinitely. If throttling prevents publication, the prior mirror
remains intact. Public v1 supports up to five mappings per site, 1,000 pages per mapping/run, and
1,500 generated files per run including the ownership manifest. Images are limited to 10 MiB each and 64 MiB in aggregate
per run; all generated output is limited to 100 MiB per run. These limits are enforced before
publication. See [supported limits](synchronization-and-managed-files.md#exact-public-v1-limits)
and [diagnostics](troubleshooting.md).

**Private repositories:** Yes, private GitHub repositories are supported. Install the verified
GitHub App with **Only select repositories** and include the intended destination. The GitHub
user performing setup or repair must be a repository administrator. The App needs repository
**Contents: read and write** and **Metadata: read** permissions. The sync target must be a
dedicated non-default branch. See [GitHub authorization](github-authorization.md).

**Source changes:** After a healthy, complete reconciliation:

| Change                                                                 | Mirror behavior                                                                                         |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Page edited or added                                                   | Update or add the managed Markdown and eligible images.                                                 |
| Page moved or renamed within the mapping                               | Update the page and affected descendant paths and recalculate internal links in the same mirror update. |
| Page explicitly archived or definitively deleted                       | Remove only its previously managed page and image paths.                                                |
| Page ambiguously missing                                               | Keep output after the first complete miss; removal requires a second consecutive complete miss.         |
| Page-specific access is lost while mapping-wide access remains healthy | Remove the managed mirror promptly during reconciliation and report the access loss.                    |
| Page is proven outside the mapping                                     | Preserve its existing output rather than treating it as a confirmed deletion.                           |
| Mapping-wide access or complete source inventory fails                 | Remove nothing and publish no mirror update.                                                            |

Removing a mapping or uninstalling Conf2Git leaves generated GitHub files in place. Deletion
applies only to files whose prior ownership is verified; it never extends to unrelated repository
content. See [source-change behavior](synchronization-and-managed-files.md#source-changes) and
[removal boundaries](synchronization-and-managed-files.md#rebuild-repair-and-removal-boundaries).

## What is the security model, and how is data handled?

Conf2Git runs on **Atlassian Forge**. Content flows from Confluence through Forge to the selected
GitHub repository. Public v1 has no vendor-operated external content-processing service or
vendor-side page-content store, and it requires no customer-managed server.

Confluence access is read-only. The declared Forge scopes are `read:confluence-user`,
`read:space:confluence`, `read:page:confluence`, `read:attachment:confluence`, and `storage:app`.
There is no Confluence write scope or write path. Administrative setup, configuration, and
recovery operations require server-side Confluence administrator checks.

GitHub access uses the GitHub App with repository **Contents: read and write** and baseline
**Metadata: read** permissions. Select only the repositories that should receive mirrors. Setup
and repair use Forge-managed user authorization; background synchronization uses the verified
App installation. Personal access tokens are not required or supported. Configured GitHub
connections are limited to `https://github.com` and `https://api.github.com`.

Page bodies and image bytes are processed transiently. The intended Markdown and eligible images
are stored in your selected GitHub repository. Tenant-isolated Forge storage retains bounded
configuration and operational metadata, such as source identifiers, versions, paths, hashes,
run status, and recovery state. Page bodies, generated Markdown, and image bytes are not stored
in Forge storage. Credentials, tokens, and customer content are not included in application
logs or diagnostics.

The GitHub mirror has its own access and retention settings. Removing a mapping or uninstalling
the app does not erase that mirror. Read the [data-flow, scopes, and retention guide](security-and-data-flow.md)
for the full boundaries, and the [backup limitations](limitations.md) before relying on generated
output for continuity planning.
