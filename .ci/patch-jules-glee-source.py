from pathlib import Path

path = Path('.github/workflows/jules-glee-reusable.yml')
text = path.read_text()

old_condition = "    if: ${{ github.event_name == 'pull_request_target' && github.event.action == 'opened' }}"
new_condition = "    if: ${{ github.event_name == 'pull_request_target' && (github.event.action == 'opened' || github.event.action == 'synchronize' || github.event.action == 'reopened') }}"
if old_condition not in text:
    raise SystemExit('Expected Glee job condition not found')
text = text.replace(old_condition, new_condition, 1)

old_init = """          page_token=''\n          source_name=''\n\n          while :; do\n"""
new_init = """          page_token=''\n          source_name=''\n          source_json=''\n\n          while :; do\n"""
if old_init not in text:
    raise SystemExit('Expected Jules source init block not found')
text = text.replace(old_init, new_init, 1)

old_lookup = """            source_name=\"$(jq -r \\\n              --arg owner \"$owner\" \\\n              --arg repo \"$repo\" \\\n              '[.sources[]? | select(\n                ((.githubRepo.owner // \"\") | ascii_downcase) == ($owner | ascii_downcase)\n                and ((.githubRepo.repo // \"\") | ascii_downcase) == ($repo | ascii_downcase)\n              ) | .name] | first // empty' \\\n              jules-sources.json)\"\n\n            if [[ -n \"$source_name\" ]]; then\n              break\n            fi\n"""
new_lookup = """            source_json=\"$(jq -c \\\n              --arg owner \"$owner\" \\\n              --arg repo \"$repo\" \\\n              '[.sources[]? | select(\n                ((.githubRepo.owner // \"\") | ascii_downcase) == ($owner | ascii_downcase)\n                and ((.githubRepo.repo // \"\") | ascii_downcase) == ($repo | ascii_downcase)\n              )] | first // empty' \\\n              jules-sources.json)\"\n\n            if [[ -n \"$source_json\" ]]; then\n              printf '%s\\n' \"$source_json\" > jules-source.json\n              source_name=\"$(jq -r '.name // empty' jules-source.json)\"\n              if [[ -n \"$source_name\" ]]; then\n                break\n              fi\n            fi\n"""
if old_lookup not in text:
    raise SystemExit('Expected Jules source lookup block not found')
text = text.replace(old_lookup, new_lookup, 1)

old_detail_fetch = """          curl --fail-with-body --silent --show-error \\\n            -H \"X-Goog-Api-Key: ${JULES_API_KEY}\" \\\n            \"https://jules.googleapis.com/v1alpha/${source_name}\" \\\n            > jules-source.json\n\n"""
if old_detail_fetch not in text:
    raise SystemExit('Expected Jules source detail fetch not found')
text = text.replace(old_detail_fetch, '', 1)

path.write_text(text)
