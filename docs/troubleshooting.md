# Diagnostics and troubleshooting

Conf2Git returns bounded stable codes instead of raw provider errors. Start with the code, mapping
ID, run ID, and timestamp. A failed or indeterminate run does not publish a partial candidate.

## Diagnostic inventory

These are all customer-visible run and item diagnostic codes in the production catalog.

| Code                              | Meaning and publication impact                                                                     | Safe administrator action                                                        |
| --------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `RUN_ALREADY_ACTIVE`              | Another run already owns the mapping; no second run starts.                                        | Open the active run and wait for it to finish.                                   |
| `RUN_STALE_RESUMED`               | Conf2Git safely resumed stale worker ownership; the run may continue.                              | Monitor the run; contact support only if it repeats without progress.            |
| `RUN_CHECKPOINT_FAILED`           | Durable progress could not be recorded; publication is prevented.                                  | Retry; contact support if it repeats.                                            |
| `RUN_QUEUE_HANDOFF_FAILED`        | Work could not be queued; no mirror update occurs.                                                 | Start a new manual run; contact support if it repeats.                           |
| `RUN_RETRY_EXHAUSTED`             | Bounded upstream retries ended; publication is prevented.                                          | After the upstream service recovers, start a new run.                            |
| `RUN_RETRY_METADATA_INVALID`      | Stored retry evidence was unsafe; publication is prevented.                                        | Start a new run; contact support if it repeats.                                  |
| `MARKETPLACE_LICENSE_EXPIRED`     | The Marketplace licence expired; synchronization and publication are denied.                       | Renew or purchase through Atlassian Marketplace, then retry.                     |
| `MARKETPLACE_UNLICENSED`          | No active paid licence or evaluation was proven; synchronization is denied.                        | Start an evaluation or purchase through Atlassian Marketplace, then retry.       |
| `CONFLUENCE_AUTH_FAILED`          | Conf2Git could not prove Confluence read authorization; publication is prevented.                  | Reinstall or approve the app permissions shown by Atlassian.                     |
| `CONFLUENCE_SPACE_UNREADABLE`     | The selected space cannot be read completely; publication is prevented.                            | Verify the space selection and app access.                                       |
| `CONFLUENCE_PAGE_ACCESS_LOST`     | A page-specific access loss was proven; its managed mirror may be removed in a complete safe run.  | Review page permissions and the item outcome.                                    |
| `CONFLUENCE_APP_ACCESS_BLOCKED`   | Atlassian app-access policy blocked required reads; publication is prevented.                      | Review Atlassian app access and data-security policy.                            |
| `CONFLUENCE_INVENTORY_INCOMPLETE` | The complete source inventory was not proven; nothing is deleted or published.                     | Retry after Confluence recovers.                                                 |
| `CONFLUENCE_RATE_LIMITED`         | Confluence asked Conf2Git to slow down; the bounded run may retry.                                 | Wait for automatic retry; start a new run only after terminal failure.           |
| `CONFLUENCE_INVALID_HIERARCHY`    | A page is orphaned or cyclic; safe output may contain a warning.                                   | Review the affected item and repair the Confluence hierarchy.                    |
| `GITHUB_AUTH_INVALID`             | Installation authorization is invalid; publication is prevented.                                   | Reauthorize, then test the saved binding.                                        |
| `GITHUB_REPO_NOT_FOUND`           | The bound repository is unavailable; publication is prevented.                                     | Verify the repository and installation selection.                                |
| `GITHUB_WRITE_FORBIDDEN`          | Required Contents write access is missing; publication is prevented.                               | Grant the App Contents read/write access, then test the connection.              |
| `GITHUB_BRANCH_PROTECTED`         | Branch rules reject the App's non-force update; publication is prevented.                          | Allow the App to update the dedicated branch or choose another dedicated branch. |
| `GITHUB_REF_CONFLICT`             | Another writer moved the target ref; Conf2Git does not overwrite it.                               | Wait for the other writer, then retry.                                           |
| `GITHUB_RATE_LIMITED`             | GitHub asked Conf2Git to slow down; the bounded run may retry.                                     | Wait for automatic retry; start a new run only after terminal failure.           |
| `GITHUB_RESPONSE_INVALID`         | GitHub returned an unsafe or unexpected shape; publication is prevented.                           | Retry; contact support if it persists.                                           |
| `GITHUB_UPSTREAM_UNAVAILABLE`     | GitHub was unavailable; publication is prevented.                                                  | Retry after GitHub service availability recovers.                                |
| `GITHUB_MANAGED_FILE_MODIFIED`    | A manifest-owned file changed outside Conf2Git; a complete run may replace it.                     | Treat the branch as generated or review the downstream edit.                     |
| `MANIFEST_MISSING`                | Prior ownership cannot be proven; destructive reconciliation is prevented.                         | Use the confirmed manifest-repair workflow if offered.                           |
| `MANIFEST_CORRUPT`                | The ownership manifest is invalid; destructive reconciliation is prevented.                        | Use the confirmed manifest-repair workflow if offered.                           |
| `MANIFEST_PROVENANCE_INVALID`     | The manifest is not proven to be app-published; destructive reconciliation is prevented.           | Review repository history; contact support before repair.                        |
| `MANIFEST_OWNERSHIP_CONFLICT`     | Desired output collides with unowned or inconsistently owned content; nothing is published.        | Move the unowned path or change the base path; do not delete files blindly.      |
| `PATH_INVALID`                    | A generated or configured path is unsafe; publication is prevented.                                | Correct the title, branch, or base path identified by the UI.                    |
| `CONVERSION_UNSUPPORTED_NODE`     | ADF content was degraded to text, a link, or a placeholder; publication may succeed with warnings. | Review the generated page and source; contact support for a repeatable gap.      |
| `CONVERSION_FAILED`               | Safe Markdown could not be produced; the complete run is not published.                            | Simplify or repair the affected Confluence content, then retry.                  |
| `ASSET_TOO_LARGE`                 | A referenced image exceeds 10 MiB; it is represented by a safe fallback.                           | Reduce the image below the limit if mirroring it is required.                    |
| `ASSET_TYPE_UNSUPPORTED`          | The referenced image type is not PNG, JPEG, GIF, or WebP; a fallback is used.                      | Convert it to a supported image type if mirroring it is required.                |
| `ASSET_DOWNLOAD_FAILED`           | An eligible image could not be downloaded; a fallback is used when safe.                           | Verify attachment access and retry.                                              |
| `PUBLIC_V1_LIMIT_EXCEEDED`        | A documented page, file, image, or byte ceiling was exceeded; nothing is published.                | Reduce the mapping below the exact documented limit.                             |
| `STORAGE_LIMITED`                 | Forge storage could not safely accept required bounded state; publication is prevented.            | Retry later; contact support if it persists.                                     |

For `CONVERSION_UNSUPPORTED_NODE`, use the
[conversion fallback review and remediation path](conversion-support.md#reviewing-conversion_unsupported_node)
to interpret the exact run's publication outcome, review commit and output-path evidence, accept
an adequate fallback with no action, or change unsupported source content before synchronizing
again.

## GitHub setup and authorization diagnostics

These codes appear while testing, activating, or repairing a GitHub binding. A rejected or
unavailable test preserves the current binding and starts no synchronization.

| Code                                | Meaning                                                                | Safe administrator action                                                                                             |
| ----------------------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `AUTHORIZATION_REQUIRED`            | Forge-managed GitHub consent is missing.                               | Select **Authorize GitHub**, complete consent, and wait for the fresh status read; refresh once if it is unavailable. |
| `AUTHORIZATION_REVOKED`             | Interactive consent was revoked.                                       | Select **Reauthorize GitHub**, then test the saved binding.                                                           |
| `APP_IDENTITY_MISMATCH`             | The installation belongs to a different GitHub App.                    | Install and select the verified Conf2Git GitHub App.                                                                  |
| `INSTALLATION_UNAVAILABLE`          | The selected installation cannot be fully verified.                    | Confirm it still exists and grants access, then refresh.                                                              |
| `INSTALLATION_SUSPENDED`            | GitHub reports the installation as suspended.                          | Have the installation owner unsuspend it, then test again.                                                            |
| `REPOSITORY_ADMIN_REQUIRED`         | The current GitHub user is not a repository administrator.             | Ask a repository administrator to perform the test and activation.                                                    |
| `APP_PERMISSIONS_INSUFFICIENT`      | The installation lacks required repository permissions.                | Grant Contents read/write and retry the test.                                                                         |
| `REPOSITORY_UNAVAILABLE`            | The exact repository is missing, inactive, unrelated, or not selected. | Review selected-repository access or choose a valid replacement.                                                      |
| `TARGET_BRANCH_UNAVAILABLE`         | The target is invalid, is the default branch, or cannot be verified.   | Choose a dedicated non-default branch and retry.                                                                      |
| `CONTENTS_WRITE_FAILED`             | The unreachable-blob write probe did not succeed safely.               | Review App Contents permission and repository policy.                                                                 |
| `UPSTREAM_RESPONSE_INVALID`         | GitHub returned malformed or incomplete verification evidence.         | Refresh and retry; contact support if it persists.                                                                    |
| `ENVIRONMENT_CONFIGURATION_INVALID` | The deployed App identity or required vendor configuration is invalid. | Contact support; do not create alternate credentials.                                                                 |

## Bounded workflow messages

- **Synchronization could not be started**: refresh the mapping. It must be ready, entitled, and
  free of another active run. The server starts work only when those facts are current.
- **Progress unavailable**: current synchronization evidence did not form one coherent snapshot.
  Refresh later; do not infer that publication happened.
- **GitHub authorization status unavailable**: the bounded global status read could not prove a
  current result. This is not proof of revocation and does not change a saved mapping. Refresh the
  authorization status once and follow only the diagnostic/action then shown.
- **Run or item unavailable**: the requested record is outside the bounded history/detail window,
  stale, malformed, or not part of the mapping. This does not recreate or change it.
- **Plan unavailable/refused/rejected**: no rebuild or repair starts. Read the reason code in
  [Recovery and lifecycle operations](recovery-and-lifecycle.md#plan-and-confirmation-reasons).

## What to collect for support

Provide the mapping ID, run ID, stable code, timestamp, phase and bounded counters, repository
owner/name, target branch, and displayed non-secret installation/repository IDs. You may also
provide the Conf2Git commit link and a description of the visible generated result.

Never provide page or Markdown bodies, image or attachment bytes, a private key, OAuth secret,
JWT, token, authorization header, callback code, raw provider response, Marketplace payload,
licence context, billing identifier, entitlement identifier, or stack trace.
