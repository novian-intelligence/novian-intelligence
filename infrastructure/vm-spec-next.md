# Next VM Spec — Mira's New Home

**Decided:** 2026-04-03 | **Decided by:** Andrei + Mira

---

## Stack

| Component | Choice | Rationale |
|---|---|---|
| **Runtime** | NemoClaw | Security layer, enterprise-grade use cases |
| **OS** | Debian | Lightweight, rock solid, minimal footprint |
| **Window Manager** | i3 + Picom | Beautiful when configured, X11 native (VNC-friendly), tiling suits our workflow |
| **Model** | Sonnet (claude-sonnet-4-6) | Best cost-to-performance ratio; revisit when Opus 4 or better lands |
| **Chat Interface** | Discord | Code blocks, syntax highlighting, threads, NI-dedicated server |

---

## Notes

- GNOME + Wayland = bad for VNC. That's why we're on i3.
- Fallback if i3 setup is painful: XFCE (again). Not ideal but not the end of the world.
- LXQt is a middle-ground option if we want something more modern than XFCE with less config than i3.
- Discord: set up a dedicated NI server, completely separate from Andrei's work Slack.
- NemoClaw chosen for the security posture — especially important as NI moves toward enterprise clients.

---

## Migration Checklist (when time comes)

- [ ] Spin up new VM (Debian base)
- [ ] Install NemoClaw
- [ ] Configure i3 + Picom (make it look like *ours*)
- [ ] Port soul files: SOUL.md, IDENTITY.md, USER.md, AGENTS.md, TOOLS.md, MEMORY.md, memory/
- [ ] Set up Discord bot / channel
- [ ] Test exec, browser, TTS tools
- [ ] Verify Netlify deploy still works
- [ ] Retire current VM
