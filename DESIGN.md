# Conf2Git documentation design

The documentation extends Magnascale’s established forest, cream, and lime identity, matching
the reading-focused [Service Quality Review portal](https://magnascale.github.io/sqrjsm-public-docs/).
It is a presentation-only change: customer-guide Markdown, headings, anchors, and route paths
remain unchanged.

## Shared foundation

- MkDocs Material 9.7.7 with native search, task tabs, section navigation, on-page contents,
  previous/next links, return-to-top control, and mobile drawer.
- Locally served variable Manrope (200–800), `font-display: swap`, and the bundled OFL licence.
- Forest `#153f34` navigation, off-white `#fffefa` reading surface, ink `#253c34`,
  green `#245e47` links, and lime `#d7ef90` selection/navigation accents.
- Balanced headings, an approximately 73-character body measure, generous line spacing,
  underlined content links, and restrained table surfaces rather than decorative cards.
- The original Conf2Git product logo and public product wording are retained. SQR-specific
  release notices and product assets are not copied.

## Conf2Git adaptations

Light, dark, and system appearance remain available. Dark mode uses a deep green reading
surface, pale ink/headings, lime links, and scheme-aware table/code colors. A three-pixel
focus outline uses green on the light reading surface and lime on forest navigation and
dark surfaces. Navigation groups existing files by task without changing their URLs.

Tables keep Material’s horizontal overflow container. Inline diagnostic codes may wrap;
preformatted blocks keep native scrolling. Small screens use native Material navigation and
a smaller headline. No custom interaction JavaScript, external font requests, analytics, or
background repository-metadata requests are introduced.

## Maintenance and acceptance

Run the strict build and `scripts/check_site.py` before review. The checker validates all guide
routes, local URLs/assets/anchors, and search coverage. For a migration, pass
`--baseline-site <previous-build-directory>` to compare generated routes and heading anchors.
Review desktop/mobile layouts, keyboard focus, search open/clear/close, navigation/back behavior,
tables, and light/dark/system persistence in a browser.

The export manifest is historical provenance and is intentionally unchanged. A legacy product
export can overwrite shell files; inspect its diff and preserve the theme when updating guides.
