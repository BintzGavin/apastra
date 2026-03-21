# Moderation Decision Records Policy

## 1. Overview
This policy defines the handling and structure of moderation decision records within the registry.

## 2. Immutability and Storage
The registry must maintain all moderation decision records as append-only, immutable artifacts. Once a record is created, it cannot be altered or deleted.

## 3. Record Generation
Every moderation action (e.g., approval, rejection, takedown) MUST generate a corresponding moderation decision record detailing the action, the rationale, and the human checkpoint.

## 4. Record Contents
Each moderation decision record must detail:
- The specific moderation action taken.
- The rationale or justification for the action.
- The human checkpoint (e.g., the identity of the moderator or admin) that authorized the decision.
