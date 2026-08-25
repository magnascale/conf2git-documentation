# Conf2Git customer documentation

This public repository hosts the customer documentation for **Conf2Git – Markdown Sync for
Confluence**.

- [Read the published documentation](https://magnascale.github.io/conf2git-documentation/)
- [Visit Magnascale](https://magnascale.com/)
- [Contact support](https://magnascale.com/contact-us/)

The site is built with MkDocs and deployed to GitHub Pages whenever `main` changes. Customer-guide
content is mirrored from the canonical product documentation so its permissions, limits,
diagnostics, and recovery guidance stay aligned with the released application.

## Local preview

With Python 3.13 available:

```shell
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m mkdocs serve
```

In PowerShell, activate the environment with `.venv\Scripts\Activate.ps1` instead of the
`source` command.

Run a release-equivalent local build with:

```shell
python -m mkdocs build --strict
```

Please report documentation corrections through [Magnascale
support](https://magnascale.com/contact-us/). Never include page or Markdown bodies, images,
private keys, OAuth secrets, JWTs, tokens, authorization headers, provider responses, Marketplace
payloads, or other customer content or credentials in a report.
