"""One causal replay of all eleven frozen deterministic variants; no fit API."""
from __future__ import annotations

from dataclasses import asdict
import math

from .contract import ContractError
from .controls import ARDetector, ARReference, TemplateDetector, TemplateReference
from .observer import EvidenceScale, ObserverConfig, PhaseObserver, prepare_observation
from .observer_scores import score_observer_proposal
from .velocity import VelocityDetector, VelocityReference

METHODS = ("O-R", "O-RC", "O-C", "O-K", "O-L", "O-Rv", "O-Follow", "O-Free", "V-Z", "T-32", "AR-4")


class FrozenRoster:
    def __init__(self, models):
        self.models = models
        model = models["observer"]
        self.reference = TemplateReference.from_dict(model["template"])
        self.config = ObserverConfig.from_dict(model["observer_config"])
        self.scales = EvidenceScale(model["training_eligible_count"],
            model["normalizers"]["residual"]["mean"], model["normalizers"]["correction_js"]["mean"])
        self.observers = {mode: PhaseObserver(self.reference, self.config, mode=mode)
                          for mode in ("synchronized", "unconstrained", "free_running")}
        value = models["velocity"]["reference"]
        velocity = VelocityReference(value["n"], *(tuple(value[k]) for k in ("mean", "variance", "sigma")))
        self.controls = {"V-Z": VelocityDetector(velocity),
            "T-32": TemplateDetector(TemplateReference.from_dict(models["template"]["reference"])),
            "AR-4": ARDetector(ARReference.from_dict(models["ar"]["reference"]))}
        if self.controls["T-32"].reference != self.reference:
            raise ContractError("Observer and selected template reference differ")
        self.fitted_before = self.fitted_state()

    def fitted_state(self):
        return {"observer_reference": self.reference.to_dict(), "config": self.config.to_dict(),
                "scales": asdict(self.scales),
                "controls": {k: d.reference.to_dict() for k, d in self.controls.items()}}

    def step(self, observation, eligible):
        """Propose -> emit every score -> commit; no coordinates or labels here."""
        prepared = prepare_observation(self.reference, observation)
        proposals = {mode: observer.propose(prepared) for mode, observer in self.observers.items()}
        if observation.dt is None:
            for detector in self.controls.values():
                detector.reset()
        scores = {}
        if eligible:
            if any(not p.ready for p in proposals.values()):
                raise ContractError("Observer not ready on common support")
            scores.update(score_observer_proposal(proposals["synchronized"], prepared, self.config, self.scales).to_dict())
            scores["O-Follow"] = proposals["unconstrained"].residual / self.scales.mean_residual
            scores["O-Free"] = proposals["free_running"].residual / self.scales.mean_residual
            scores.update({name: detector.score(observation) for name, detector in self.controls.items()})
            if tuple(scores) != METHODS or any(type(v) not in (int, float) or not math.isfinite(v) or v < 0 for v in scores.values()):
                raise ContractError("Missing/nonfinite/negative roster score")
        for mode, observer in self.observers.items():
            observer.commit(proposals[mode])
        for detector in self.controls.values():
            detector.update(observation)
        return scores

    def verify_unchanged(self):
        if self.fitted_state() != self.fitted_before:
            raise ContractError("Frozen fitted parameters changed during replay")
