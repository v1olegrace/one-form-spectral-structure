"""Canonical book library, with verified identifiers and legal access routes.

Every DOI/ISBN below was resolved against Crossref in this session. Nothing is
typed from memory: an entry that could not be resolved is marked
PENDING_VERIFICATION rather than filled in with a plausible number.

ACCESS POLICY. These are copyrighted monographs. What is stored here is
bibliographic metadata plus a pointer to the chapter that must be read and a
legitimate route to obtain it. No protected full text is downloaded or stored.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scilit import db as sdb  # noqa: E402

# (title, authors, edition, year, isbn, doi, publisher, chapters, cluster,
#  priority, reason)
BOOKS = [
    ("The Moment Problem", "Konrad Schmudgen", "1st", 2017, "9783319645452",
     "10.1007/978-3-319-64546-9", "Springer",
     "Ch. 3 (moment problem on an interval); Ch. 9-10 (truncated Hamburger and "
     "Stieltjes problems, Hankel matrices); Ch. 16-17 (determinacy, Carleman)",
     "B", "NOW",
     "THE reference for every moment-problem statement in the paper. Needed to "
     "cite the truncated Stieltjes problem correctly and to state exactly which "
     "Hankel positivity conditions are necessary vs sufficient. Also settles "
     "determinacy language: Carleman gives determinacy ONLY, never support."),

    ("Jacobi Matrices and the Moment Problem", "Aad Dijksma; et al.", "1st", 2023,
     "9783031463860", "10.1007/978-3-031-46387-7", "Springer Nature",
     "Chapters on Jacobi operators and the spectrum; extreme eigenvalues",
     "B", "NOW",
     "Directly the machinery of Theorem E. The map from the Hankel pencil to a "
     "Jacobi operator, and the convergence of its extreme Ritz values to the "
     "endpoint of the support, is the exact theorem the paper needs to cite "
     "rather than re-derive."),

    ("The Classical Moment Problem and Some Related Questions in Analysis",
     "N. I. Akhiezer", "SIAM reissue", 2020, "9781611976380",
     "10.1137/1.9781611976397", "SIAM",
     "Ch. 1-2 (Hamburger/Stieltjes), Ch. 3 (Nevanlinna parametrization)",
     "B", "NEXT",
     "The classical source. Needed for the canonical form of the truncated "
     "problem and for the extremal-measure characterization underlying the "
     "sharpness of the Hankel bound."),

    ("Bernstein Functions: Theory and Applications",
     "Rene L. Schilling; Renming Song; Zoran Vondracek", "2nd", 2012,
     "9783110252293", "10.1515/9783110269338", "De Gruyter",
     "Ch. 1 (complete monotonicity), Ch. 3 (Bernstein/Stieltjes functions), "
     "Ch. 7 (Stieltjes and complete Bernstein classes)",
     "A", "NOW",
     "The precise class definitions the paper depends on. Theorem B's statement "
     "must distinguish completely monotone from Stieltjes from complete "
     "Bernstein; these are DIFFERENT classes and the paper's counterexamples "
     "separating positivity, support and UV integrability live exactly here. "
     "A 3rd edition (2026, DOI 10.1515/9783111295121) exists."),

    ("Laplace Transform (PMS-6)", "David Vernon Widder", "1st", 1942,
     "9781400876457", "10.1515/9781400876457", "Princeton University Press",
     "Ch. II (Stieltjes-Laplace transform), Ch. IV (Bernstein-Widder "
     "representation theorem), Ch. V (inversion and uniqueness)",
     "A", "NOW",
     "The Bernstein-Widder theorem is the backbone of Theorem A and B. Cite the "
     "theorem number from here, not a secondary restatement."),

    ("The Problem of Moments", "J. A. Shohat; J. D. Tamarkin", "1st", 1943,
     "9780821815014", "10.1090/surv/001", "American Mathematical Society",
     "Ch. I-II (existence and determinacy), Ch. III (Hankel forms)",
     "B", "NEXT",
     "Historical primary source for the Hankel-determinant criteria; useful for "
     "the HISTORICAL_LINEAGE report and for priority statements."),

    ("Orthogonal Polynomials: Computation and Approximation", "Walter Gautschi",
     "1st", 2004, "9780198506720", "10.1093/oso/9780198506720.001.0001",
     "Oxford University Press",
     "Ch. 1.4 (Gauss quadrature), Ch. 2 (computing recurrence coefficients, "
     "conditioning of the moment map)",
     "D", "NOW",
     "The conditioning results matter directly: Gautschi quantifies how badly "
     "the map from moments to recurrence coefficients is conditioned, which is "
     "the mechanism behind the paper's finite-precision no-go (Theorem H) and "
     "behind the observed need for ~86 digits in the wide-dynamic-range model."),

    ("Pade Approximants", "George A. Baker; Peter Graves-Morris", "2nd", 1996,
     "9780511530074", "10.1017/cbo9780511530074", "Cambridge University Press",
     "Ch. 5 (Stieltjes series and Pade), Ch. 17 (convergence for Stieltjes "
     "functions, bounds from Pade)",
     "D", "NEXT",
     "Establishes that Pade approximants to a Stieltjes series give two-sided "
     "bounds converging to the function, and that poles/zeros interlace on the "
     "cut. This is the classical ancestor of threshold extraction and must be "
     "cited when claiming the Hankel hierarchy is not new mathematics."),

    ("Moments, Positive Polynomials and Their Applications", "Jean-Bernard Lasserre",
     "1st", 2009, "9781848164451", "10.1142/p665", "Imperial College Press",
     "Ch. 3 (moment-SOS hierarchy), Ch. 4 (localizing matrices and support "
     "constraints)",
     "B", "NEXT",
     "Determines whether the paper's Hankel hierarchy is the one-dimensional "
     "specialization of the general moment-SOS hierarchy. If it is, that is a "
     "required citation and a further downgrade of Theorem E's novelty."),

    ("Asymptotics and Special Functions", "Frank W. J. Olver", "AKP reissue", 1997,
     "9780429064616", "10.1201/9781439864548", "A K Peters/CRC Press",
     "Ch. 3 (Watson's lemma and Laplace's method), Ch. 4 (error bounds for "
     "asymptotic expansions)",
     "C", "NOW",
     "Watson's lemma with RIGOROUS ERROR BOUNDS is what turns the edge law "
     "(Theorem D) from an asymptotic statement into a usable inequality. The "
     "paper currently states the expansion; Olver supplies the remainder bound."),

    ("Quantum Fields on a Lattice", "Istvan Montvay; Gernot Munster", "1st", 1994,
     "9780521404327", "10.1017/cbo9780511470783", "Cambridge University Press",
     "Ch. 3 (transfer matrix and reflection positivity), Ch. 7 (static potential "
     "and Wilson loops)",
     "E", "NOW",
     "The source for reflection positivity of the transfer matrix, which is the "
     "strongest available support for H3 at the nonperturbative level, and for "
     "the standard definition of the static potential from Wilson loops."),

    ("An Introduction to Orthogonal Polynomials", "Theodore S. Chihara", "1st",
     1978, "PENDING_VERIFICATION", "PENDING_VERIFICATION", "Gordon and Breach",
     "Ch. I-II (moment functionals, quasi-definite case), Ch. IV (chain "
     "sequences and the true interval of orthogonality)",
     "B", "NEXT",
     "NOT RESOLVED against Crossref in this session: no identifier is recorded "
     "rather than a guessed one. Chihara's chain sequences give the sharp "
     "condition for the true interval of orthogonality, which is the natural "
     "home of the signed-measure gate (a quasi-definite but not positive-"
     "definite moment functional is exactly what the gate must reject)."),
]


def load(con):
    n = 0
    for (title, authors, edition, year, isbn, doi, publisher, chapters,
         cluster, priority, reason) in BOOKS:
        verified = isbn != "PENDING_VERIFICATION"
        con.execute(
            "INSERT OR REPLACE INTO books (title, authors, edition, year, isbn,"
            " publisher, relevant_chapters, access_status, access_route, reason,"
            " cluster, priority) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (title, authors, edition, year,
             isbn if verified else None, publisher, chapters,
             "PAYWALLED_METADATA_ONLY" if verified else "PENDING_VERIFICATION",
             f"https://doi.org/{doi}" if verified else
             "identifier unresolved; obtain via institutional library catalogue",
             reason, cluster, priority))
        n += 1
    con.commit()
    return n


if __name__ == "__main__":
    con = sdb.connect()
    print(f"books loaded: {load(con)}")
