---
name: session-pickup
description: "Resume from a prior session's trail without redoing it. Use for /session-pickup."
disable-model-invocation: true
# 這四行開頭是我們加的。原檔是 poteto-mode 裡的一頁劇本，沒有自己的開頭。
# 來源：cursor/plugins pstack/skills/poteto-mode/playbooks/session-pickup.md @ 7a58391。第 1 步的對話紀錄位置從 Cursor 的換成 Claude Code 的，其餘原文未改。
---

### Session pickup

**You own the resume point. Read the prior trail, don't redo it.**

1. Locate the prior trail. A local transcript under Claude Code's per-project transcripts directory at `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/<encoded-cwd>/*.jsonl` (`<encoded-cwd>` is the directory the session started in, with every character that is not a letter or digit replaced by `-`. Do not glob across other directories under `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/`, that crosses workspace boundaries and reads private chats from unrelated projects), a cloud-agent URL, or a pushed branch. Read the metadata overview and last messages first, then scan back for the decision points. Parse a long transcript in a subagent and keep the reduced timeline in the main thread (the **principle-guard-the-context-window** skill). Pick each subagent's reasoning level for the job, per the Subagents section.
2. Reconstruct operational state. The branch and worktree, what already landed (`git log`, `git diff` against the base), the open todos, the decisions made. The prior trail is authoritative input. Resist the bias to re-derive it.
3. Diff done vs pending. Compare what shipped against what was planned, name the resume point, do not re-run the prior repro or redo completed work. A "let me verify from scratch" pass means you're treating the trail as untrustworthy when it's authoritative.
4. Route the remaining work to the matching playbook and pick the verdict: continue the execution, ship a finished recommendation, ratify or override a prior conclusion, or postmortem a failed run. The pickup playbook ends here. The routed playbook owns the rest.
5. Verify the inherited claims against the original goal on the real artifact (the **principle-prove-it-works** skill). A passing prior self-report is not the proof.

**Reply:** where the prior agent stopped, what you inherited vs redid (ideally nothing redone), the resume point, and the outcome.
