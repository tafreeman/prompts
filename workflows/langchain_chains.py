"""Scaffold LangChain chain constructors for the LATS workflow.

These functions try to construct LangChain chains if `langchain` is installed.
They intentionally avoid executing LLM calls at import time. If LangChain
is not available, calling the constructor will raise an informative error.

Usage example:
  from workflows.langchain_chains import create_scoring_chain
  chain = create_scoring_chain()
  result = chain.run({"prompt": my_prompt, "criteria": criteria})
"""

from __future__ import annotations


def _require_langchain():
    try:
        pass  # type: ignore
    except Exception as e:
        raise ImportError(
            "langchain is not installed. Install it with `pip install langchain` "
            "and a provider SDK (openai, anthropic, etc.) to use these chains."
        ) from e


def create_criteria_validator_chain(llm=None):
    """Return a LangChain LLMChain or a callable that validates criteria.

    If `llm` is None the function will construct a default LLM from environment
    using LangChain's default LLM class (if available).
    """
    _require_langchain()
    from langchain import LLMChain, PromptTemplate  # type: ignore
    from langchain.llms import OpenAI  # type: ignore

    if llm is None:
        llm = OpenAI(temperature=0.0)

    prompt = PromptTemplate(
        input_variables=["manifest"],
        template=(
            "Validate the grading_criteria in the provided manifest (YAML/JSON).\n"
            "Return a JSON object with fields: criteria_valid (bool), effective_criteria (map), evidence (list).\n"
            "Manifest:\n{manifest}"
        ),
    )
    return LLMChain(llm=llm, prompt=prompt)


def create_scoring_chain(llm=None):
    """Return a LangChain chain that scores a prompt per-criterion.

    The chain should accept inputs: prompt (string), effective_criteria (map)
    and return a JSON-like string with per_criterion scores and weighted_score.
    """
    _require_langchain()
    from langchain import LLMChain, PromptTemplate  # type: ignore
    from langchain.llms import OpenAI  # type: ignore

    if llm is None:
        llm = OpenAI(temperature=0.0)

    prompt = PromptTemplate(
        input_variables=["prompt_text", "criteria_json"],
        template=(
            "You are an objective evaluator. Given the prompt and the grading criteria, "
            "produce a JSON object with keys: per_criterion (map of numeric scores 0-10) "
            "and weighted_score (0-10).\nPrompt:\n{prompt_text}\nCriteria:\n{criteria_json}"
        ),
    )
    return LLMChain(llm=llm, prompt=prompt)


def create_implementer_chain(llm=None):
    """Return a LangChain chain that suggests concrete prompt edits
    (implementer).

    Inputs: prompt_text, prioritized_fixes (list)
    Output: updated_prompt (string) and top_action (string)
    """
    _require_langchain()
    from langchain import LLMChain, PromptTemplate  # type: ignore
    from langchain.llms import OpenAI  # type: ignore

    if llm is None:
        llm = OpenAI(temperature=0.0)

    prompt = PromptTemplate(
        input_variables=["prompt_text", "top_fix"],
        template=(
            "Apply the following top_fix to the prompt_text and return a JSON object: {updated_prompt, top_action}.\n"
            "Top fix:\n{top_fix}\nPrompt:\n{prompt_text}"
        ),
    )
    return LLMChain(llm=llm, prompt=prompt)


def create_validator_chain(llm=None):
    """Return a LangChain chain that validates an updated prompt against tests.

    Inputs: updated_prompt, test_spec (optional)
    Output: JSON with pass/fail and issues.
    """
    _require_langchain()
    from langchain import LLMChain, PromptTemplate  # type: ignore
    from langchain.llms import OpenAI  # type: ignore

    if llm is None:
        llm = OpenAI(temperature=0.0)

    prompt = PromptTemplate(
        input_variables=["updated_prompt", "test_spec"],
        template=(
            "Run quick validation checks on the updated_prompt and return JSON: {passed: bool, issues: []}.\n"
            "Updated prompt:\n{updated_prompt}\nTests:\n{test_spec}"
        ),
    )
    return LLMChain(llm=llm, prompt=prompt)
