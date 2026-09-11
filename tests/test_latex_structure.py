"""Structural validation of the LaTeX sources.

No LaTeX toolchain exists in this environment (pdflatex, xelatex, lualatex,
tectonic and latexmk are all absent), so ``make pdf`` cannot be executed and is
NOT claimed to pass. These checks are what can be verified without a compiler:
balanced environments and braces, resolvable cross-references, required
structure, and the honesty constraints the audit imposes on the wording.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper" / "paper.tex"
APPENDIX = ROOT / "paper" / "appendix.tex"


def sources():
    assert PAPER.exists() and APPENDIX.exists()
    return {p.name: p.read_text(encoding="utf-8") for p in (PAPER, APPENDIX)}


def strip_comments(text):
    return re.sub(r"(?<!\\)%.*", "", text)


def check_environment_nesting(body):
    """Stack-based check. Returns an error string, or None if well nested.

    A multiset comparison would NOT discriminate: Counter subtraction drops
    non-positive counts, so interleaved or misordered environments pass. This
    walks the tokens in order and requires proper nesting.
    """
    stack = []
    for m in re.finditer(r"\\(begin|end)\{(\w+\*?)\}", strip_comments(body)):
        kind, env = m.group(1), m.group(2)
        if kind == "begin":
            stack.append(env)
        else:
            if not stack:
                return f"\\end{{{env}}} with no matching \\begin"
            top = stack.pop()
            if top != env:
                return f"\\end{{{env}}} closes \\begin{{{top}}}"
    if stack:
        return f"unclosed environments: {stack}"
    return None


def test_environments_balanced():
    for name, body in sources().items():
        err = check_environment_nesting(body)
        assert err is None, f"{name}: {err}"


def test_environment_checker_discriminates():
    """The checker must actually fail on broken input, in all three ways."""
    assert check_environment_nesting(r"\begin{equation}x\end{equation}") is None
    assert check_environment_nesting(r"\begin{equation}x") is not None
    assert check_environment_nesting(r"x\end{equation}") is not None
    assert check_environment_nesting(
        r"\begin{a}\begin{b}\end{a}\end{b}") is not None, "interleaving not caught"


def test_braces_balanced():
    for name, body in sources().items():
        body = strip_comments(body)
        body = body.replace(r"\{", "").replace(r"\}", "")
        assert body.count("{") == body.count("}"), (
            f"{name}: {body.count('{')} open vs {body.count('}')} close braces")


def test_math_delimiters_balanced():
    for name, body in sources().items():
        body = strip_comments(body)
        body = re.sub(r"\\\$", "", body)
        # $$ is not used; count single $ and require an even number
        assert body.count("$") % 2 == 0, f"{name}: odd number of $ delimiters"


def test_labels_and_refs_resolve():
    body = strip_comments("\n".join(sources().values()))
    labels = set(re.findall(r"\\label\{([^}]+)\}", body))
    refs = set(re.findall(r"\\(?:eq)?ref\{([^}]+)\}", body))
    missing = sorted(refs - labels)
    assert not missing, f"unresolved \\ref targets: {missing}"


def test_no_duplicate_labels():
    body = strip_comments("\n".join(sources().values()))
    labels = re.findall(r"\\label\{([^}]+)\}", body)
    dupes = {x for x in labels if labels.count(x) > 1}
    assert not dupes, f"duplicate labels: {sorted(dupes)}"


def test_required_structure_present():
    body = sources()["paper.tex"]
    for needed in [r"\begin{abstract}", r"\section{Introduction}",
                   r"\bibliography{references}", r"\input{appendix}"]:
        assert needed in body, f"missing {needed}"


def test_abstract_states_the_conditional_claim():
    """The audit requires the abstract to say 'conditional on ... Stieltjes'
    AND immediately clarify what 'exact' does not mean."""
    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}",
                  sources()["paper.tex"], re.S)
    assert m, "no abstract"
    a = " ".join(m.group(1).split()).lower()
    assert "conditional on a positive stieltjes representation" in a
    assert "exact" in a and "hypothesis" in a
    assert "do \\emph{not} prove" in a or "do not prove" in a, (
        "abstract must state that the hypothesis is not proved nonperturbatively")


def test_no_overclaiming_language():
    """Forbidden rhetoric: the audit bans grandiose and unsupported framing."""
    body = " ".join(strip_comments("\n".join(sources().values())).split()).lower()
    banned = ["theory of everything", "revolution", "we prove the weak gravity",
              "proof of the weak gravity conjecture", "for the first time",
              "unprecedented", "paradigm shift"]
    hits = [b for b in banned if b in body]
    assert not hits, f"overclaiming language present: {hits}"


def test_nonperturbative_is_never_claimed_unqualified():
    """'nonperturbative' must never appear as a bare claim about H3 holding."""
    body = " ".join(strip_comments("\n".join(sources().values())).split())
    for m in re.finditer(r"[^.]*nonperturbativ[^.]*\.", body, re.I):
        sent = m.group(0).lower()
        qualified = any(w in sent for w in
                        ["not", "does not", "hypothesis", "conditional", "whether"])
        assert qualified, f"unqualified nonperturbative claim: {sent.strip()[:160]}"


def test_high_threat_precedents_are_discussed_not_just_cited():
    """Bachas and the lattice GEVP must appear in prose, not only in a \\cite."""
    body = sources()["paper.tex"]
    assert "Bachas" in body, "Bachas must be discussed by name"
    assert "effective-mass" in body or "effective mass" in body
    assert "lattice" in body.lower()


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-q"]))
