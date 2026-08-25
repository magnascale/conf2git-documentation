# Conversion support and image behavior

Conf2Git converts Confluence Atlas Doc Format (ADF) with its project-owned deterministic
converter. The table describes current behavior; it does not promise perfect or lossless
fidelity. Unsupported or degraded content remains visible through preserved text, a safe source
link, a stable placeholder, or a structured warning when safe output can be produced.

## Reviewing `CONVERSION_UNSUPPORTED_NODE`

This warning means Conf2Git produced safe Markdown but could not represent part of the Confluence
structure faithfully. The fallback can preserve visible text, use a safe source link, flatten
content into reading order, or emit a visible placeholder.

Use the exact run outcome before deciding what to do:

- **Succeeded with warnings and a recorded commit:** the mirror was published with the fallback.
  Open the commit from **Run details**, show the affected outcomes, and locate each displayed
  **Output path** in that commit.
- **Succeeded with warnings and no change:** no new commit was needed. Review the displayed output
  path on the existing dedicated mirror branch.
- **Failed, partial, or cancelled:** that attempt published no mirror update. Change the source and
  synchronize again before reviewing a later successful commit.

If the generated fallback is adequate, accept it with no action. Retrying unchanged Confluence
content produces the same fallback and does not improve fidelity. If fidelity is inadequate,
replace the unsupported Confluence construct with a supported construct from the table below, then
synchronize again. Report a repeatable conversion gap when content documented as supported still
degrades; provide the stable code, run ID, Page ID, output path, and recorded commit link, but do
not send page content, ADF, generated Markdown, or raw provider data.

## Support table

| Confluence content                                              | Status                                | Current Markdown behavior and limitation                                                                                                        |
| --------------------------------------------------------------- | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Paragraphs and hard breaks                                      | Supported                             | Plain text is escaped for safe Markdown; hard breaks are preserved.                                                                             |
| Headings                                                        | Supported                             | ATX headings; levels are clamped to 1–6.                                                                                                        |
| Duplicate, case-conflicting, non-ASCII, and long page titles    | Supported within path limits          | Stable page IDs disambiguate paths; safe path normalization and length bounds still apply.                                                      |
| Strong, emphasis, strike, and inline code marks                 | Supported                             | Deterministic CommonMark-compatible marks; inline-code fences expand around backticks.                                                          |
| Unknown text marks or duplicate link marks                      | Supported with limitations            | Visible text is retained; unsupported mark semantics are dropped with `CONVERSION_UNSUPPORTED_NODE`.                                            |
| Ordered, unordered, and nested lists                            | Supported                             | Normalized Markdown list indentation.                                                                                                           |
| Task lists                                                      | Supported with limitations            | Emits `- [ ]` and `- [x]`; malformed child/state shapes are made visible with warnings.                                                         |
| Simple tables                                                   | Supported                             | Rectangular single-block cells become pipe tables.                                                                                              |
| Complex tables                                                  | Supported with limitations            | Spans, mixed block cells, or irregular shapes are flattened into a visible quoted representation with a warning.                                |
| Block quotes and horizontal rules                               | Supported                             | Converted to Markdown quotes and rules.                                                                                                         |
| Fenced code blocks                                              | Supported with limitations            | Language is retained only when safe; fences expand as needed. Invalid language or complex child content is removed or flattened with a warning. |
| Informational panels                                            | Supported                             | Converted to labelled block quotes.                                                                                                             |
| Expand and nested expand                                        | Supported with limitations            | Content is flattened in reading order with an explicit label and warning; interactive expansion is not preserved.                               |
| Layout sections and columns                                     | Supported with limitations            | Flattened in reading order with a warning; visual column layout is not preserved.                                                               |
| Mentions                                                        | Supported with limitations            | Display text becomes plain `@name` text; there is no user-directory enrichment.                                                                 |
| Emoji                                                           | Supported with limitations            | Display text or short name is retained; missing display text becomes a placeholder with a warning.                                              |
| Smart links                                                     | Supported                             | Safe URL and label become a normal Markdown link.                                                                                               |
| In-scope internal page links                                    | Supported                             | Stable page IDs are resolved to relative links after the complete path map is known.                                                            |
| Renamed parents and moved descendants                           | Supported                             | Complete path and link planning updates descendant paths and affected internal links together.                                                  |
| Out-of-scope, inaccessible, or unresolved Confluence links      | Supported with limitations            | A safe Confluence source URL is retained when available; otherwise visible unresolved text or a placeholder remains with a warning.             |
| PNG, JPEG, GIF, and WebP images referenced by a page            | Supported within limits               | Eligible referenced images are mirrored under the page's `assets/` directory and linked relatively.                                             |
| Oversized, missing, forbidden, failed, or unsafe image metadata | Safe fallback                         | Uses a safe source link or visible `Image unavailable` placeholder and reports the relevant asset or conversion diagnostic.                     |
| SVG and other image media types                                 | Unsupported for mirroring             | The image is not committed as an asset; a safe source link or visible placeholder remains with `ASSET_TYPE_UNSUPPORTED`.                        |
| General non-image attachments                                   | Unsupported                           | Public v1 mirrors only referenced supported inline images. It does not mirror arbitrary attachments.                                            |
| Jira and other dynamic macros                                   | Unsupported                           | Visible child text, safe source link, and/or `[Unsupported content: …]` placeholder with `CONVERSION_UNSUPPORTED_NODE`; no Jira API enrichment. |
| Include and excerpt macros                                      | Unsupported                           | Visible text or a safe source link and a stable placeholder are retained with a warning; referenced content is not expanded.                    |
| Unknown or third-party nodes                                    | Safe fallback                         | Visible text is retained when present, otherwise a source link or stable placeholder is emitted with `CONVERSION_UNSUPPORTED_NODE`.             |
| Malformed ADF that cannot produce safe output                   | Unsupported for that run              | The page reports `CONVERSION_FAILED`; the complete run publishes no ref update.                                                                 |
| Live Doc and legacy-authored ADF                                | Supported according to the rows above | Both authoring origins use the same ADF converter; individual node support and limitations still govern.                                        |

## Image and attachment limits

- Only images actually referenced by an exported page are considered.
- Supported mirrored media types are PNG, JPEG, GIF, and WebP.
- An individual image may be at most 10 MiB.
- All mirrored images in one run may total at most 64 MiB.
- Images, Markdown, and the ownership manifest together count toward the 1,500 generated-file and
  100 MiB generated-byte limits.
- Attachment ID and version participate in change detection; filename alone is not identity.
- Duplicate filenames do not collide because generated asset paths include the attachment ID.
- Missing, unsupported, oversized, or failed images normally degrade the page rather than failing
  it, provided safe valid Markdown can still be produced.

## Evidence basis

This table is bound to the production converter and its current 35-page synthetic regression
corpus. The corpus covers supported, degraded, unsupported, and strict-error cases, including
Live Doc and legacy-authored ADF, links, tables, layouts, macros, images, Unicode and long paths,
and malformed input. It validates current behavior but does not expand the supported set.
