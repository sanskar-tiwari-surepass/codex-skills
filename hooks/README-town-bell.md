Town bell Stop hook

- Hook entrypoint: `/Users/sanskartiwari/.codex/hooks/stop_checker_hook.py`
- Hook config: `/Users/sanskartiwari/.codex/hooks.json`
- Sound asset: `/Users/sanskartiwari/.codex/assets/town-bell.mp3`

Behavior:

- Always rings the bell when a Stop hook fires.
- Only activates stop enforcement when the transcript contains an explicit `$stop-checker` invocation.
- Re-checks every stop attempt in the thread, so a later `continue` or `blocked` artifact is still forced to continue.
- Current continuation checks:
  - require a `<stop_checker>` XML artifact in the latest assistant message
  - allow stop when the artifact says `done`
  - force continuation when the artifact says `continue`
  - force continuation when the artifact says `blocked`
  - force continuation when the XML artifact is missing or invalid

Source notes:

- The canonical gameplay reference is the Age of Empires wiki `Town Bell` page:
  `https://ageofempires.fandom.com/wiki/Town_Bell`
- The AoE wiki does not expose a directly downloadable Town Bell sound asset on that page, and Fandom blocks direct media fetches from the shell.
- The current local MP3 is sourced from the real AoE2 interface asset pack on The Sounds Resource:
  `https://sounds.spriters-resource.com/pc_computer/ageofempiresii/asset/426500/`
- The hook asset was rebuilt from the extracted `town_bell1.wav` entry in that ZIP.
