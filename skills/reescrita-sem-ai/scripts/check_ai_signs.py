#!/usr/bin/env python3
"""Scan text files for common stylistic signs associated with LLM writing.

This is a heuristic scanner. It does not determine authorship and should be
combined with a manual read of references/signs.md.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

PATTERNS = {
    "1.1": [
        r"\bserve como\b",
        r"\btestemunho\b",
        r"\bpapel (?:crucial|pivotal|vital|significativo|chave)\b",
        r"\blegado duradouro\b",
        r"\bmarca indelével\b",
        r"\bpaisagem em evolução\b",
        r"\bpreparando o terreno\b",
    ],
    "1.2": [
        r"\bcobertura independente\b",
        r"\bmeios de comunicação (?:locais|nacionais)\b",
        r"\bpublicações comerciais\b",
        r"\bpresença ativa nas redes sociais\b",
    ],
    "1.3": [
        r"\b(?:destacando|sublinhando|enfatizando|garantindo|refletindo|simbolizando|cultivando|favorecendo|abrangendo|melhorando)\b",
        r"\bcontribuindo para\b",
        r"\bperceções valiosas\b",
        r"\balinhar com\b",
        r"\bressoar com\b",
    ],
    "1.4": [
        r"\bvibrante\b",
        r"\bric[ao] (?:cultura|herança|história)\b",
        r"\bno coração de\b",
        r"\bde tirar o fôlego\b",
        r"\bde classe mundial\b",
        r"\bstate-of-the-art\b",
        r"\bampla variedade\b",
        r"\bcompromisso com\b",
    ],
    "1.5": [
        r"\bespecialistas (?:dizem|argumentam|afirmam)\b",
        r"\bestudos mostram\b",
        r"\bamplamente considerado\b",
        r"\bobservadores (?:citaram|notaram|afirmam)\b",
        r"\bvárias fontes\b",
    ],
    "1.6": [
        r"\bapesar (?:destes|desses|dos|das|de seus|de suas) desafios\b",
        r"\benfrenta (?:vários )?desafios\b",
    ],
    "1.7": [
        r"\brefere-se a\b",
        r"\bé uma compilação (?:curada )?de\b",
    ],
    "2.1": [
        r"\badicionalmente\b",
        r"\bcrucial\b",
        r"\bmergulhar\b",
        r"\bintricado\b",
        r"\binter-relação\b",
        r"\bpivotal\b",
        r"\btapeçaria\b",
        r"\bfomentar\b",
        r"\bmeticuloso\b",
        r"\bvalioso\b",
    ],
    "2.2": [
        r"\bfunciona como\b",
        r"\bopera como\b",
        r"\brepresenta\b",
        r"\bserve como\b",
    ],
    "2.3": [
        r"\bassociad[oa] com\b",
        r"\bem conexão com\b",
        r"\bconectad[oa] a\b",
    ],
    "2.4": [
        r"\bnão apenas\b.{0,120}\bmas (?:também )?\b",
        r"\bnão é apenas\b",
        r"\bisto não é\b.{0,120}\bé\b",
        r"\bsem\b.{0,80}\bsem\b.{0,80}\bapenas\b",
    ],
    "3.4": [r"—"],
    "3.5": [r"[😀-🙏🌀-🫿]"],
    "4.1": [
        r"\bespero que (?:isto|isso) ajude\b",
        r"\bótima pergunta\b",
        r"\bgostarias que eu\b",
        r"\baqui está\b",
        r"\bnesta secção, discutiremos\b",
    ],
    "4.2": [
        r"\baté (?:à|a) minha última atualização\b",
        r"\bnão amplamente documentad[oa]\b",
        r"\bcom base nas informações disponíveis\b",
        r"\bmantém um perfil baixo\b",
    ],
    "4.3": [
        r"\[Seu Nome\]",
        r"\[Descreva a secção\]",
        r"\bINSERT_URL\b",
        r"\b20\d{2}-XX-XX\b",
    ],
    "5.1": [
        r"\bé importante notar\b",
        r"\bvale a pena notar\b",
        r"\bé importante lembrar\b",
        r"\bé importante considerar\b",
        r"\blembre-se\b",
    ],
    "5.2": [
        r"\bem resumo\b",
        r"\bem conclusão\b",
        r"\bno geral\b",
        r"\bem última análise\b",
    ],
}

COMPILED = {
    sign: [re.compile(pattern, re.IGNORECASE | re.UNICODE) for pattern in patterns]
    for sign, patterns in PATTERNS.items()
}


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def split_sentences(text: str) -> list[str]:
    # Keep the splitter deliberately simple so Markdown and HTML remain readable.
    chunks = re.split(r"(?<=[.!?])\s+|\n{2,}", text)
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def scan(text: str) -> dict[str, list[str]]:
    matches: dict[str, list[str]] = defaultdict(list)
    seen: set[tuple[str, str]] = set()

    for sentence in split_sentences(text):
        for sign, patterns in COMPILED.items():
            if any(pattern.search(sentence) for pattern in patterns):
                key = (sign, sentence)
                if key not in seen:
                    matches[sign].append(sentence)
                    seen.add(key)

    return dict(matches)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan .txt, .md or .html files for common AI-writing signs."
    )
    parser.add_argument("files", nargs="+", help='Files to scan, or "-" for stdin')
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print counts only instead of matched sentences",
    )
    args = parser.parse_args()

    total = 0

    for filename in args.files:
        try:
            text = read_text(filename)
        except OSError as exc:
            print(f"{filename}: {exc}", file=sys.stderr)
            return 2

        results = scan(text)
        count = sum(len(items) for items in results.values())
        total += count

        print(f"{filename}: {count} hit(s)")

        if args.summary:
            for sign in sorted(results):
                print(f"  {sign}: {len(results[sign])}")
            continue

        for sign in sorted(results):
            for sentence in results[sign]:
                print(f"  [{sign}] {sentence}")

    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
