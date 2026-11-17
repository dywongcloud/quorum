# QUORUM panel protocol: a verdict is a file

A panel round is several independent agents run at once, and the harness that
runs them is not reliable. A seat can be launched, do all its work, write its
verdict, and have the connection drop before the verdict reaches the caller.
When that happens the caller sees a failure and the work looks lost. It is not
lost if the verdict is a file: it is still on disk.

This is a distributed-systems fact applied to the panel itself: an at-least-once
delivery channel with a dropped acknowledgement is not a failure of the
computation. The file is the durable acknowledgement. Do not treat the return
value as the source of truth.

## The rule

**A verdict is a file, not a return value.** A seat has reported when its file
exists and has enough words to name an anchor and point at the work. Nothing
else counts: not the launch call, not a completion notice, not what the caller
remembers seeing.

## What the caller does

1. **Make a panel directory before launching anything.** One per round:
   `panel/R1/`, `panel/R2/`. It is the round's state, so a session that restarts
   can be resumed by listing it instead of re-running everything.
2. **Launch at most three seats at a time.** Seven seats in one batch produce
   transport failures; three short seats in a batch do not. A large panel is
   several batches, and the wall clock is barely worse because each batch is
   short. This is a concurrency bound on a contended channel, not a coverage
   bound.
3. **Keep each seat prompt under about 350 words.** Give the seat a file of
   measured facts to read rather than paraphrasing the artifact into the prompt.
4. **Every seat prompt ends with the filing instruction**, naming the absolute
   path:

   > Write your report to `<panel_dir>/<seat>.md` as your last action, then
   > return the same text. If the connection drops, the file is the verdict.

5. **Before re-running a failed seat, check whether its file exists.** A dropped
   agent has usually already written it. Re-running a seat whose verdict is on
   disk wastes the seat and risks two conflicting verdicts under one name. This
   is the idempotence axiom `f(f(x)) = f(x)` applied to dispatch.
6. **Bound the retries: three attempts per seat.** After that, stop.
7. **Collect, then write the Panel Report.** Run `collect_panel.py`; read what is
   there. A required seat with no file is recorded as
   `NOT REPORTED (3 attempts, transport failure)` -- never as PASS, never
   reconstructed from what the caller thinks that authority would have said. A
   required seat that never reports leaves the run incomplete, and the final
   reply names it.

## What the seat prompt needs

- Which round and which seat, and the doctrine it argues from alone.
- Where the artifact is, and where the measured evidence file is.
- The four required fields: Anchor used / Observed / Verdict / Requested change.
- The word budget.
- The instruction not to read or react to any other seat.
- The filing instruction, with the path.

Nothing else. Everything else belongs in a file the seat reads.

## Recursive gm agents

A seat that is itself driven by the gm skill mints **its own** `SESSION_ID`,
derived from the parent id plus the seat index. It never inherits the parent's
literal id: concurrent seats sharing one session id read each other's responses
from the spool. A seat dispatches its own `instruction`, `codesearch` and
`phase-status` verbs under that id, and its verdict file carries the dispatch
id as the witness tuple `(id, hash, ts)`. A parent resolving a PRD row cites a
witness dispatch id from a seat's session, never one from its own.
