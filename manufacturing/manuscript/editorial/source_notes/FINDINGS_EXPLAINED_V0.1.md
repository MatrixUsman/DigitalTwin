# What the completed manufacturing study means

17 October 2026. Evidence: [complete final report](FINAL_CAMPAIGN_REPORT_V0.1.md) and [frozen aggregate results](../experiments/FINAL_CAMPAIGN_V0.1_SUMMARY.json). This explanation adds no experiment, model choice or test-driven redesign.

## The question we actually answered

We compared a motion observer's prediction-error score, O-R, with that same score plus a measure of how much the new measurement changed its phase estimate, O-RC. The predictions, measurements and evolving state were identical. Both methods already used expected progression around the motion cycle. We tested the extra **correction-score term**, not whether progression itself works.

The reference and thresholds stayed fixed. Updating the observer's estimate of its current phase is different from learning new model parameters. Our manufacturing experiment therefore did not test the water project's proposed adaptation gate or contamination-resistance claim.

## The numerical result in plain terms

O-RC marked 3,043 of 345,602 schedule-positive observations as alarms: **0.8805% recall**. O-R marked 2,921: **0.8452% recall**. The added correction term gained 122 positive observations, removed 32 false positives within the mixed slice, and removed 27 alarms in the separate normal slice. F1 increased from 0.016603 to 0.017292. That is a small favorable difference with poor absolute detection. F1 is not classification accuracy.

O-RC alarmed on 2,132 of 214,473 protected-normal observations, approximately 0.9941%. Those alarm points formed **554 separate contiguous alarm episodes during about 2.98 eligible hours**, or about 186 episodes/hour. An episode is a run of adjacent alarm points, not an independently verified incident. Selecting the 99th percentile of calibration scores does not control how often alarm episodes begin or guarantee the future alarm fraction.

## Why “eight out of eight events” does not settle the question

Every event lasted over 43,000 recorded positive observations. A single alarm anywhere inside it counts as an event-overlap hit. O-RC produced a fresh alarm in all eight, but alarmed on less than 1% of positive observations overall. Frequent normal alarms mean an event hit alone cannot establish reliable recognition of the scheduled intervention.

There were no pre-existing alarms at event starts in this particular campaign, so overlap and fresh-onset outcomes coincided. The definitions remain different. We did not mark a sustained alarm that began before an event as a new detection.

O-R missed event 5; O-RC first alarmed there after 9.20 seconds. Among the seven events both hit, O-RC was never earlier: five delays were identical, two were later. Its lower detected-only median uses a different event set and does not prove faster matched detection. Misses remain in the table as misses.

Point recall alone is also not a complete operational objective: some systems need only one actionable alarm per incident. Our result remains weak because event hits must be assessed with normal episode burden, reliable onset semantics and the intended response policy. This study did not define or validate an operator response policy.

## What the ordinary controls tell us

The ordinary AR-4 predictor had higher F1 and average precision than O-RC, with slightly fewer normal alarm points but many more normal episodes. The periodic template had the highest F1 and recall, but higher point false alarms. The direct velocity control and several observer residual variants gave similar results. No predeclared utility collapses these trade-offs into one winner.

Average precision values were close to the mixed slice's 50.63% positive prevalence. We cannot present an AP around 0.50 as strong merely because it sounds much larger than F1 around 0.017: these quantities answer different questions. The study's schedule prevalence is not an estimate of real-world attack frequency.

We measured total scoring and evaluation cost, but not isolated method latency. We cannot say the extra correction evidence was free, faster, or worth a measured processing penalty. The resource-limited execution succeeded; a deployed security system was not evaluated.

## What can go into this paper

Supported: a complete within-recording score comparison, a small correction-score effect, weak absolute detection, all simple-control trade-offs, and the difference between event hits and useful monitoring evidence. The manuscript can explain the methods precisely and preserve negative results.

Unsupported: a new general digital twin, first use of phase or surprise, broad detector superiority, authenticated monitoring, fault/attack discrimination, cross-robot cybersecurity, physical protection, or leading-journal readiness. One acquisition and eight dependent intervals cannot establish those claims. Software tests and seeds do not create more robots or independent data.

## The next scientific decision

The results are frozen and the final holdout is exposed. We can understand and document them. Any new feature, model, smoothing/persistence rule, threshold or preferred variant motivated by them is exploratory. It may be useful work, but it needs a new declared protocol and genuinely reserved independent evidence for a new confirmatory claim.

The [post-exposure independent-evidence plan](POST_EXPOSURE_INDEPENDENT_EVIDENCE_PLAN_V0.1.md) gives the next bounded route. First audit a source for a clearly stated question; do not download a different robot file and automatically call it another cyberattack benchmark.

## Researcher comprehension check

These questions remain for the authors to answer in their own words. This document does not certify understanding.

1. Why does 8/8 event recall coexist with 0.88% point recall?
2. Why are 0.994% normal alarm points and 186 episodes/hour both necessary?
3. Which variable changed in the primary pair, and which variables stayed identical?
4. Why does a second robot's fault dataset not establish attack-intent recognition?
5. Which observations could be used for exploratory design now, and what must remain unseen in a new confirmatory study?
6. What work did each author personally perform and verify?
