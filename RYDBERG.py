# RYDBERG.py -- Rydberg / Photon Energy Solver
# Target : TI-84 Evo (TI CircuitPython build)
# Imports: math only
# Notes  : no f-strings (TI Python builds reject them), no file I/O.
#
# Every calculation prints a full worked solution, one step per
# line, the way it would be written out by hand.

import math

R_B = 1.097e-2          # nm^-1 -- the constant given on the exam
H = 6.62607e-34         # J*s
C = 2.99792458e8        # m/s
NA = 6.02214e23         # photons per mol
HC = H * C              # J*m
WIDTH = 30

VIS_LO = 380.0
VIS_HI = 700.0


# ---------- formatting ----------

def sci(x):
    return "{:.4e}".format(x)


def f2(x):
    return "{:.2f}".format(x)


def f4(x):
    return "{:.4f}".format(x)


def f6(x):
    return "{:.6f}".format(x)


def rule():
    print("-" * WIDTH)


# ---------- input helpers ----------

def ask_float(prompt):
    """Blank input cancels and returns None."""
    while True:
        s = input(prompt).strip()
        if s == "":
            print("  (cancelled)")
            return None
        try:
            return float(s)
        except ValueError:
            print("  ! Number please (blank=back)")


def ask_n(prompt):
    """A quantum number: whole, >= 1. Blank cancels."""
    while True:
        s = input(prompt).strip()
        if s == "":
            print("  (cancelled)")
            return None
        try:
            v = int(s)
        except ValueError:
            print("  ! Whole number (blank=back)")
            continue
        if v < 1:
            print("  ! n must be >= 1")
            continue
        return v


def ask_choice(prompt, valid):
    s = input(prompt).strip()
    if s in valid:
        return s
    print("! Pick one of: " + ", ".join(valid))
    return None


# ---------- shared steps ----------

def region(lam):
    if lam < VIS_LO:
        return "UV (< 380 nm)"
    if lam > VIS_HI:
        return "IR (> 700 nm)"
    if lam < 450.0:
        c = "violet"
    elif lam < 495.0:
        c = "blue"
    elif lam < 570.0:
        c = "green"
    elif lam < 590.0:
        c = "yellow"
    elif lam < 620.0:
        c = "orange"
    else:
        c = "red"
    return "VISIBLE - " + c


def step_visible(lam, tag):
    print(tag + " visible check 380-700:")
    print("    L = " + f2(lam) + " nm")
    r = region(lam)
    if r[0] == "V":
        print("    YES, " + r)
    else:
        print("    NO, " + r)


def step_energy_from_lambda(lam_nm, tag_a, tag_b):
    """E = hc/L, shown with values substituted in."""
    lam_m = lam_nm * 1e-9
    e = HC / lam_m
    print(tag_a + " E = hc/L")
    print("    h = " + sci(H) + " J*s")
    print("    c = " + sci(C) + " m/s")
    print("    L = " + f2(lam_nm) + " nm")
    print("      = " + sci(lam_m) + " m")
    print("    E = (" + sci(H) + ")")
    print("        x (" + sci(C) + ")")
    print("        / (" + sci(lam_m) + ")")
    print(tag_b + " E = " + sci(e) + " J")
    return e


def step_lambda_from_energy(e, tag):
    """L = hc/E, shown with values substituted in."""
    lam_m = HC / e
    lam_nm = lam_m * 1e9
    print(tag + " L = hc/E")
    print("    hc = " + sci(HC) + " J*m")
    print("    L = (" + sci(HC) + ")")
    print("        / (" + sci(e) + ")")
    print("      = " + sci(lam_m) + " m")
    print("    L = " + f2(lam_nm) + " nm")
    return lam_nm


# ---------- mode 1: ni, nf -> L and E ----------

def solve_lambda_from_n(ni, nf):
    inv_f = 1.0 / (nf * nf)
    inv_i = 1.0 / (ni * ni)
    diff = inv_f - inv_i
    inv_lam = R_B * diff                # signed, nm^-1
    emission = ni > nf

    rule()
    if emission:
        print("ni={} > nf={}".format(ni, nf))
        print("-> EMISSION (released)")
    else:
        print("ni={} < nf={}".format(ni, nf))
        print("-> ABSORPTION (absorbed)")
    print("")

    print("[1] 1/L = R(1/nf^2 - 1/ni^2)")
    print("    R = " + sci(R_B) + " nm^-1")
    print("    1/L = (" + sci(R_B) + ")")
    print("        x (1/{}^2 - 1/{}^2)".format(nf, ni))
    print("")

    print("[2] right-hand side:")
    print("    1/{}^2 = ".format(nf) + f6(inv_f))
    print("    1/{}^2 = ".format(ni) + f6(inv_i))
    print("    diff  = " + f6(diff))
    print("    1/L = " + sci(inv_lam))
    print("          nm^-1")
    if not emission:
        print("    (neg => energy absorbed)")
    print("")

    lam = 1.0 / inv_lam
    lam_abs = abs(lam)
    print("[3] L = 1/(" + sci(inv_lam) + ")")
    print("    L = " + f2(lam) + " nm")
    if not emission:
        print("    |L| = " + f2(lam_abs) + " nm")
    print("")

    e = step_energy_from_lambda(lam_abs, "[4]", "[5]")
    print("")
    if emission:
        print("    dE(atom)  = -" + sci(e))
        print("    E(photon) = +" + sci(e))
        print("    photon EMITTED")
    else:
        print("    dE(atom)  = +" + sci(e))
        print("    E(photon) =  " + sci(e))
        print("    photon ABSORBED")
    print("")

    step_visible(lam_abs, "[6]")
    rule()
    return lam_abs, e


def mode_forward():
    ni = ask_n("n_i (initial): ")
    if ni is None:
        return
    nf = ask_n("n_f (final)  : ")
    if nf is None:
        return
    if ni == nf:
        print("! n_i and n_f must differ -")
        print("  no transition, no photon.")
        return
    solve_lambda_from_n(ni, nf)


# ---------- mode 2: L or E + one n -> the other n ----------

def get_lambda():
    """Ask for L directly, or for E and convert. -> nm or None."""
    print("What do you have?")
    print("  1) wavelength L (nm)")
    print("  2) photon energy E (J)")
    c = ask_choice("Choice: ", ("1", "2"))
    if c is None:
        return None
    if c == "1":
        lam = ask_float("L (nm): ")
        if lam is None:
            return None
        if lam <= 0:
            print("! L must be > 0.")
            return None
        return lam
    e = ask_float("E (J): ")
    if e is None:
        return None
    if e <= 0:
        print("! E must be > 0.")
        return None
    rule()
    lam = step_lambda_from_energy(abs(e), "[0]")
    print("")
    return lam


def solve_for_n(lam, known_is_nf, known, emission):
    """Find the missing quantum number.

    The same level pair underlies both cases, so work in terms
    of lower/upper and map back:
      emission   -> ni is upper, nf is lower
      absorption -> ni is lower, nf is upper
    """
    k = 1.0 / (R_B * lam)               # = |1/n_lo^2 - 1/n_hi^2|
    inv_known = 1.0 / (known * known)

    if emission:
        unknown_is_upper = known_is_nf
    else:
        unknown_is_upper = not known_is_nf

    if known_is_nf:
        want = "n_i"
        have = "n_f"
    else:
        want = "n_f"
        have = "n_i"

    print("[1] 1/L = R(1/nf^2 - 1/ni^2)")
    print("")
    print("[2] 1/(R*L):")
    print("    R*L = (" + sci(R_B) + ")")
    print("        x " + f2(lam))
    print("        = " + f6(R_B * lam))
    print("    1/(R*L) = " + f6(k))
    print("")

    print("[3] rearrange for " + want + ":")
    if unknown_is_upper:
        print("    (" + want + " is the upper level)")
        print("    1/hi^2 = 1/lo^2 - 1/(R*L)")
        val = inv_known - k
    else:
        print("    (" + want + " is the lower level)")
        print("    1/lo^2 = 1/hi^2 + 1/(R*L)")
        val = inv_known + k
    print("")

    print("[4] substitute " + have + "={}:".format(known))
    print("    1/{}^2 = ".format(known) + f6(inv_known))
    if unknown_is_upper:
        print("    1/" + want + "^2 = " + f6(inv_known))
        print("             - " + f6(k))
    else:
        print("    1/" + want + "^2 = " + f6(inv_known))
        print("             + " + f6(k))
    print("             = " + f6(val))
    print("")

    if val <= 0:
        print("! No bound level here: that")
        print("  photon meets or exceeds the")
        print("  ionization limit from n={}.".format(known))
        print("  Check L, E, or the type.")
        rule()
        return

    raw = 1.0 / math.sqrt(val)
    print("[5] " + want + " = 1/sqrt(" + f6(val) + ")")
    print("    " + want + " (raw) = " + f4(raw))
    print("")

    nearest = int(raw + 0.5)
    print("[6] " + want + " = {}".format(nearest))
    print("    (nearest whole number)")
    if nearest < 1:
        print("! n < 1 is not physical.")
    elif nearest == known:
        print("! Same as " + have + " - check the")
        print("  emission/absorption choice.")
    rule()


def mode_backward():
    lam = get_lambda()
    if lam is None:
        return
    print("Which n do you KNOW?")
    print("  1) n_f (final)")
    print("  2) n_i (initial)")
    c = ask_choice("Choice: ", ("1", "2"))
    if c is None:
        return
    known_is_nf = (c == "1")
    if known_is_nf:
        known = ask_n("n_f = ")
    else:
        known = ask_n("n_i = ")
    if known is None:
        return
    print("Transition type?")
    print("  1) emission (ni > nf)")
    print("  2) absorption (ni < nf)")
    t = ask_choice("Choice: ", ("1", "2"))
    if t is None:
        return
    emission = (t == "1")

    rule()
    if emission:
        print("EMISSION (energy released)")
    else:
        print("ABSORPTION (energy absorbed)")
    print("L = " + f2(lam) + " nm")
    print("")
    solve_for_n(lam, known_is_nf, known, emission)


# ---------- mode 3: kJ/mol ----------

def mode_kjmol():
    ek = ask_float("E (kJ/mol): ")
    if ek is None:
        return
    if ek == 0:
        print("! E cannot be 0.")
        return
    mag = abs(ek)

    rule()
    print("[0] kJ/mol -> J/photon")
    print("    E = " + f2(mag) + " kJ/mol")
    j_per_mol = mag * 1000.0
    print("    x 1000 J/kJ")
    print("      = " + sci(j_per_mol) + " J/mol")
    print("    NA = " + sci(NA) + " /mol")
    e = j_per_mol / NA
    print("    E = (" + sci(j_per_mol) + ")")
    print("        / (" + sci(NA) + ")")
    print("    E = " + sci(e) + " J/photon")
    print("")

    lam = step_lambda_from_energy(e, "[1]")
    print("")
    step_visible(lam, "[2]")
    rule()

    print("Solve for a quantum number")
    print("with this photon? (y/n)")
    if input("> ").strip().lower() not in ("y", "yes"):
        return
    print("Which n do you KNOW?")
    print("  1) n_f (final)")
    print("  2) n_i (initial)")
    c = ask_choice("Choice: ", ("1", "2"))
    if c is None:
        return
    known_is_nf = (c == "1")
    if known_is_nf:
        known = ask_n("n_f = ")
    else:
        known = ask_n("n_i = ")
    if known is None:
        return
    print("Transition type?")
    print("  1) emission (ni > nf)")
    print("  2) absorption (ni < nf)")
    t = ask_choice("Choice: ", ("1", "2"))
    if t is None:
        return
    rule()
    solve_for_n(lam, known_is_nf, known, t == "1")


# ---------- constants ----------

def show_constants():
    rule()
    print("R  = " + sci(R_B) + " nm^-1")
    print("h  = " + sci(H) + " J*s")
    print("c  = " + sci(C) + " m/s")
    print("hc = " + sci(HC) + " J*m")
    print("NA = " + sci(NA) + " /mol")
    print("visible: 380-700 nm")
    rule()


# ---------- menu ----------

def main():
    print("RYDBERG / PHOTON SOLVER")
    while True:
        print("")
        print("1) ni,nf -> L and E")
        print("2) L or E + one n -> other n")
        print("3) kJ/mol -> J/photon -> L")
        print("4) Show constants")
        print("5) Quit")
        c = input("Choice: ").strip()
        if c == "1":
            mode_forward()
        elif c == "2":
            mode_backward()
        elif c == "3":
            mode_kjmol()
        elif c == "4":
            show_constants()
        elif c == "5":
            print("Bye.")
            return
        else:
            print("! Pick 1-5.")


main()
