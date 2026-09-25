import os
import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """One-time transfer of the committed media_seed/ files onto whatever
    MEDIA_ROOT actually resolves to at runtime (e.g. a Railway Volume) --
    used because a shell `cp` in the Procfile depends on the working
    directory matching BASE_DIR, which isn't guaranteed across
    platforms/builders. Never overwrites an existing file, so it's safe
    to run on every deploy: only fills in what's missing.
    """

    help = "Copy home/../media_seed/* into MEDIA_ROOT, skipping files that already exist there."

    def handle(self, *args, **options):
        seed_dir = Path(settings.BASE_DIR) / "media_seed"
        media_root = Path(settings.MEDIA_ROOT)

        if not seed_dir.is_dir():
            self.stdout.write(self.style.WARNING(f"No seed directory at {seed_dir}, skipping."))
            return

        # One-time diagnostic for the "PermissionError creating a
        # subdirectory under a mounted Volume" issue -- there's no shell
        # access to the container, so this is the only way to see the
        # mount's actual ownership/mode.
        if hasattr(os, "getuid") and media_root.exists():
            st = media_root.stat()
            self.stdout.write(
                f"seed_media: running as uid={os.getuid()} gid={os.getgid()}; "
                f"media_root owned by uid={st.st_uid} gid={st.st_gid} mode={oct(st.st_mode)}"
            )

        copied = 0
        skipped = 0
        failed = 0
        for source in seed_dir.rglob("*"):
            if source.is_dir():
                continue
            relative = source.relative_to(seed_dir)
            destination = media_root / relative
            if destination.exists():
                skipped += 1
                continue
            try:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
                copied += 1
            except OSError as exc:
                # Never let a media-seeding hiccup (e.g. a volume mount
                # that doesn't grant this user permission to create new
                # subdirectories) block app startup -- this step is a
                # nice-to-have, and the app must still boot without it.
                failed += 1
                self.stderr.write(
                    self.style.WARNING(f"seed_media: could not write {destination}: {exc}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"seed_media: copied {copied} file(s), skipped {skipped} already-present file(s), "
                f"failed {failed} file(s). seed_dir={seed_dir} media_root={media_root}"
            )
        )
