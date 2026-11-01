# Contributing

## Commit trailers

Every ordinary commit needs two trailers, each on its own line: `Assisted-by` and `Approved-by`.

`Assisted-by` names each Grok Bot that worked on the change. One line per bot. When several bots worked on separate workstreams, list each bot on its own line:

```
Assisted-by: Grok Bot (Ship Desk)
```

A commit written entirely by a person uses exactly:

```
Assisted-by: none
```

`Approved-by` is the owner who approved the change:

```
Approved-by: Jacob Kraniak <jacob-kraniak@users.noreply.github.com>
```

Bots do not use `Co-authored-by`.

`.githooks/commit-msg` rejects a commit unless the message has a line matching `^Approved-by: .+` and either a line matching `^Assisted-by: .+` or a line matching `^Assisted-by: none$`. Merge commits and commits whose subject starts with `fixup!` or `squash!` are skipped.

Enable the hook in this clone:

```
git config core.hooksPath .githooks
```
