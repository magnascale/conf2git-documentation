# Conf2Git customer documentation

This public repository hosts the customer documentation for **Conf2Git – Markdown Sync for
Confluence**.

- [Read the published documentation](https://magnascale.github.io/conf2git-documentation/)
- [Visit Magnascale](https://magnascale.com/)
- [Contact support](https://magnascale.com/contact-us/)

The site uses Magnascale’s shared, reading-focused MkDocs Material styling and deployed to GitHub Pages whenever `main` changes. Customer-guide
content is mirrored from the canonical product documentation so its permissions, limits,
diagnostics, and recovery guidance stay aligned with the released application.

## Local preview

With Python 3.13 available:

```shell
python -m venv .venv
source .venv/bin/activate
python -m pip install --require-hashes -r requirements.txt
python -m mkdocs serve
```

In PowerShell, activate the environment with `.venv\Scripts\Activate.ps1` instead of the
`source` command.

Run a release-equivalent local build with:

```shell
python -m mkdocs build --strict
python scripts/check_site.py
```

Please report documentation corrections through [Magnascale
support](https://magnascale.com/contact-us/). Never include page or Markdown bodies, images,
private keys, OAuth secrets, JWTs, tokens, authorization headers, provider responses, Marketplace
payloads, or other customer content or credentials in a report.

## Theme maintenance

The visual system follows the [Service Quality Review documentation](https://magnascale.github.io/sqrjsm-public-docs/):
forest navigation, cream reading surfaces, lime accents, and locally served Manrope. It retains
Conf2Git’s logo, guide URLs, search, and light/dark/system appearance controls. See [DESIGN.md](DESIGN.md).
The font’s Open Font License is bundled alongside it. No third-party font or analytics requests
are added; the repository link also avoids background GitHub metadata requests.

Customer-guide Markdown remains canonical product documentation. The historical
`.conf2git-documentation-export.json` is retained as provenance, not regenerated for theme work.
The legacy exporter also owns shell files such as `mkdocs.yml`, the stylesheet, and requirements;
review any future export diff carefully so it does not overwrite the maintained theme. Updating
that exporter is a separate change in the product repository.

Theme dependencies are hash-locked. To update them, edit `requirements.in`, regenerate with
`uv pip compile requirements.in --generate-hashes --output-file requirements.txt`, and rerun
both validation commands. Check desktop/mobile navigation, search, tables, and all appearance
modes after theme upgrades.

Changes should be reviewed in a pull request. Merging to `main` publishes the site; a local
preview or draft pull request does not authorize a production deployment.
