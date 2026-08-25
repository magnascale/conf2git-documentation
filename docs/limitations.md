# Backup and disaster-recovery limitations

Use this exact operating assumption:

> Conf2Git is a one-way Confluence to GitHub Markdown mirror. It is not a complete backup or a
> general disaster-recovery system.

In particular:

- It is not two-way synchronization and does not publish GitHub changes to Confluence.
- It is not real-time synchronization. Manual runs and eligible daily opportunities use queued,
  bounded work; the daily interval has no exact wall-clock promise.
- It does not preserve every Confluence feature, behavior, layout, macro, attachment type,
  permission model, version-history detail, comment, annotation, or provider datum.
- Generated Markdown and images are subject to the documented conversion behavior and the exact
  page, file, image, image-byte, and generated-byte limits.
- Unsupported content is retained only through the current safe text, source-link, placeholder, or
  diagnostic behavior described in the [conversion support table](conversion-support.md).
- GitHub history and generated output do not make an unowned repository file managed. Ownership
  remains bounded by a valid manifest and app-published provenance.
- Mapping removal and app uninstall do not remove the generated repository mirror.
- Rebuild is a bounded re-materialization of managed output from current Confluence source. It
  preserves unowned files and is not a point-in-time restore system.
- Manifest repair is limited to restoring one canonical ownership manifest from independently
  verified historical provenance. It is not general repository recovery.
- Conf2Git does not replace Confluence-native or GitHub-native export, backup, retention, legal
  hold, availability, or disaster-recovery controls.

Use provider-native continuity controls for requirements that need complete source history,
provider configuration, permissions, unsupported content, or point-in-time restoration.
