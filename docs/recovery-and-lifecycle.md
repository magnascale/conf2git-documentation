# Recovery and lifecycle operations

All lifecycle operations require a current Confluence site administrator and are server-authorized;
frontend state and prior tests do not grant authority. Operations that start synchronization,
including retry/resume and confirmed rebuild or manifest repair, also require current Marketplace
entitlement. Authorization status, **Test connection**, **Test current binding**, **Reauthorize
GitHub**, **Change connection**, and mapping removal remain available while entitlement pauses
synchronization.

## Recovery matrix

| Operation                    | Use it when                                                                                                       | What it changes and preserves                                                                                                                                        | Starts synchronization?                                   |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| Retry or resume              | Run history offers the existing safe action after a recoverable failure.                                          | Reuses the bounded manual synchronization workflow. Publication recovery, when present, remains tied to the exact run and due time.                                  | Yes, as background work; never inside the button request. |
| Test current binding         | The saved GitHub binding may have lost access.                                                                    | Revalidates the current App, installation, repository, admin permission, Contents permission, and branch. It changes no binding, files, success record, or schedule. | No.                                                       |
| Reauthorize GitHub           | Forge-managed interactive GitHub consent is missing or revoked.                                                   | Restores current-user discovery/verification consent; it does not replace the background installation binding or rotate a private key.                               | No.                                                       |
| Change connection            | The installation was replaced or a different repository is intentionally required.                                | Tests a candidate first. Activation atomically replaces only the exact current binding and authorization health; stale attempts lose.                                | No.                                                       |
| Rebuild                      | Conf2Git or support directs an administrator to regenerate managed files after an exceptional recovery condition. | Uses a reviewed immutable dry-run plan, then complete reconciliation. It may change only provenance-valid managed output and preserves every unowned file.           | Yes, only after exact confirmation.                       |
| Manifest repair              | The UI proves that the canonical ownership manifest alone is repairable from verified history.                    | Restores exactly one manifest path; it changes no page/image, moves nothing, and deletes nothing.                                                                    | Yes, only after exact confirmation.                       |
| Remove mapping               | The administrator intentionally retires the mapping.                                                              | Deletes the mapping, stored binding association, schedule acceptance, and referenced authorization audit. Repository output and the GitHub App remain.               | No.                                                       |
| Uninstall the Confluence app | The site administrator is ending use of the Forge app.                                                            | Atlassian manages the uninstall. Do not assume it removes GitHub output or separately uninstalls the GitHub App.                                                     | No.                                                       |

## Authorization loss and rebinding

Background authorization loss atomically fails the affected run, releases its active ownership, and
marks only that exact mapping **Needs attention**. It does not authorize publication or cleanup.
Select **Test connection** to open the repair panel and use **Test current binding** first. If
consent is missing, use **Reauthorize GitHub**. If the
installation or repository binding genuinely changed, use **Change connection**, test the
candidate, and activate it. Only an authorization-caused needs-attention state may return to
**Ready** through this repair flow.

A vendor GitHub App private-key rotation is not customer reauthorization. Customers never receive
or rotate that key. Existing output remains intact while the service fails closed; follow only an
authorization action displayed by Conf2Git after the vendor completes rotation.

Success is recognized when the current-binding test passes or an exactly tested replacement is
activated and the mapping returns to **Ready**. These actions still do not synchronize.

## Pending removal and source access

A first complete run that ambiguously misses a page records a pending-removal observation and
keeps its managed output. A second consecutive complete miss may authorize removal. If the page
returns, is proven outside the mapping, or the observation cannot be completed safely, the prior
output is preserved. A mapping-wide inventory or authorization failure never authorizes deletion.

For a proven page-specific access loss, review and restore the page permissions if the mirror
should remain. Success is recognized by a later complete run that can read the page again. Do not
use mapping removal or manifest repair to work around incomplete source access.

## Entitlement loss and restoration

An expired or inactive licence denies new work and prevents publication, but preserves the
mapping, GitHub binding, generated output, ownership state, last-known-good success, and retained
history. A site administrator restores an active paid licence or standard evaluation through
Atlassian Administration. Then refresh Conf2Git and start or resume only the action offered by the
current UI. Success is recognized by a newly accepted run; licence restoration itself does not
publish or clean up files.

## Stale work and support escalation

Ordinary queued work should be left to its automatic retries. If the UI reports a stale run, the
same run becomes eligible for fenced recovery after five minutes without a valid heartbeat; this
does not mean that every run should finish within five minutes. After bounded platform delivery
retries end, a later server-accepted manual recovery request for the same mapping, when offered, or
the daily dispatcher may enqueue only the exact identifier-only event proven by the unchanged run,
stale worker lease, and unexpired checkpoint. The existing worker must still recover and revalidate
the same run; no replacement run is created. Refresh and use an offered safe retry/resume action
when available. Do not create competing mappings or edit the generated branch to force recovery.

Contact support after the documented provider or configuration action has been completed and the
same stable code repeats, when current state remains unavailable, or when vendor configuration is
identified. Provide only the bounded non-secret information listed in
[Diagnostics and troubleshooting](troubleshooting.md#what-to-collect-for-support).

## Advanced recovery tools

Most administrators should never need the controls under **Advanced recovery tools** during
routine operation. Conf2Git keeps the general rebuild action collapsed on a healthy mapping so it
is not mistaken for regular maintenance. Expand it only when Conf2Git or support directs you to
regenerate managed files. Creating the rebuild plan is a dry run; it changes no GitHub file until
the exact plan is reviewed and confirmed.

Manifest repair remains a contextual action. Conf2Git offers **Review manifest repair plan**
directly when the latest validated attempt proves that the mapping is in **Repair required**
state. Do not use rebuild or manifest repair speculatively, on a schedule, or as a substitute for
ordinary **Sync now**, retry, authorization repair, or source-access recovery.

## Rebuild and manifest-repair confirmation

Creating a plan does not change the repository. Review the summary and paginated operations. The
plaintext confirmation handle is returned once and kept only in the current browser component;
refreshing loses it. A plan can be confirmed for 30 minutes and its bounded plan material is
retained for at most eight days. If any mapping, repository, branch, run, or plan fence changes,
confirmation fails and no operation begins.

Manifest repair is deliberately narrower than rebuild: one canonical manifest `ADD` or `UPDATE`
from independently verified historical provenance. Rebuild is still a complete current-source
reconciliation, not a historical restore.

## Plan and confirmation reasons

Plan refusal means no plan was issued:

| Reason                                  | Administrator response                                              |
| --------------------------------------- | ------------------------------------------------------------------- |
| `INPUT_INVALID`                         | Refresh and use the current mapping action.                         |
| `MAPPING_UNAVAILABLE`                   | Confirm the mapping still exists and belongs to this site.          |
| `MAPPING_INELIGIBLE`                    | Restore the mapping to an eligible state before planning.           |
| `MAPPING_STALE`                         | Refresh; the mapping changed during the request.                    |
| `ACTIVE_RUN_UNAVAILABLE`                | Wait for or recover the active run before planning.                 |
| `PENDING_PUBLICATION_RECOVERY_REQUIRED` | Complete the offered exact publication recovery first.              |
| `EXISTING_PLAN_UNEXPIRED`               | Use the current unexpired plan or wait for expiry.                  |
| `PLANNING_EXPIRED`                      | Request a new plan.                                                 |
| `REBUILD_INELIGIBLE`                    | Resolve the mapping or ownership condition shown by the UI.         |
| `MANIFEST_REPAIR_INELIGIBLE`            | The narrow historical-provenance repair boundary was not proven.    |
| `MANIFEST_REPAIR_NOT_REQUIRED`          | The current manifest does not need the narrow repair.               |
| `TARGET_MISSING_AFTER_PRIOR_SUCCESS`    | Restore or investigate the dedicated target branch before planning. |
| `REPOSITORY_STALE`                      | Refresh; repository identity or evidence changed.                   |
| `BRANCH_STALE`                          | Refresh; the target branch changed.                                 |
| `STATE_UNAVAILABLE`                     | Retry later; safe current state was unavailable.                    |

Confirmation rejection starts no work:

| Reason                   | Administrator response                                             |
| ------------------------ | ------------------------------------------------------------------ |
| `MALFORMED_CONFIRMATION` | Return to the current plan and use its exact confirmation control. |
| `MAPPING_MISMATCH`       | Open the plan from the matching mapping.                           |
| `PLAN_UNAVAILABLE`       | Request a new plan if the operation is still required.             |
| `PLAN_MISMATCH`          | Refresh and use the exact current plan.                            |
| `PLAN_EXPIRED`           | Request and review a new plan.                                     |
| `MAPPING_STALE`          | Refresh and request a new plan.                                    |
| `REPOSITORY_STALE`       | Recheck the binding, then request a new plan.                      |
| `BRANCH_STALE`           | Review the changed target branch, then request a new plan.         |
| `ACTIVE_RUN_UNAVAILABLE` | Wait for or recover the active run.                                |
| `STATE_UNAVAILABLE`      | Retry later; no work started.                                      |

Plan reads and operation pages can also return `CURSOR_INVALID` or
`CURSOR_STALE_OR_FOREIGN`; reopen the plan and use its current first page. They may use the same
`INPUT_INVALID`, `PLAN_UNAVAILABLE`, `PLAN_MISMATCH`, or `STATE_UNAVAILABLE` responses above.

## Removal and uninstall

Mapping removal is one-shot and never contacts GitHub. It does not uninstall the GitHub App and
does not change or delete repository files. If acknowledgment is unavailable, refresh the mapping
list rather than repeatedly issuing removal.

The Confluence app and GitHub App are installed and removed in different provider administration
surfaces. If ending service, first record the mapping and generated-branch state needed by your
own retention process, remove mappings through Conf2Git if desired, uninstall the Confluence app
through Atlassian Administration, and separately review the GitHub App installation in GitHub.
Conf2Git provides no bulk generated-file cleanup operation.
