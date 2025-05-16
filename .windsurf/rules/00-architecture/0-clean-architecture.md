---
trigger: model_decision
description: APPLY Clean Architecture principles WHEN organizing code in backend
globs: **/*.php
---

# Layers Overview

- Split into: **Domain**, **Infrastucture**, **Application**, **Presentation**
- Follow Dependency Inversion: `Infrascture -> Application -> Domain <- Application <- Presentation`
- Domain and Application layers remains framework-agnostic

# Layer Structure

- **Domain Layer**:
  - Contains business models, enums, value objects
  - Place business logic and entities here.
  - Define domain services for complex logic.

- **Application Layer**:
  - Implement use cases as domain objects orchestrators.
  - Services are signle-responsability commands : `LoginUserService` instead of `UserService`.
  - Validate input at boundaries.

- **Infrastructure Layer**:
  - Implement domain repository interfaces.
  - Isolate external systems (DB, APIs, files, random, system time).
  - Keep infrastructure out of business logic.

- **Presentation Layer**:
  - Handle API requests and responses through Controllers.
  - Centralize error handling and validation
  - Delegate business logic to Application layer.

# Critical Rules

- Keep outer layers from depending on inner layers.
- Define repository interfaces in the domain layer.
- Do not mix business with infrastructure logic.