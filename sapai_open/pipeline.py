"""Section-by-section SAP generation pipeline.

Faithful to the paper: for each SAP section, calls the chosen LLM provider
with the section-specific prompt from `prompts_paper_v1`, using the common
system message parameterised by the protocol text.

The prompt functions in `prompts_paper_v1` take no arguments and return the
section prompt as a string. The system message takes the protocol text.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from . import prompts_paper_v1 as prompts
from .chat import ChatBackend


@dataclass(frozen=True)
class Section:
    """One SAP section: a key, a human-readable title, and the prompt fn."""

    key: str
    title: str
    prompt_fn: Callable[[], str]


# Ordered list of sections. Order matches the paper's section sequence
# (Gamble et al. framework, as referenced in the paper Methods §"Prompt
# development process, Stage 2").
SECTIONS: List[Section] = [
    Section("admin", "Administrative Information", prompts.generate_admin_prompt),
    Section("introduction", "Introduction", prompts.generate_introduction_prompt),
    Section("study_design", "Study Design", prompts.generate_study_design_prompt),
    Section("randomisation", "Randomisation", prompts.generate_randomisation_prompt),
    Section("sample_size", "Sample Size", prompts.generate_sample_size_prompt),
    Section(
        "interim_analysis",
        "Interim Analyses / Internal Pilot",
        prompts.generate_interim_analysis_prompt,
    ),
    Section("timing", "Timing of Final Analysis", prompts.generate_timing_prompt),
    Section(
        "analysis_considerations",
        "General Statistical Principles",
        prompts.generate_analysis_considerations_prompt,
    ),
    Section("trial_population", "Trial Population", prompts.generate_trial_population_prompt),
    Section("endpoint", "Outcome Definitions", prompts.generate_endpoint_prompt),
    Section(
        "inferential_analysis",
        "Primary and Secondary Analyses",
        prompts.generate_inferential_analysis_prompt,
    ),
    Section(
        "assumptions_sensitivity",
        "Assumptions and Sensitivity Analyses",
        prompts.generate_assumptions_sensitivity_analysis_prompt,
    ),
    Section("subgroup_analysis", "Subgroup Analyses", prompts.generate_subgroup_analysis_prompt),
    Section("missing_data", "Missing Data", prompts.generate_missing_data_prompt),
    Section("additional_analysis", "Additional Analyses", prompts.generate_additional_analysis),
    Section("harms", "Adverse Events / Harms", prompts.generate_harms),
    Section("statistical_software", "Statistical Software", prompts.generate_statistical_software),
]


@dataclass
class SAPDraft:
    """Result of running the pipeline. Section content keyed by `Section.key`."""

    sections: Dict[str, str] = field(default_factory=dict)
    errors: Dict[str, str] = field(default_factory=dict)
    trial_title: Optional[str] = None

    @property
    def section_order(self) -> List[Section]:
        return SECTIONS


def run_pipeline(
    *,
    protocol_text: str,
    chat: ChatBackend,
    progress_callback: Optional[Callable[[int, int, str], None]] = None,
) -> SAPDraft:
    """Generate a full SAP draft section by section.

    Args:
        protocol_text: extracted plain-text of the clinical trial protocol.
        chat: a ChatBackend (from sapai_open.chat).
        progress_callback: optional fn(i, n_total, section_title) for UI hooks.

    Returns:
        SAPDraft with per-section content (and any per-section error strings).
    """
    system_message = prompts.system_message(protocol_text)
    draft = SAPDraft()
    n = len(SECTIONS)
    for i, section in enumerate(SECTIONS):
        if progress_callback is not None:
            progress_callback(i, n, section.title)
        try:
            content = chat.get_response(
                prompt=section.prompt_fn(),
                system_message=system_message,
            )
            draft.sections[section.key] = content or ""
        except Exception as e:
            draft.errors[section.key] = str(e)
            draft.sections[section.key] = ""

    if progress_callback is not None:
        progress_callback(n, n, "Complete")

    # Best-effort: pull a short title from the admin section's first line for
    # filenames; user can always rename the downloaded file.
    admin_text = draft.sections.get("admin", "")
    if admin_text:
        first_line = admin_text.strip().splitlines()[0][:120]
        draft.trial_title = first_line.strip()

    return draft
