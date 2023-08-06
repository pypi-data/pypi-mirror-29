"""
Hearthstone Strings file

File format: TSV. Lines starting with `#` are ignored.
Key is always `TAG`
"""
import csv

import hearthstone_data


_cache = {}


def load(fp):
	reader = csv.DictReader(filter(lambda row: not row.startswith("#"), fp), delimiter="\t")
	stripped_rows = [{k: v for k, v in row.items() if v} for row in reader]
	return {stripped_row.pop("TAG"): stripped_row for stripped_row in stripped_rows}


def load_globalstrings(locale="enUS"):
	path = hearthstone_data.get_strings_file(locale, filename="GLOBAL.txt")
	if path not in _cache:
		with open(path, "r") as f:
			_cache[path] = load(f)

	return _cache[path]


if __name__ == "__main__":
	import json
	import sys

	for path in sys.argv[1:]:
		with open(path, "r") as f:
			print(json.dumps(load(f)))
