# GitHub authorization and branch behavior

## Authentication model

GitHub App installation authentication is the only supported GitHub authentication model.
Conf2Git does not support personal access tokens, classic tokens, fine-grained personal access
tokens, deploy keys, or machine-user credentials.

Interactive setup and unattended synchronization have distinct purposes:

- The current Confluence administrator completes Forge-managed GitHub authorization to discover
  and verify installations and repositories they may administer.
- Background work uses the verified GitHub App installation binding. It does not depend on the
  original administrator's continuing employment or user token.

Frontend values, a setup link, an installation ID, a repository ID, a prior connection test, and
displayed authorization state are never sufficient authority. The server revalidates the exact
binding at the protected operation boundaries.

## GitHub permissions

| Permission          | Level          | Customer-visible purpose                                                                                                                                                     |
| ------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Repository Contents | Read and write | Read the selected repository's commits, trees, blobs, and refs; create generated blobs, one complete commit, and a non-force update or creation of the dedicated target ref. |
| Repository Metadata | Read           | Identify and validate the selected repository, visibility, default branch, and stable repository identity.                                                                   |

The App requests no organization or account permission and subscribes to no GitHub events. Select
only the intended repositories when installing it.

## Connection verification

The server verifies the expected App and active installation, exact stable repository ID,
canonical repository identity and visibility, current GitHub user's returned administrator
permission, required App permissions, repository selection, and target-branch state. Contents
write is checked with an unreachable blob. Testing a connection does not create a commit or change
a visible ref.

The GitHub user who runs setup or repair must be a repository administrator. This requirement is
for server-side configuration verification; background mirroring remains installation-owned.

## Target branch rules

- The target must be a dedicated non-default branch. The default is `confluence-sync`.
- Conf2Git never writes the repository default branch.
- If the target is absent on the first sync, the current default-branch tree is used only as the
  publication base. The target ref is created directly at the completed Conf2Git commit after the
  entire run passes.
- If the target exists, Conf2Git protects the captured head with an exact-head compare-and-swap.
- Ref updates are non-force. Conf2Git never force-pushes.
- If another writer moves the target head, Conf2Git retries within its bounded policy or fails with
  `GITHUB_REF_CONFLICT`; it does not overwrite the other writer.
- Durable success is recorded only after the expected ref, commit, and ownership manifest are
  reread and verified.

Branch protection must allow the GitHub App to update the dedicated branch. Never solve a branch
protection problem by selecting the default branch.

## Reauthorization and binding replacement

Use **Reauthorize GitHub** when Forge-managed user consent is missing or revoked. Conf2Git performs
one fresh status read when it observes the consent flow returning; use **Refresh authorization
status** if that return or read was unavailable. Returning focus alone never proves authorization.
On the mapping card, select **Test connection** to open the repair panel, then use **Test current
binding** for the saved connection. When an installation was uninstalled and reinstalled, or the
intended repository genuinely changed, use **Change connection**, test the replacement, and
activate it only after reviewing the exact destination.

An unavailable global authorization status does not by itself prove that consent was revoked and
does not change a saved mapping binding. Refresh the status once and follow **Reauthorize GitHub**
only when Conf2Git reports the corresponding authorization-required or revoked diagnostic.

The current binding remains authoritative until the replacement passes a fresh server validation
and the atomic activation succeeds. Testing or activating a binding does not start a sync, publish
files, clean repository content, change the schedule, or alter the last successful mirror.

See [Authorization-loss recovery](recovery-and-lifecycle.md#authorization-loss-and-rebinding) and
the [GitHub setup diagnostic table](troubleshooting.md#github-setup-and-authorization-diagnostics).

## Private-key rotation is not a customer task

The GitHub App private key is a vendor environment secret. Customers must not possess, inspect,
upload, paste, transmit, or rotate it. During planned vendor key rotation, a synchronization may
temporarily fail closed. The prior mirror remains intact. After the vendor completes replacement
and validation, an administrator should open **Test connection** and run **Test current binding**
only if Conf2Git displays an authorization action.

Customer reauthorization does not rotate the App private key. Vendor operators use a separate,
restricted rotation procedure that is not a customer setup workflow.

## Safe information for support

You may provide the mapping ID, run ID, stable diagnostic code, timestamp, canonical repository
owner/name, non-default target branch, and the displayed installation and repository IDs. Never
provide a private key, OAuth secret, JWT, token, authorization header, callback code, raw GitHub
response, repository content, or Confluence content.
