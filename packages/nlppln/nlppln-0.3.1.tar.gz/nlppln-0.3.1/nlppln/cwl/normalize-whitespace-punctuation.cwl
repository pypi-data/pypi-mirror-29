#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "-m", "nlppln.commands.normalize_whitespace_punctuation"]

doc: |
  Normalize whitespace and punctuation.

  Replace multiple subsequent occurrences of whitespace characters and
  punctuation with a single occurrence.

inputs:
  meta_in:
    type: File
    inputBinding:
      position: 1

outputs:
  metadata_out:
    type: File
    outputBinding:
      glob: "*.txt"
