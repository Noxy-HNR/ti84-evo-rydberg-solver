> Legacy standalone edition. Use `../release/` for the current graphical suite, corrected configurations, and ion support. These files are retained for reference.

# TI-84 Evo — Rydberg / Photon Energy Solver

Solve hydrogen-transition problems with a **full worked solution printed
step by step**, the way it would be written out by hand.

Written for the **TI-84 Evo** (Texas Instruments, April 2026) running TI's
adapted CircuitPython build.

## What it does

Given nᵢ = 3 and n_f = 2 (the Balmer H-alpha line):

```
ni=3 > nf=2
-> EMISSION (released)

[1] 1/L = R(1/nf^2 - 1/ni^2)
    R = 1.0970e-02 nm^-1
    1/L = (1.0970e-02)
        x (1/2^2 - 1/3^2)

[2] right-hand side:
    1/2^2 = 0.250000
    1/3^2 = 0.111111
    diff  = 0.138889
    1/L = 1.5236e-03
          nm^-1

[3] L = 1/(1.5236e-03)
    L = 656.34 nm

[4] E = hc/L
    h = 6.6261e-34 J*s
    c = 2.9979e+08 m/s
    L = 656.34 nm
      = 6.5634e-07 m
    E = (6.6261e-34)
        x (2.9979e+08)
        / (6.5634e-07)
[5] E = 3.0266e-19 J

    dE(atom)  = -3.0266e-19
    E(photon) = +3.0266e-19
    photon EMITTED

[6] visible check 380-700:
    L = 656.34 nm
    YES, VISIBLE - red
```

## The three modes

1. **nᵢ, n_f → λ and E** — the worked solution above.
2. **λ or E, plus one quantum number → the other** — prints the rearranged
   equation, the substituted values, the raw non-integer result, and the
   nearest integer on its own line (real transitions require integer n).
3. **kJ/mol → J/photon → λ** — shows the Avogadro division as its own
   explicit step before it feeds the rest of the calculation, then
   optionally continues into a quantum-number solve.

Plus a menu option that prints the constants, for checking against your
exam sheet.

## Constants

| Symbol | Value | Note |
|--------|-------|------|
| R | `1.097e-2 nm^-1` | **nm⁻¹**, not the more common m⁻¹ form |
| h | `6.62607e-34 J*s` | |
| c | `2.99792458e8 m/s` | |
| N_A | `6.02214e23 /mol` | |
| visible | 380–700 nm | |

The Rydberg constant is in **inverse nanometres** to match the value given
on the course exams. Using the m⁻¹ form here would be off by 10⁹.

## Sign conventions

Emission and absorption are handled explicitly. For absorption the
right-hand side goes negative, and the program says so rather than hiding
it:

```
    diff  = -0.138889
    1/L = -1.5236e-03
    (neg => energy absorbed)
[3] L = 1/(-1.5236e-03)
    L = -656.34 nm
    |L| = 656.34 nm
...
    dE(atom)  = +3.0266e-19
    photon ABSORBED
```

Both directions between the same pair of levels give the same |λ|, which is
the physically correct result.

## Error handling

- nᵢ = n_f → `! n_i and n_f must differ - no transition, no photon.`
- Photon above the ionization limit from the known level → reports that no
  bound n exists, rather than taking the square root of a negative number.
- Non-numeric input re-prompts; a blank entry backs out of any prompt.
- n < 1 is rejected as unphysical.

## Calculator constraints

- Imports `math` only (one `sqrt`).
- No f-strings. TI's Python builds have rejected `f"..."` with a
  `SyntaxError`, so all formatting uses `.format()` and concatenation.
- No file I/O; the Python environment is sandboxed.
- Output is capped at 30 columns, one step per line.

## Transfer

Send `RYDBERG.py` to the calculator with **TI Connect Evo**, then run it
from the Python App's File Manager. The filename is 7 characters — TI
program names follow the 8-character variable-name limit.

## Verification

Checked against known hydrogen lines:

| Transition | Computed | Actual |
|------------|----------|--------|
| 3 → 2 (Balmer H-α) | 656.34 nm, 3.0266e-19 J | 656.3 nm, visible red |
| 2 → 1 (Lyman α) | 121.54 nm | 121.6 nm, UV |

All four backward-solve combinations (known nᵢ or n_f × emission or
absorption) recover n = 3.0000 → 3. The mole path: 182.3 kJ/mol →
3.0272e-19 J/photon → 656.21 nm → nᵢ = 3.0004 → 3.
