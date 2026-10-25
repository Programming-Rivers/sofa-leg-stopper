# Laser Cutting Schemas for Sofa Leg Stoppers

The stoppers that keep the sofa at  cenrain distance from the wall.

Two types of stoppers are available in this repo:
- Regular stopper: Keeps a leg at a certain distance from the wall.
- Corner stopper: Keeps a leg at a certain distance from a corner.

## How to use

1. Clone the repo.
2. Adjust the dimensions to your desire
3. Generate the SVG files with this command
   ```bash
   $ bazel run //:main
   ```
   The above commandn will generate the following SVG file:
   - `<PROJECT_DIR>/bazel-bin/sofa_leg_stopper_py.runfiles/_main/leg-stopper.svg`
