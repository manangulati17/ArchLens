ArchLens — Project Overview

ArchLens is a GenAI-powered system design explainer and evaluator.

The system takes a textual description of a software architecture
(e.g. system design interview answers or real-world design docs)
and produces a structured, senior-level evaluation focusing on:
	•	architecture decomposition
	•	data and control flow
	•	scalability bottlenecks
	•	reliability and failure modes
	•	“what breaks first” analysis
	•	cost vs scale trade-offs
	•	rough infrastructure cost estimation

⸻

Design Philosophy

ArchLens does not aim to generate a “perfect system design”.
Instead, it behaves like a senior engineer reviewing an existing design,
highlighting trade-offs, assumptions, and risks.

The project prioritizes:
	•	reasoning over generation
	•	structure over free-form text
	•	clarity of assumptions over false precision

⸻

Architecture Decisions

This document tracks major architectural decisions made during
the development of ArchLens, along with their rationale.

⸻

Decision 1: Monolith vs Microservices

Decision: Modular Monolith

Alternatives Considered:
	•	Microservices
	•	Single-file application

Why This Decision:
	•	Single developer and single core use case
	•	No need for independent deployment or scaling
	•	Microservices would add operational complexity without benefits
	•	A modular monolith provides clean separation of concerns while
remaining easy to evolve

Future Consideration:
	•	The ai module could be extracted into a separate service if
independent scaling or reuse becomes necessary

⸻

Decision 2: Introduce Retrieval-Augmented Generation (RAG)

Decision: Include RAG as a core component of ArchLens.

Why This Decision:
	•	Cost estimation and latency reasoning require factual grounding
	•	Architecture trade-offs benefit from known patterns and benchmarks
	•	Prevents hallucinated infrastructure claims
	•	Enables company-specific constraints in future iterations

Scope of RAG:
	•	Cloud pricing references (directional, not exact)
	•	Latency and infrastructure baselines
	•	Known architecture patterns and trade-offs
	•	Optional company-specific constraints

Design Choice:
	•	RAG is performed before prompt construction
	•	Retrieved context is explicitly provided to the LLM
	•	LLM remains responsible for reasoning, not fact lookup

Future Evolution:
	•	Move from static curated sources to dynamic or external sources
	•	Add freshness checks and versioning

⸻

Backend Architecture

The backend follows a layered, modular-monolith architecture designed
to support controlled GenAI reasoning while remaining simple to deploy
and evolve.

⸻

High-Level Layers
	1.	API Layer
	•	Handles HTTP requests and responses
	•	Performs input validation
	•	Contains no business or GenAI logic
	2.	Application Layer
	•	Orchestrates use cases and reasoning flow
	•	Coordinates RAG, prompt construction, and LLM execution
	•	Assembles and validates final outputs
	3.	Domain Layer
	•	Pydantic models defining input and output contracts
	•	Acts as the schema boundary for LLM outputs
	•	Represents the “AI contract” enforced across the system
	4.	GenAI Layer
	•	Prompt construction and reasoning instructions
	•	LLM client interaction
	•	Isolated from API and application logic
	5.	RAG Layer
	•	Retrieves authoritative reference context
	•	Supplies factual grounding for cost, latency, and pattern analysis
	•	Remains separate from reasoning logic

⸻

Backend Module Layout

The backend is implemented with the following strict boundaries:
	•	api/ handles HTTP transport only
	•	services/ orchestrates use cases and reasoning flow
	•	rag/ retrieves authoritative reference context
	•	ai/ contains GenAI prompt logic and LLM interaction
	•	models/ defines input/output contracts enforced across the system
	•	core/ manages configuration and environment concerns

Dependencies are strictly one-directional to avoid tight coupling
and to enable future extraction of components if needed.

⸻

Key Principle

Only one module (ai/llm_client.py) is allowed to directly interact
with the LLM provider. This ensures:
	•	easy model replacement
	•	controlled AI behavior
	•	minimal blast radius for AI-related changes

⸻

GenAI Reasoning Model

ArchLens treats prompt engineering and LLM interaction as
first-class architectural components rather than implementation details.

The system is designed so that:
	•	reasoning logic is explicit and inspectable
	•	LLM behavior is constrained by contracts
	•	model interaction is isolated and replaceable

This prevents the GenAI layer from becoming opaque or tightly coupled
to the rest of the backend.

⸻

AI Contracts (Schema-First Design)

ArchLens follows a schema-first GenAI design.

Instead of allowing the LLM to return free-form text, the system enforces
a strict output contract using Pydantic models. This ensures:
	•	deterministic response structure
	•	predictable frontend rendering
	•	early detection of hallucinated or malformed outputs
	•	clear separation between reasoning and presentation

⸻

Output Contract

The LLM is required to return a structured response that includes:
	•	architecture breakdown and assumptions
	•	data and control flow
	•	scalability analysis and bottlenecks
	•	reliability analysis with explicit “what breaks first”
	•	cost vs scale trade-off table
	•	infrastructure cost estimates at multiple scales
	•	global assumptions
	•	overall summary

If the LLM output does not conform to this schema, it is rejected.

This contract defines the boundary of AI freedom:
	•	reasoning remains flexible
	•	structure remains fixed

⸻

Input Contract

The input schema defines what context ArchLens is allowed to use.

It includes:
	•	mandatory system design text
	•	optional evaluation context (scale, system type, constraints)
	•	explicit RAG configuration
	•	optional focus areas (scalability, reliability, cost, security)

This keeps the system minimal by default while allowing controlled
depth and grounding when additional context is provided.

⸻

Prompt System (ai/prompt.py)

Prompts in ArchLens are treated as structured programs rather than
static strings.

The prompt system is responsible for:
	•	defining the senior-engineer review persona
	•	enforcing reasoning-first analysis
	•	explicitly requesting assumptions and failure modes
	•	constraining the LLM to a fixed output structure

The prompt layer does not:
	•	call the LLM
	•	handle retries
	•	parse or validate outputs
	•	contain orchestration logic

⸻

Prompt Structure

Each evaluation prompt consists of two parts:
	1.	System Prompt
	•	Defines role, behavior, and global reasoning rules
	•	Enforces:
	•	trade-off driven analysis
	•	explicit assumptions
	•	avoidance of false precision
	•	mandatory failure-first reasoning
	2.	User Prompt
	•	Contains the system design text
	•	Includes optional evaluation context
	•	Injects RAG-provided reference material when enabled
	•	Explicitly specifies output structure requirements

This separation improves compliance and keeps persona definition
stable across requests.

⸻

Prompt Construction Flow

The prompt system exposes pure functions that:
	•	accept structured input objects
	•	return a prompt payload containing:
	•	system message text
	•	user message text

This payload acts as an internal intermediate representation
and is not directly tied to any specific LLM provider.

⸻

Retrieval-Augmented Generation (RAG) — v1 Design

RAG in ArchLens is used strictly as a grounding mechanism, not a
decision-making engine.

⸻

Purpose of RAG

RAG supplies factual context for:
	•	cloud pricing references (directional)
	•	latency and infrastructure baselines
	•	known architecture patterns and trade-offs

This reduces hallucinations and improves reasoning quality without
outsourcing architectural judgment to retrieved documents.

⸻

RAG v1 Implementation

The initial RAG implementation is intentionally simple:
	•	static, curated markdown sources
	•	deterministic loading from rag/sources/
	•	no embeddings
	•	no vector database
	•	no semantic search

This design prioritizes:
	•	auditability
	•	predictability
	•	low complexity
	•	clear interview explanation

Future versions may introduce embeddings and semantic retrieval once
the knowledge corpus becomes large or dynamic.

⸻

LLM Interaction Layer (ai/llm_client.py)

The LLM interaction layer is implemented as a thin abstraction over
the LLM provider API.

This is the only backend module allowed to directly communicate
with an external LLM service.

⸻

Responsibilities

llm_client.py is responsible for:
	•	initializing the LLM client
	•	reading API credentials, base URLs, and model identifiers
	•	translating internal prompt payloads into provider-specific formats
	•	sending requests to the LLM
	•	returning raw text responses

It intentionally does not:
	•	build prompts
	•	apply business logic
	•	validate schemas
	•	interpret outputs
	•	perform orchestration

⸻

Provider Abstraction

ArchLens uses OpenRouter as an OpenAI-compatible gateway.

This enables:
	•	low-cost or free experimentation
	•	easy model switching
	•	avoidance of vendor lock-in

All provider-specific configuration is isolated in this module.

⸻

Message Translation

The LLM client converts the internal prompt payload into the standard
chat-completions format using:
	•	a system role message for persona and rules
	•	a user role message for task-specific input

This translation isolates protocol details and keeps the rest of the
system provider-agnostic.

⸻

Determinism and Output Handling

The LLM client uses a low temperature setting to:
	•	reduce randomness
	•	improve consistency
	•	increase schema compliance

Although the LLM may return multiple choices, ArchLens intentionally
consumes only the first response to maintain deterministic behavior.

All parsing and validation is handled outside this layer.

⸻

Backend Status (Current Checkpoint)

At this point, the backend includes:
	•	input and output contracts
	•	structured prompt system
	•	deterministic RAG retrieval (v1)
	•	isolated LLM interaction layer

The GenAI core is fully implemented and ready to be orchestrated
by the application layer.