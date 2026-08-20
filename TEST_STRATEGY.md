# Test Strategy

## Objective

Provide fast, repeatable confidence in the highest-value behaviour of the demo application while keeping the suite small and maintainable.

## Quality risks

| Risk | Impact | Automated coverage |
|---|---|---|
| Application unavailable | High | API health smoke test |
| Valid users cannot sign in | High | UI smoke test |
| Invalid authentication is accepted | High | Negative UI test |
| Inventory API returns incorrect structure/data | High | API regression tests |
| UI does not reflect inventory data | Medium/High | UI inventory test |
| Search/filter produces incorrect results | Medium | UI regression tests |
| Missing API resource returns unsafe/unhelpful response | Medium | Negative API test |
| Invalid create request is accepted | Medium | API validation test |

## Test layers

### API

API tests are preferred for business/data validation where browser interaction adds little value. They are faster, easier to diagnose, and less brittle than UI tests.

### UI

UI automation is reserved for workflows where browser behaviour itself matters: authentication, rendering, navigation, and user interaction.

### Manual / exploratory

The following would remain primarily exploratory in a real product:

- visual quality;
- accessibility review beyond automated checks;
- unusual browser/device interactions;
- new or rapidly changing workflows;
- subjective usability;
- unexpected combinations not yet represented in regression coverage.

## Smoke vs regression

**Smoke tests** answer: _Is this build fundamentally testable?_

They cover:
- service health;
- successful login;
- initial inventory load.

**Regression tests** cover broader behaviour and negative scenarios.

This separation allows a CI pipeline to fail quickly before spending time on deeper validation.

## Automation selection

A test is a strong automation candidate when it is:

- repeatable;
- deterministic;
- important enough to run frequently;
- stable enough that maintenance cost is justified;
- objectively pass/fail.

I would avoid automating a workflow simply because it can be automated. The expected value should exceed the maintenance cost.

## Release confidence

A passing suite is evidence, not proof, that a release is safe.

A release decision should also consider:

- scope of change;
- untested areas;
- open defects and severity;
- environment health;
- dependency changes;
- production observability;
- rollback/recovery options.

Automation supports engineering judgement rather than replacing it.
