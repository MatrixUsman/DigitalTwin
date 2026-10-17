# Your virtual robot laboratory

**This step is already implemented and runs entirely on the computer. You do not need a robot, sensors, a laboratory or special equipment.** I will handle the code, execution and checks. Here, “physical simulation” means that equations calculate how a robot would move and respond to its controller.

Open the [animated robot replay](../output/virtual_lab_demo/virtual_robot_lab.gif) or the [still overview](../output/virtual_lab_demo/virtual_lab_overview.png). These show saved synthetic observations from the completed pilot. They do not create another experiment or add new evidence.

## What is inside the simulation?

| Part | What the software does |
|---|---|
| Robot | Calculates the angles and velocities of a horizontal arm with two joints, including inertia, coupling between joints and friction. |
| Controller | Compares desired and actual motion, then applies limited virtual motor torque to follow the program. It responds throughout each simulation step. |
| Sensors | Produces virtual joint-angle and velocity readings with Gaussian measurement noise. |
| Reference observer | Predicts motion using the approved program and nominal robot parameters. Its mass/friction values differ from the two simulated plants. |
| Legitimate changes | Changes both the approved program and the commands received by the virtual controller. |
| Unauthorized changes | Changes controller commands after the protected planner; the monitor still has the approved program. |
| Detectors | Process the same saved time sequence, predict or score unusual behavior, and issue alarms or uncertainty. |
| Evaluator | Uses separately retained true states and intervention labels to measure detection, normal alarms and recovery. Those truths are not detector inputs. |

The existing simulator has eight scenarios: unchanged motion, legitimate position change, legitimate slowdown, a brief unauthorized position change, sustained unauthorized position change, held command, unauthorized slowdown, and unauthorized change during missing command context. Two mass/friction variants and three noise seeds have already been evaluated. All generated observations are labelled **synthetic**.

The simulation chain is:

```text
Approved program ────────────────> command-aware detectors
       │                              ↑
       └─> optional command change    │ noisy sensor readings
                    │                 │
                    v                 │
             virtual controller ─> virtual robot motion

True state / intervention schedule ─> evaluator only
```

## Reading the animation

The dark arm is the simulated robot. The dashed blue arm is the independent prediction driven by the approved program. The orange dot is the endpoint implied by noisy joint-angle readings; noise is small and has not been exaggerated for visibility.

The four panels show unchanged motion, a legitimate program change, an unauthorized command change, and an unauthorized change with missing trusted context. They use the same light-plant parameters and noise seed 17. Changes start at 6 s; sustained changes end at 10 s. The context gap ends at 7.2 s. Labels above each panel describe evaluator-known scenarios for explanation; detectors do not see those labels.

The legitimate and unauthorized position-change panels have **identical actual motion and sensor readings**. The approved program differs. This illustrates why trustworthy context matters: motion alone cannot tell us whether that particular change was authorized. The animation samples the original 50 Hz recording every ten observations and plays at 5 fps, approximately real simulation time. It is an illustrative replay of existing outcomes.

## Fair information access

The context-matched comparison includes ARX, the following observer, its rolling mean/CUSUM variants, command reference, fused errors and hysteresis variants. Each receives the same four noisy joint-state channels, approved position/velocity commands and command-validity flag. None gets the true mass, noise-free state, corrupted executed command or attack labels.

Persistence and AR deliberately omit commands and serve as **information ablations**. They are labelled separately: a gain over them cannot be attributed solely to a new twin. ARX is the ordinary predictor with matching command access. Every method has the same episode boundaries, eligible evaluation points and normal-only fitting/calibration rules. Existing paper-derived IMU models remain in their separate input track.

## What has already been validated?

The completed pilot has 18 normal training episodes, 18 normal calibration episodes and 48 evaluation episodes across eleven methods. Its 26 passing synthetic tests and 53,004 verification checks cover numerical physics, energy/geometry identities, prediction timing, fit isolation, thresholds, scores, recovery state machines and saved artifacts. These are the existing v0.5 checks, not new benchmark results from this demonstration.

The rendering helper additionally compares its calculated endpoints with 4,000 saved endpoint coordinates, verifies the identical-motion pair, and checks the old artifact identities before and after rendering. The [full scientific report](../research_cycles/recovery_v0.5/RESULTS.md) retains the original numerical-test failure and the corrected summary-export failure.

The physics model is an idealized two-joint arm. Its numerical validation supports simulation-based experiments; correspondence to a particular physical robot has not been measured. Our writing will identify simulation findings as simulation findings.

## Optional inspection command

Everything above is already generated. If you want to inspect the saved package, run this from the repository root; it checks file identities and prints a plain JSON summary without training or generating a new scenario:

```sh
manufacturing/.venv-reproduction-v02/bin/python manufacturing/simulation/inspect_virtual_lab.py
```

The rendering command used for this demonstration was:

```sh
manufacturing/.venv-plots-v03/bin/python manufacturing/simulation/render_virtual_lab.py
```

It refuses to overwrite the existing demonstration. Code and original configuration are in [recovery_v0.5](../research_cycles/recovery_v0.5/README.md). `local/virtual_lab_demo/render_receipt.json` records the exact source hashes, versions, frame count and measured rendering cost. No installation, hardware setup or manual experiment is required from you. Future scientific runs will use a separately frozen configuration; this demonstration leaves the original experiment intact.
