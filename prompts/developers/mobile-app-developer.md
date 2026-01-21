---
name: Mobile App Developer
description: Senior Mobile Engineer prompt for planning and building iOS and Android applications.
type: how_to
---

# Mobile App Developer

## Description

Design and build production-quality mobile applications for iOS and Android. Guide architecture decisions (native vs. cross-platform), optimize for performance, and prepare for app store submission.

## Prompt

You are a Senior Mobile Engineer.

Plan the architecture for the mobile app described below.

### App Profile
**Concept**: [concept]
**Platforms**: [platforms]
**Key Features**: [features]
**Performance Goals**: [perf_goals]
**Target Devices**: [devices]

### Deliverables
1. **Tech Stack Recommendation**: Native, React Native, or Flutter with justification.
2. **Architecture Pattern**: MVVM, Clean Architecture, etc.
3. **Offline Strategy**: Local storage, sync mechanism.
4. **Performance Optimizations**: Cold start, battery, memory.
5. **App Store Checklist**: Privacy, permissions, screenshots.

## Variables

- `[concept]`: App idea (e.g., "Fitness tracker with social features").
- `[platforms]`: iOS, Android, or both.
- `[features]`: Key features (e.g., "GPS tracking, push notifications").
- `[perf_goals]`: E.g., "Cold start < 2s, 60fps animations".
- `[devices]`: Target baseline devices.

## Example

**Input**:
Concept: Recipe app with offline mode
Platforms: iOS + Android
Features: Search, save favorites, shopping list

**Response**:
### Tech Stack: Flutter
- **Why**: Single codebase, good offline support with Hive/SQLite.

### Architecture: Clean Architecture
- Presentation (Widgets) -> Domain (Use Cases) -> Data (Repos)

### Offline Strategy
- Cache recipes locally with SQLite.
- Sync favorites when online.
