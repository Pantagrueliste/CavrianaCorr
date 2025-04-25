#!/usr/bin/env python3
from pathlib import Path
import argparse, logging, sys, shutil, xml.etree.ElementTree as ET
from typing import Optional

TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}
ET.register_namespace("", TEI_NS["tei"])   # preserve default ns on write


def locate_para(root: ET.Element) -> Optional[ET.Element]:
    """Return the first <p> under <encodingDesc>/<projectDesc>, regardless of namespace."""
    for xp in (
        ".//tei:encodingDesc/tei:projectDesc/tei:p",
        ".//encodingDesc/projectDesc/p",
    ):
        hit = root.find(xp, TEI_NS)
        if hit is not None:
            return hit
    return None


def patch(path: Path, old: str, new: str, *, dry: bool, bak: str = ".bak") -> bool:
    try:
        tree = ET.parse(path)
    except (ET.ParseError, OSError) as exc:
        logging.warning("Skip %s (%s)", path, exc)
        return False

    para = locate_para(tree.getroot())
    if para is None or old not in (para.text or ""):
        return False

    logging.info("%s -> will update", path)
    if dry:
        return True

    try:
        shutil.copy2(path, path.with_suffix(path.suffix + bak))
        para.text = new
        tree.write(path, encoding="utf-8", xml_declaration=True)
        return True
    except OSError as exc:
        logging.error("Cannot write %s (%s)", path, exc)
        return False


def run(root: Path, old: str, new: str, *, dry: bool) -> int:
    return sum(
        patch(p, old, new, dry=dry)
        for p in root.rglob("*.xml")
    )


def cli(argv: Optional[list[str]] = None) -> None:
    ap = argparse.ArgumentParser(
        description="Replace <encodingDesc>/<projectDesc>/<p> text in TEI XML."
    )
    ap.add_argument("old_text", help="Substring to look for in the paragraph")
    ap.add_argument("new_text", help="Replacement paragraph text")
    ap.add_argument("directory", nargs="?", default=Path.cwd(), type=Path,
                    help="Root directory (default: current)")
    ap.add_argument("--dry-run", action="store_true", help="Show changes only")
    ap.add_argument("-v", "--verbose", action="count", default=0,
                    help="Increase verbosity")
    args = ap.parse_args(argv)

    lvl = logging.WARNING - 10 * min(args.verbose, 2)
    logging.basicConfig(format="%(levelname)s: %(message)s", level=lvl)

    if not args.directory.is_dir():
        sys.exit(f"{args.directory} is not a directory (pwd: {Path.cwd()})")

    try:
        n = run(args.directory, args.old_text, args.new_text, dry=args.dry_run)
    except KeyboardInterrupt:
        sys.exit("\nInterrupted")

    print(f"{n} file(s) {'would be ' if args.dry_run else ''}updated.")


if __name__ == "__main__":
    cli()