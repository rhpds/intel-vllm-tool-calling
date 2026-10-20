# Enable AI Tool Calling on OpenShift

## Delivery ownership

Migrate the existing Tool Calling guided lab into Publishing House. Learners connect to a platform-managed tool-capable model, implement the tool-call protocol, build a Python dispatch loop and test multi-tool behavior. Standalone CPU serving remains in rhpds/vllm-tool-calling. PH generates AgnosticV and owns RHDP onboarding; Dallas is the dev test environment. Tracking: GPTEINFRA-17784 and INTEL-47.

PH owns intake, reviews, Env Setup, generated AgnosticV and onboarding. Existing catalog PRs are historical proposals for reference; they are not a parallel onboarding route. Dallas OCP 4.18.16 is a development test environment. The proposed published target is OCP 4.22, subject to PH infrastructure acceptance.

## Learner path

1. Module 1: Tool Calling Fundamentals (10 min).
2. Module 2: Connect to a Tool-Calling Model (15 min).
3. Module 3: Anatomy of a Tool Call (20 min).
4. Module 4: Build the Tool Calling Loop (20 min).
5. Module 5: Build a Multi-Tool Application (15 min).
6. Module 6: Advanced Patterns (10 min).
7. Module 7: Evaluate CPU Inference for Tool Calling (5 min).
8. Module 8: Conclusion (5 min).

## Infrastructure and credential boundary

One assigned tenant namespace and tenant-scoped model access. No learner GPU or local model server is provisioned in the guided profile. Max 25 concurrent learners is a capacity proposal requiring validation, not a tested result. Preserve namespace isolation, short-lived key creation/revocation and workload-owned cleanup.

## Acceptance and evidence

Validate deployed images and terminal dependencies, then real model access and the full learner workflow. Record source/image revisions, failure behavior, tenant isolation and cleanup. CPU placement requires serving-team evidence. Remaining RCARS overlap review, model allocation, capacity and author acceptance are explicit intake gates.

Tracking: RHDPCD-2147; GPTEINFRA-17784 / INTEL-47.
