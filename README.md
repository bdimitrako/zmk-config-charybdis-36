# zmk-config-charybdis-36

ZMK firmware for a Charybdis-family split keyboard: 3 rows x 6 columns per side
+ 3 thumb keys per side (42 keys total), trackball (PMW3610) mounted under the
right thumb. Bluetooth device name: **Nano36**.

Base config forked from [Vzhao-L/zmk-for-charybdis](https://github.com/Vzhao-L/zmk-for-charybdis)
branch `Charybdis-mini36-Mod` (the only Mini36-family branch with the trackball
wired in — its sibling `charybdis-RL-Mini36-MOD` has no pointing device).

Changes from the vendor source:
- `ZMK_KEYBOARD_NAME` set to `Nano36` (was `Charybdis`)
- `zmk-pmw3610-driver` pinned to an exact commit SHA instead of floating `main`
- RGB underglow (SPI3/WS2812) disabled — board has the header but no LEDs installed
- Rotary encoders left enabled as shipped (both halves) pending physical confirmation

Sibling project: [zmk-config-charybdis-nano](https://github.com/bdimitrako/zmk-config-charybdis-nano)
(the 35-key InnerBall board, trackball under the palm instead of the thumb).

## Status
- [x] Repo scaffolded from vendor branch
- [ ] Keymap ported from Temper_zmk (36-key source -> 42-key target, 6 spare thumb slots)
- [ ] Flashed and verified on hardware
