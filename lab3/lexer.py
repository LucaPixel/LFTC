"""Simple FilterMini lexer. Run: python lexer.py [source_file]"""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent


def add_symbol(word, buckets, symbols):
    bucket = buckets[sum(ord(char) for char in word) % len(buckets)]
    for saved_word, position in bucket:
        if saved_word == word:
            return position
    position = len(symbols)
    bucket.append((word, position))
    symbols.append(word)
    return position


def analyze(source, tokens):
    pif, symbols, errors = [], [], []
    buckets = [[] for _ in range(101)]
    pattern = r"[ \t\r]+|-?[0-9][A-Za-z0-9_.]*|[A-Za-z_][A-Za-z0-9_.]*|\.[A-Za-z0-9_.]*|."
    source = source.replace("\r\n", "\n").replace("\r", "\n")
    for line_number, line in enumerate(source.split("\n"), 1):
        for match in re.finditer(pattern, line):
            word = match.group()
            if re.fullmatch(r"[ \t\r]+", word):
                continue
            if word in tokens and word not in ("IDENTIFIER", "INTEGER_CONSTANT"):
                pif.append((tokens[word], -1))
            elif re.fullmatch(r"[a-z][a-z0-9]*", word):
                position = add_symbol(word, buckets, symbols)
                pif.append((tokens["IDENTIFIER"], position))
            elif re.fullmatch(r"-?[0-9]+", word):
                position = add_symbol(word, buckets, symbols)
                pif.append((tokens["INTEGER_CONSTANT"], position))
            else:
                errors.append(f"Line {line_number}, column {match.start() + 1}: invalid token {word!r}")
    return pif, symbols, errors


def main():
    source_file = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "examples/program1.fm"
    try:
        tokens = json.loads((ROOT / "tokens.json").read_text(encoding="utf-8"))
        source = source_file.read_text(encoding="utf-8-sig")
        pif, symbols, errors = analyze(source, tokens)
        output = ROOT / "output" / source_file.stem
        output.mkdir(parents=True, exist_ok=True)
        (output / "pif.txt").write_text(
            "token_code st_position\n" + "".join(f"{code} {position}\n" for code, position in pif),
            encoding="utf-8")
        (output / "st.txt").write_text(
            "position symbol\n" + "".join(f"{i} {word}\n" for i, word in enumerate(symbols)),
            encoding="utf-8")
        (output / "errors.txt").write_text(
            "\n".join(errors) + "\n" if errors else "No lexical errors.\n", encoding="utf-8")
        print(f"{len(pif)} tokens, {len(symbols)} symbols, {len(errors)} lexical errors")
        print(f"Output: {output}")
        return 1 if errors else 0
    except (OSError, ValueError, KeyError) as error:
        print(f"Error: {error}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
