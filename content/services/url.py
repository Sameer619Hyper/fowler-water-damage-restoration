from pathlib import Path
import re

folder = Path(".")
mapping_file = folder / "a.txt"

def parse_mapping_line(line):
    line = line.strip()
    if not line or line.startswith("#"):
        return None

    m = re.match(r'^(\/[^:]+\/):(https?://[^:]+):(<iframe.*</iframe>)$', line)
    if not m:
        return None

    slug, short_url, iframe = m.groups()
    return slug.strip(), short_url.strip(), iframe.strip()

mapping = {}
bad_lines = []

for i, line in enumerate(mapping_file.read_text(encoding="utf-8").splitlines(), 1):
    parsed = parse_mapping_line(line)
    if parsed:
        slug, short_url, iframe = parsed
        mapping[slug] = {
            "short_url": short_url,
            "iframe": iframe,
        }
    elif line.strip():
        bad_lines.append((i, line))

if bad_lines:
    print("Unparsed lines in a.txt:")
    for n, line in bad_lines:
        print(f"  line {n}: {line}")
    print()

md_files = list(folder.glob("*.md"))
updated = 0
skipped = []

def replace_service_area_block(content, short_url, iframe):
    lines = content.splitlines()
    out = []

    in_service_area = False
    service_indent = None

    for line in lines:
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        # Enter service_area block
        if not in_service_area and re.match(r'^\s*service_area:\s*$', line):
            in_service_area = True
            service_indent = indent
            out.append(line)
            continue

        # Exit service_area block when indentation returns to same or less
        if in_service_area and stripped and indent <= service_indent:
            in_service_area = False
            service_indent = None

        if in_service_area:
            if re.match(r'^\s*map_embed_url:\s*', line):
                out.append('  map_embed_url: \'' + iframe + '\'')
                continue
            elif re.match(r'^\s*directions_url:\s*', line):
                out.append(f'  directions_url: "{short_url}"')
                continue
            elif re.match(r'^\s*full_map_url:\s*', line):
                out.append(f'  full_map_url: "{short_url}"')
                continue

        out.append(line)

    return "\n".join(out) + ("\n" if content.endswith("\n") else "")

for md_file in md_files:
    content = md_file.read_text(encoding="utf-8")

    slug_match = re.search(r'^\s*slug:\s*"([^"]+)"', content, re.MULTILINE)
    url_match = re.search(r'^\s*url:\s*"([^"]+)"', content, re.MULTILINE)

    page_path = None
    if slug_match:
        page_path = slug_match.group(1).strip()
    elif url_match:
        page_path = url_match.group(1).strip()

    if not page_path or page_path not in mapping:
        skipped.append(md_file.name)
        continue

    short_url = mapping[page_path]["short_url"]
    iframe = mapping[page_path]["iframe"]

    new_content = replace_service_area_block(content, short_url, iframe)

    if new_content != content:
        backup = md_file.with_suffix(md_file.suffix + ".bak")
        backup.write_text(content, encoding="utf-8")
        md_file.write_text(new_content, encoding="utf-8")
        updated += 1

print(f"Updated {updated} files.")
if skipped:
    print("\nSkipped:")
    for name in skipped:
        print(" -", name)