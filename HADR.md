# High Availability and Disaster Recovery (HADR)

Sitebender's "everything is data" architecture transforms HADR from an
operational bolt-on into a first-class design principle. When your entire
application — structure, content, behavior, validation — lives as queryable RDF
triples, recovery becomes straightforward: recover the graph, recover
everything.

## The Fundamental Advantage

Traditional web applications scatter state across application memory, database
rows, file systems, external services, and browser state. Coordinating recovery
across N systems requires N strategies.

Sitebender collapses all state into one queryable knowledge graph. One backup
strategy. One recovery procedure. One source of truth.

```
Traditional: State lives in N places → coordinate N recovery strategies
Sitebender:  State lives in triples → recover the graph, recover everything
```

## RPO and RTO by Data Category

| Category       | Examples                | RPO    | RTO     | Strategy                               |
| -------------- | ----------------------- | ------ | ------- | -------------------------------------- |
| **Critical**   | Auth sessions, payments | 0      | <1 min  | Sync replication, hot standby          |
| **Important**  | User content, settings  | <1 min | <5 min  | Async replication, warm standby        |
| **Standard**   | Comments, reactions     | <5 min | <15 min | Async replication, cold standby        |
| **Deferrable** | Analytics, logs         | <1 hr  | <4 hr   | Batch replication, restore from backup |

## Layer-by-Layer Architecture

### Triple Store Layer (Oxigraph)

The single source of truth. HADR here is HADR everywhere.

#### Synchronous Replication (Zero RPO)

```
Write Request → Primary Oxigraph → Replicate → Secondary Acknowledges → Return Success
```

Every write confirmed on N nodes before acknowledgment. Guarantees zero data
loss at the cost of latency proportional to network distance. Use for
authentication state, financial transactions, anything where data loss is
unacceptable.

#### Asynchronous Replication (Near-Zero RPO)

```
Write Request → Primary Oxigraph → Return Success → Background Replication
```

Write acknowledged immediately, replicated in background. RPO equals replication
lag (typically milliseconds to seconds). Use for content, user preferences,
anything tolerating small loss windows.

#### Named Graph Partitioning

RDF's named graphs enable per-graph replication policies:

```turtle
# Critical: Synchronous replication, zero RPO
GRAPH <urn:sitebender:auth> {
  :session123 :belongsTo :user456 ;
              :expiresAt "2025-12-16T23:00:00Z"^^xsd:dateTime .
}

# Important: Async replication, 5-second RPO
GRAPH <urn:sitebender:content> {
  :article789 :title "Understanding HADR" ;
              :author :user456 .
}

# Deferrable: Eventual consistency acceptable
GRAPH <urn:sitebender:analytics> {
  :pageView999 :page :article789 ;
               :timestamp "2025-12-16T12:00:00Z"^^xsd:dateTime .
}
```

Different data categories receive different replication policies without
requiring multiple databases.

### Application Layer

The rendering pipeline is stateless and deterministic:

```
Triples → SPARQL Query → JSON → Render → HTML
```

Any node can render any page given access to the triple store. No sticky
sessions required. Horizontal scaling is trivial. Failover is instant—failed
node's requests route to any other node producing identical output because same
triples yield same HTML.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Node A    │     │   Node B    │     │   Node C    │
│  (Render)   │     │  (Render)   │     │  (Render)   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌──────┴──────┐
                    │   Oxigraph  │
                    │  (Primary)  │
                    └─────────────┘
```

### Client Layer

Oxigraph runs as WASM in browsers, enabling local-first architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │   Oxigraph  │    │   Service   │    │  IndexedDB  │      │
│  │    WASM     │◄──►│   Worker    │◄──►│  (Persist)  │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
│         ▲                                                   │
│         │ SPARQL                                            │
│         ▼                                                   │
│  ┌─────────────┐                                            │
│  │  Architect  │                                            │
│  │  Renderer   │                                            │
│  └─────────────┘                                            │
└─────────────────────────────────────────────────────────────┘
         │
         │ Sync (when online)
         ▼
┌─────────────────────┐
│   Server Oxigraph   │
└─────────────────────┘
```

The browser maintains its own triple store. If the server is unavailable:

- Reads work against local data
- Writes queue locally
- Sync occurs when connectivity is restored

Users may not notice server outages for many operations.

## Event Sourcing

Instead of storing current state, store the sequence of events that produced it:

```typescript
type MutationEvent = Tagged<"MutationEvent"> & {
	readonly id: UUID;
	readonly timestamp: Instant;
	readonly graph: IRI;
	readonly operation: "INSERT" | "DELETE";
	readonly triples: ReadonlyArray<Triple>;
	readonly actor: IRI;
	readonly causedBy?: UUID;
};
```

The event log IS the backup:

- RPO = time since last event persisted
- Point-in-time recovery by replaying events to any point
- Complete audit trail
- Reproduce any historical state

```
Event Log:
┌────────────────────────────────────────────────────────────┐
│ E1: UserCreated { id: u1, email: "..." }                   │
│ E2: ArticleCreated { id: a1, author: u1, title: "..." }    │
│ E3: ArticlePublished { id: a1 }                            │
│ E4: ArticleEdited { id: a1, title: "New Title" }           │◄── Disaster here
│ E5: CommentAdded { article: a1, author: u2, text: "..." }  │
└────────────────────────────────────────────────────────────┘

Recovery:
1. Load last snapshot (before E3)
2. Replay E3, E4, E5
3. Current state restored
```

## CRDT-Based Conflict Resolution

When multiple nodes accept writes during a partition, CRDTs (Conflict-free
Replicated Data Types) enable automatic, lossless merging.

### CRDT Selection by Triple Pattern

**Single-Value Properties (Functional Properties)**

```turtle
:user123 :email "user@example.com" .
```

Use LWW-Register (Last-Writer-Wins with timestamp). Higher timestamp wins;
tie-break on node ID.

**Multi-Value Properties (Non-Functional Properties)**

```turtle
:article123 :tag "hadr" .
:article123 :tag "architecture" .
```

Use OR-Set (Observed-Remove Set). Additions and removals merge without conflict.

**Ordered Sequences (RDF Lists)**

```turtle
:article123 :sections ( :intro :body :conclusion ) .
```

Use RGA (Replicated Growable Array). Concurrent insertions receive deterministic
ordering.

**Counters (Aggregates)**

```turtle
:article123 :viewCount 12345 .
```

Use PN-Counter (Positive-Negative Counter). Each node tracks its own increments
and decrements; sum yields correct total.

## Degradation Levels

The three rendering modes map to graceful degradation:

### Level 0: Full Operation (Production)

```
JSX → IR → Triples → Oxigraph (Primary) → SPARQL → JSON → HTML
```

All features available. Real-time data. Full write capability.

### Level 1: Degraded (Integration)

```
JSX → IR → Triples → Oxigraph (Replica) → SPARQL → JSON → HTML
```

Read operations work. Writes queued or rejected. Data may be slightly stale
within RPO.

### Level 2: Emergency (Development)

```
JSX → IR → JSON (Cached) → HTML
```

Triple store bypassed. Serve from CDN/cache. Static content only.

### Level 3: Maintenance

```
Static HTML: "We're down for maintenance"
```

Honest communication with estimated restoration time.

## Multi-Region Architecture

### Active-Active

```
┌─────────────────┐                    ┌─────────────────┐
│   US-EAST       │                    │   EU-WEST       │
│  ┌───────────┐  │    Event Stream    │  ┌───────────┐  │
│  │ Oxigraph  │  │◄──────────────────►│  │ Oxigraph  │  │
│  └───────────┘  │                    │  └───────────┘  │
│  ┌───────────┐  │                    │  ┌───────────┐  │
│  │  Operator │  │◄──────────────────►│  │  Operator │  │
│  │ Event Log │  │                    │  │ Event Log │  │
│  └───────────┘  │                    │  └───────────┘  │
└─────────────────┘                    └─────────────────┘
```

Multiple regions serve traffic. Each region has a full Oxigraph instance. CRDTs
resolve conflicts. Events replicate bidirectionally.

### Active-Passive

Primary region handles all writes. Secondary regions receive replicated data.
Failover promotes secondary to primary on failure.

## Backup Strategies

### Full Backup

Serialize entire triple store as N-Quads (preserves named graphs):

```sparql
CONSTRUCT { GRAPH ?g { ?s ?p ?o } } WHERE { GRAPH ?g { ?s ?p ?o } }
```

Compress and store in multiple geographic locations.

### Incremental Backup

Query only graphs modified since last backup:

```sparql
CONSTRUCT { GRAPH ?g { ?s ?p ?o } }
WHERE {
  GRAPH <urn:sitebender:metadata> {
    ?g :lastModified ?modified .
    FILTER(?modified > "2025-12-15T00:00:00Z"^^xsd:dateTime)
  }
  GRAPH ?g { ?s ?p ?o }
}
```

### Continuous Backup

Event log replication provides near-zero RPO. Every mutation captured as an
immutable event.

## Recovery Validation

After recovery, SHACL shapes validate the restored triple store:

```sparql
SELECT ?focusNode ?resultMessage
WHERE {
  ?report a sh:ValidationReport ;
          sh:result ?result .
  ?result sh:focusNode ?focusNode ;
          sh:resultMessage ?resultMessage ;
          sh:resultSeverity sh:Violation .
}
```

If violations exist, the recovery introduced inconsistencies. The AI-Safe
Architecture ensures invalid states are immediately detectable.

## Named Graph Convention

Graph naming encodes replication policy:

```turtle
<urn:sitebender:critical:auth>         # Sync replicated
<urn:sitebender:important:content>     # Async, 1-min max lag
<urn:sitebender:standard:social>       # Async, 5-min max lag
<urn:sitebender:deferrable:analytics>  # Eventually consistent

GRAPH <urn:sitebender:meta:replication> {
  <urn:sitebender:critical:auth>
    :replicationPolicy :synchronous ;
    :replicas ( <urn:node:us-east-1> <urn:node:us-west-2> ) ;
    :lastSync "2025-12-16T12:00:00.000Z"^^xsd:dateTime .
}
```

## Backup Metadata as Triples

```turtle
GRAPH <urn:sitebender:meta:backups> {
  <urn:backup:2025-12-16T00:00:00Z>
    :timestamp "2025-12-16T00:00:00Z"^^xsd:dateTime ;
    :type :full ;
    :location "s3://sitebender-backups/2025-12-16/full.nq.zst" ;
    :tripleCount 1234567 ;
    :compressedSize 52428800 ;
    :checksum "sha256:abc123..." ;
    :eventLogPosition "evt-123456" .
}
```

## Runbooks as Triples

Operational procedures stored in the knowledge graph:

```turtle
GRAPH <urn:sitebender:runbooks> {
  :primaryFailover a :Runbook ;
    :trigger "primary_unreachable_5min" ;
    :steps ( :verifyPrimaryDown :promoteReplica :updateDNS :notifyOncall ) ;
    :estimatedDuration "PT5M"^^xsd:duration .
}
```

## Summary

| Traditional                                  | Sitebender                       |
| -------------------------------------------- | -------------------------------- |
| State scattered across app, DB, cache, files | State unified in triple store    |
| Coordinate N backup strategies               | One backup strategy              |
| Failover requires session migration          | Stateless rendering, no sessions |
| App-specific conflict resolution             | Universal CRDT merge semantics   |
| Manual recovery validation                   | SHACL validates automatically    |
| Uniform RPO across all data                  | Per-graph RPO via named graphs   |
| Separate audit trail system                  | Event sourcing IS the data model |
| Client recovery loses local state            | Browser has its own triple store |

The architecture embodies HADR principles:

- **Backup** = serialize triples
- **Recovery** = load triples
- **Replication** = sync triples
- **Validation** = SHACL check triples
- **Audit** = query event triples
