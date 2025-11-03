from __future__ import annotations

from typing import Annotated, List
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict, HttpUrl, field_validator

# ---------- Common constrained scalars ----------
Percentage = Annotated[float, Field(ge=0, le=100, description="0–100 percentage")]
NonNegativeNumber = Annotated[float, Field(ge=0, description="Non-negative number")]
Ratio01 = Annotated[float, Field(ge=0, le=1, description="Ratio in [0, 1]")]

# Optional: a permissive ISO-8601 duration pattern for strings like 'PT2H', 'P3D', etc.
ISO_DURATION_PATTERN = r"^P(?=.*[T\d])(?:\d+Y)?(?:\d+M)?(?:\d+D)?(?:T(?:\d+H)?(?:\d+M)?(?:\d+S)?)?$"


# ---------- Enums ----------
class DurationUnits(str, Enum):
    hours = "hours"
    minutes = "minutes"
    days = "days"


class ToleranceModelType(str, Enum):
    exponential = "exponential"
    linear = "linear"
    custom = "custom"
    unknown = "unknown"


class ToleranceDataQuality(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"
    anecdotal = "anecdotal"
    theoretical = "theoretical"


class CategoryEnum(str, Enum):
    psychedelic = "psychedelic"
    gabapentinoid = "gabapentinoid"
    antipsychotic = "antipsychotic"
    medical_off_label = "medical|off-label"
    cannabinoid = "cannabinoid"
    cariotoxic = "cariotoxic"
    hepatotoxic = "hepatotoxic"
    ototoxic = "ototoxic"
    neurotoxic = "neurotoxic"
    carcinogenic = "carcinogenic"
    toxic_unspecified = "toxic|unspecified"
    irreversible_damage = "irreversible-damage"
    dissociative = "dissociative"
    stimulant = "stimulant"
    research_chemical = "research-chemical"
    empathogen = "empathogen"
    habit_forming = "habit-forming"
    opioid = "opioid"
    depressant = "depressant"
    hallucinogen = "hallucinogen"
    entactogen = "entactogen"
    deliriant = "deliriant"
    antidepressant = "antidepressant"
    sedative = "sedative"
    nootropic = "nootropic"
    barbiturate = "barbiturate"
    benzodiazepine = "benzodiazepine"
    supplement = "supplement"
    stimulant_sedative = "stimulant-sedative"
    anorectic = "anorectic"
    antiepileptic = "antiepileptic"
    antihistamine = "antihistamine"


# ---------- $defs ----------
class DurationRange(BaseModel):
    model_config = ConfigDict(extra="forbid")
    min: float = Field(description="Minimum duration value")
    max: float = Field(description="Maximum duration value")
    iso: List[Annotated[str, Field(pattern=ISO_DURATION_PATTERN)]] = Field(
        description="ISO 8601 duration format representations"
    )
    note: str = Field(description="Additional notes about the duration")


class DurationPhase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    start: float = Field(description="Start time of this phase")
    end: float = Field(description="End time of this phase")
    iso_start: List[Annotated[str, Field(pattern=ISO_DURATION_PATTERN)]] = Field(
        description="ISO 8601 duration format for start time"
    )
    iso_end: List[Annotated[str, Field(pattern=ISO_DURATION_PATTERN)]] = Field(
        description="ISO 8601 duration format for end time"
    )


class DurationCurveData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reference: str = Field(description="Citation or reference for the duration data")
    units: DurationUnits = Field(description="Time units used")
    total_duration: DurationRange
    onset: DurationPhase
    peak: DurationPhase
    offset: DurationPhase
    after_effects: DurationPhase


class DurationCurveEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")
    method: str = Field(description="Route of administration (e.g., oral, IV, insufflated, smoked)")
    duration_curve: DurationCurveData


class DoseRanges(BaseModel):
    model_config = ConfigDict(extra="forbid")
    threshold: str = Field(description="Threshold dose.")
    light: str = Field(description="Light dose.")
    common: str = Field(description="Common dose.")
    strong: str = Field(description="Strong dose.")
    heavy: str = Field(description="Heavy dose.")


class RouteOfAdministration(BaseModel):
    model_config = ConfigDict(extra="forbid")
    route: Annotated[
        str,
        Field(
            pattern=r"^[A-Za-z]+$",
            description="The route of administration. SINGLE WORD OR ABBREVIATION ONLY (e.g., oral, smoked, IV, insufflated).",
        ),
    ]
    units: str = Field(description="Units of measurement (e.g., mg, µg, ml).")
    notes: str = Field(
        description=(
            "Commentary on provenance and context; if mostly derived from user reports, it MUST be noted as such."
        )
    )
    dose_ranges: DoseRanges


class Dosages(BaseModel):
    model_config = ConfigDict(extra="forbid")
    routes_of_administration: List[RouteOfAdministration] = Field(
        description="Dosages information for different routes of administration."
    )


class DurationSummary(BaseModel):
    """String-based duration summary ($defs.duration in original schema)."""

    model_config = ConfigDict(extra="forbid")
    total_duration: str = Field(description="Total duration of effects.")
    onset: str = Field(description="Onset time of effects.")
    peak: str = Field(description="Peak time of effects.")
    offset: str = Field(description="Offset time of effects.")
    after_effects: str = Field(description="Duration of after-effects.")


class Interactions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    dangerous: List[str] = Field(description="Dangerous drug interactions.")
    unsafe: List[str] = Field(description="Unsafe drug interactions.")
    caution: List[str] = Field(description="Interactions that require caution.")


class ToleranceModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: ToleranceModelType = Field(description="The mathematical model used to describe tolerance changes")
    build_rate: NonNegativeNumber = Field(description="Rate at which tolerance develops (percentage per hour)")
    decay_rate: NonNegativeNumber = Field(description="Rate at which tolerance decays (percentage per hour)")
    half_life: NonNegativeNumber = Field(description="Half-life of tolerance decay in hours")


class ToleranceTimelinePoint(BaseModel):
    model_config = ConfigDict(extra="forbid")
    hours: NonNegativeNumber = Field(description="Time in hours since last use")
    tolerance_percentage: Percentage = Field(description="Percentage of tolerance remaining (0-100)")
    confidence: Percentage = Field(description="Confidence level in this data point (0-100)")


class ToleranceBaselinePoint(BaseModel):
    model_config = ConfigDict(extra="forbid")
    hours: float = Field(description="Hours for this tolerance marker")
    confidence: Percentage = Field(description="Confidence in this estimate (0-100)")


class ToleranceBaselines(BaseModel):
    model_config = ConfigDict(extra="forbid")
    full_tolerance: ToleranceBaselinePoint
    half_tolerance: ToleranceBaselinePoint
    baseline_tolerance: ToleranceBaselinePoint


class CrossToleranceEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")
    substance: str = Field(description="Name of substance with cross-tolerance")
    ratio: Ratio01 = Field(description="Approximate ratio of cross-tolerance (0-1)")
    confidence: Percentage = Field(description="Confidence in this estimate (0-100)")


class ToleranceData(BaseModel):
    """Complex tolerance object used by the root schema."""

    model_config = ConfigDict(extra="forbid")
    model: ToleranceModel = Field(description="Mathematical model for tolerance development and decay")
    timeline: List[ToleranceTimelinePoint] = Field(description="Discrete points on the tolerance curve")
    baselines: ToleranceBaselines = Field(description="Key tolerance timeline markers")
    cross_tolerances: List[CrossToleranceEntry] = Field(description="Substances with cross-tolerance")
    notes: str = Field(description="Additional notes about tolerance patterns or data quality")
    data_quality: ToleranceDataQuality = Field(description="Overall quality assessment of tolerance data")


class ToleranceSimple(BaseModel):
    """
    Unused $defs.tolerance object preserved for completeness:
    { full_tolerance: str, half_tolerance: str, zero_tolerance: str, cross_tolerances: [str] }
    """

    model_config = ConfigDict(extra="forbid")
    full_tolerance: str = Field(description="Time to full tolerance.")
    half_tolerance: str = Field(description="Time to half tolerance.")
    zero_tolerance: str = Field(description="Time to zero tolerance.")
    cross_tolerances: List[str] = Field(description="Substances with cross-tolerance.")


class Citation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(description="The name or title of the citation.")
    reference: str = Field(description="The URL or other reference of the citation.")


# ---------- Root model ----------
class DrugInfo(BaseModel):
    model_config = ConfigDict(
        extra="forbid",  # additionalProperties: false across the model
        validate_assignment=True,
    )

    drug_name: str = Field(
        description="Primary name of the substance as commonly recognized across sources."
    )
    search_url: Annotated[
        HttpUrl,
        # Negative lookahead to forbid PsychonautWiki
        Field(pattern=r"^(?!.*psychonautwiki\.org).*"),
    ] = Field(
        description=(
            "URL to a comprehensive information repository. Must NOT be a PsychonautWiki.org URL."
        )
    )
    chemical_class: str = Field(
        description="Chemical class of the substance based on structural/functional similarity."
    )
    psychoactive_class: str = Field(
        description="Psychoactive class reflecting CNS effects."
    )

    dosages: Dosages
    duration: DurationSummary
    duration_curves: List[DurationCurveEntry] = Field(
        description="ROA-specific duration curve data for plotting drug effect timelines"
    )

    addiction_potential: str = Field(
        description="Description of addiction potential based on epidemiology, case reports, and user accounts."
    )
    interactions: Interactions

    notes: str = Field(
        description=(
            "Additional notes/warnings for harm reduction. Must include at least 3 sentences; "
            "ideally 5–20 concise, pertinent facts."
        )
    )
    subjective_effects: List[str] = Field(
        description="List of subjective effects aggregated from user reports and research."
    )

    # Complex tolerance object (NOT the simple $defs.tolerance)
    tolerance: ToleranceData

    half_life: str = Field(
        description="Pharmacokinetic half-life as reported in studies."
    )

    citations: List[Citation] = Field(
        description="Citations supporting the information provided."
    )
    categories: List[CategoryEnum] = Field(
        description="List of categories the drug belongs to."
    )

    # ----- Validators -----
    @field_validator("search_url")
    @classmethod
    def _no_psychonautwiki(cls, v: HttpUrl) -> HttpUrl:
        host = getattr(v, "host", "")
        if host and "psychonautwiki.org" in host.lower():
            raise ValueError("search_url must not be a PsychonautWiki.org URL")
        if "psychonautwiki.org" in str(v).lower():
            raise ValueError("search_url must not be a PsychonautWiki.org URL")
        return v

    @field_validator("notes")
    @classmethod
    def _notes_min_sentences(cls, v: str) -> str:
        # crude sentence count: split on ., !, ?; count non-empty segments
        import re
        sentences = [s for s in re.split(r"[.!?]+", v) if s.strip()]
        if len(sentences) < 3:
            raise ValueError("notes must contain at least 3 sentences")
        return v


# ---------- Helper: emit OpenAI Structured Outputs schema ----------
def to_openai_structured_output() -> dict:
    """
    Build the exact response_format payload for OpenAI Structured Outputs.

    Returns:
        {
          "type": "json_schema",
          "json_schema": {
             "name": "drug_info",
             "strict": True,
             "schema": <DrugInfo JSON Schema Draft 2020-12>
          }
        }
    """
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "drug_info",
            "strict": True,
            "schema": DrugInfo.model_json_schema(),
        },
    }
