import datetime
import os

def minutes_to_markdown(minutes_obj, output_dir="."):
    """
    Save meeting minutes to markdown file.
    """
    title = minutes_obj.get("title") or "Meeting Minutes"
    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{safe_title}_{timestamp}.md"
    out_path = os.path.join(output_dir, filename)

    md = []
    md.append(f"# {title}\n")
    md.append(f"_Generated: {datetime.datetime.now().isoformat()}_\n")
    if minutes_obj.get("attendees"):
        md.append("## Attendees\n")
        for a in minutes_obj["attendees"]:
            md.append(f"- {a}")
        md.append("\n")
    md.append("## Summary\n")
    md.append(minutes_obj.get("summary","") + "\n")
    md.append("## Decisions\n")
    for d in minutes_obj.get("decisions", []):
        md.append(f"- {d}")
    md.append("\n## Action Items\n")
    for ai in minutes_obj.get("action_items", []):
        if isinstance(ai, dict):
            task = ai.get("task") or ""
            owner = ai.get("owner") or "Unassigned"
            due = ai.get("due") or ""
            md.append(f"- **{task}** — Owner: {owner} — Due: {due}")
        else:
            md.append(f"- {ai}")
    md.append("\n---\n")
    md.append("### Full Transcript\n```\n")
    md.append(minutes_obj.get("_transcript",""))
    md.append("\n```\n")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    return out_path
