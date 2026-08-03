# zmk-config-charybdis-36

ZMK firmware for a Charybdis-family split keyboard: 3 rows x 5 columns per side
+ 3 thumb keys per side (36 keys total), trackball (PMW3610) mounted under the
right thumb, no rotary encoders, no RGB underglow installed. Bluetooth device
name: **Nano36**.

Base config forked from [Vzhao-L/zmk-for-charybdis](https://github.com/Vzhao-L/zmk-for-charybdis)
branch `charybdis-Nano35-MOD` — despite the branch's internal `Nano35_layout`
label, its physical layout is actually 36 keys (5 cols x 3 rows + 3 thumbs per
side), matching this board exactly. (The sibling branch `Charybdis-mini36-Mod`
looked promising at first but is a different, larger 42-key PCB variant —
ruled out after comparing physical layouts key-by-key.)

Changes from the vendor source:
- `ZMK_KEYBOARD_NAME` set to `Nano36` (was hardcoded `"V&Z-Nano35"` in
  `config/charybdis.conf`, which is what Studio was showing before this repo existed)
- `zmk-pmw3610-driver` pinned to an exact commit SHA instead of floating `main`
- RGB underglow disabled (`CONFIG_ZMK_RGB_UNDERGLOW=n`, `&spi3` disabled in both
  overlays) — board has the header but no LEDs installed
- Rotary encoders disabled (`CONFIG_EC11=n`, both `left_encoder`/`right_encoder`
  devicetree nodes explicitly disabled) — confirmed no physical encoders

Sibling project: [zmk-config-charybdis-nano](https://github.com/bdimitrako/zmk-config-charybdis-nano)
(the 35-key InnerBall board, trackball under the palm instead of the thumb).

## Status
- [x] Repo scaffolded from the correct vendor branch, RGB/encoder Kconfig cleaned up
- [ ] CI build verified green
- [ ] Keymap ported from Temper_zmk (36-key source -> 36-key target, thumb cluster
      re-sited around the relocated trackball)
- [ ] Flashed and verified on hardware
- [ ] Trackball sensor orientation/CPI re-tuned for thumb position (currently
      inherited as-is from the vendor's palm-mounted defaults)
