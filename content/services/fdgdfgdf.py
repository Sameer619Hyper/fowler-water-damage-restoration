from pathlib import Path

# Change these paths if needed
MD_FOLDER = "."          # folder containing md files
ZIP_FILE = "zips.txt"    # txt file with City:Zip


def load_zipcodes(zip_file):
    city_to_zip = {}

    with open(zip_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue

            city, zipcode = line.split(":", 1)
            city = city.strip().lower()
            zipcode = zipcode.strip()

            if city and zipcode:
                city_to_zip[city] = zipcode

    return city_to_zip


def update_md_file(md_path, city_to_zip):
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    city_name = None
    slug_index = None
    zipcode_exists = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith("city_name:"):
            # Example: city_name: Dinuba, CA
            value = stripped.split(":", 1)[1].strip()
            city_name = value.split(",")[0].strip().lower()

        if stripped.startswith("slug:"):
            slug_index = i

        if stripped.startswith("zipcode:"):
            zipcode_exists = True

    if zipcode_exists or city_name is None or slug_index is None:
        return False

    zipcode = city_to_zip.get(city_name)
    if not zipcode:
        print(f"Skipping {md_path} - no zipcode found for city '{city_name}'")
        return False

    lines.insert(slug_index + 1, f"zipcode: "{zipcode}\n")

    with open(md_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Updated {md_path} -> zipcode: "{zipcode}")
    return True


def main():
    city_to_zip = load_zipcodes(ZIP_FILE)
    md_files = Path(MD_FOLDER).rglob("*.md")

    updated_count = 0
    for md_file in md_files:
        if update_md_file(md_file, city_to_zip):
            updated_count += 1

    print(f"\nDone. Updated {updated_count} markdown file(s).")


if __name__ == "__main__":
    main()