"""
Built-in Evaluators - Ported from gh-models (MIT License)

These evaluators are based on Microsoft PromptFlow's battle-tested evaluation
prompts. Each evaluator uses example-anchored definitions for consistent,
reliable scoring.

Source: https://github.com/github/gh-models (MIT License)
Original: https://github.com/microsoft/promptflow

Key improvements over prose-only rubrics:
1. Concrete query/response examples for EACH score level
2. ThoughtChain reasoning required before scoring
3. Simple choice-based score extraction (more robust than JSON parsing)
4. Standardized dimensions used across the industry
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

# =============================================================================
# DATA TYPES
# =============================================================================


@dataclass
class Choice:
    """A scoring choice with label and normalized score."""

    choice: str  # e.g., "1", "2", "poor", "excellent"
    score: float  # Normalized 0.0-1.0


@dataclass
class LLMEvaluator:
    """LLM-based evaluator with example-anchored rubric."""

    model_id: str
    system_prompt: str
    prompt: str
    choices: List[Choice]

    def get_score_from_response(self, response: str) -> Optional[tuple]:
        """Extract score from LLM response using choice matching.

        Returns (choice_label, normalized_score) or None if no match.
        Much more robust than complex JSON parsing.
        """
        response_lower = response.strip().lower()

        # Try to find the score in the last line (most reliable)
        lines = response_lower.strip().split("\n")
        last_line = lines[-1].strip() if lines else ""

        # Check for exact matches first
        for choice in self.choices:
            if last_line == choice.choice.lower():
                return (choice.choice, choice.score)

        # Then check for containment in last few lines
        search_text = "\n".join(lines[-3:]) if len(lines) >= 3 else response_lower
        for choice in self.choices:
            if choice.choice.lower() in search_text:
                return (choice.choice, choice.score)

        return None


@dataclass
class StringEvaluator:
    """Simple string-based evaluator for deterministic checks."""

    contains: Optional[str] = None
    equals: Optional[str] = None
    starts_with: Optional[str] = None
    ends_with: Optional[str] = None

    def evaluate(self, response: str, variables: Dict[str, Any] = None) -> tuple:
        """Evaluate response against string criteria.

        Returns (passed: bool, score: float, details: str)
        """
        variables = variables or {}

        # Template variable substitution
        def template(s: str) -> str:
            if not s:
                return s
            result = s
            for k, v in variables.items():
                result = result.replace(f"{{{{{k}}}}}", str(v))
            return result

        response_lower = response.lower()

        if self.equals:
            expected = template(self.equals)
            passed = response == expected
            return (
                passed,
                1.0 if passed else 0.0,
                f"Expected exact match: '{expected}'",
            )

        if self.contains:
            expected = template(self.contains).lower()
            passed = expected in response_lower
            return (
                passed,
                1.0 if passed else 0.0,
                f"Expected to contain: '{expected}'",
            )

        if self.starts_with:
            expected = template(self.starts_with).lower()
            passed = response_lower.startswith(expected)
            return (
                passed,
                1.0 if passed else 0.0,
                f"Expected to start with: '{expected}'",
            )

        if self.ends_with:
            expected = template(self.ends_with).lower()
            passed = response_lower.endswith(expected)
            return (
                passed,
                1.0 if passed else 0.0,
                f"Expected to end with: '{expected}'",
            )

        return (False, 0.0, "No evaluation criteria specified")


# =============================================================================
# STANDARD 1-5 CHOICES (used by all built-in evaluators)
# =============================================================================

STANDARD_CHOICES = [
    Choice("1", 0.0),
    Choice("2", 0.25),
    Choice("3", 0.5),
    Choice("4", 0.75),
    Choice("5", 1.0),
]

# Alternative word-based choices for rules compliance
COMPLIANCE_CHOICES = [
    Choice("poor", 0.0),
    Choice("below_average", 0.25),
    Choice("average", 0.5),
    Choice("good", 0.75),
    Choice("excellent", 1.0),
]


# =============================================================================
# BUILT-IN EVALUATORS (Ported from Microsoft PromptFlow)
# =============================================================================

BUILTIN_EVALUATORS: Dict[str, LLMEvaluator] = {
    # -------------------------------------------------------------------------
    # SIMILARITY (Answer Equivalence)
    # -------------------------------------------------------------------------
    "similarity": LLMEvaluator(
        model_id="openai/gpt-4o",
        system_prompt=(
            "You are an AI assistant. You will be given the definition of an evaluation "
            "metric for assessing the quality of an answer in a question-answering task. "
            "Your job is to compute an accurate evaluation score using the provided "
            "evaluation metric. You should return a single integer value between 1 to 5 "
            "representing the evaluation metric. You will include no other text or information."
        ),
        prompt="""Equivalence, as a metric, measures the similarity between the predicted answer and the correct answer. If the information and content in the predicted answer is similar or equivalent to the correct answer, then the value of the Equivalence metric should be high, else it should be low. Given the question, correct answer, and predicted answer, determine the value of Equivalence metric using the following rating scale:

One star: the predicted answer is not at all similar to the correct answer
Two stars: the predicted answer is mostly not similar to the correct answer
Three stars: the predicted answer is somewhat similar to the correct answer
Four stars: the predicted answer is mostly similar to the correct answer
Five stars: the predicted answer is completely similar to the correct answer

This rating value should always be an integer between 1 and 5. So the rating produced should be 1 or 2 or 3 or 4 or 5.

The examples below show the Equivalence score for a question, a correct answer, and a predicted answer.

question: What is the role of ribosomes?
correct answer: Ribosomes are cellular structures responsible for protein synthesis.
predicted answer: Ribosomes participate in the synthesizing proteins in the cell.
stars: 5

question: Why is the sky blue?
correct answer: The sky is blue because of Rayleigh scattering.
predicted answer: The sky is blue because the molecules scatter light.
stars: 4

question: What are the benefits of regular exercise?
correct answer: Regular exercise can help maintain a healthy weight, increase muscle and bone strength, and reduce the risk of chronic diseases. It also promotes mental well-being by reducing stress and improving overall mood.
predicted answer: Routine physical activity can contribute to maintaining ideal body weight, enhancing muscle and bone strength, and preventing chronic illnesses. In addition, it supports mental health by alleviating stress and augmenting general mood.
stars: 5

question: {{input}}
correct answer: {{expected}}
predicted answer: {{completion}}
stars:""",
        choices=STANDARD_CHOICES,
    ),
    # -------------------------------------------------------------------------
    # COHERENCE (Logical Flow)
    # -------------------------------------------------------------------------
    "coherence": LLMEvaluator(
        model_id="openai/gpt-4o",
        system_prompt="""# Instruction
## Goal
### You are an expert in evaluating the quality of a RESPONSE from an intelligent system based on provided definition and data. Your goal will involve answering the questions below using the information provided.
- **Definition**: You are given a definition of the communication trait that is being evaluated to help guide your Score.
- **Data**: Your input data include a QUERY and a RESPONSE.
- **Tasks**: To complete your evaluation you will be asked to evaluate the Data in different ways.""",
        prompt="""# Definition
**Coherence** refers to the logical and orderly presentation of ideas in a response, allowing the reader to easily follow and understand the writer's train of thought. A coherent answer directly addresses the question with clear connections between sentences and paragraphs, using appropriate transitions and a logical sequence of ideas.

# Ratings
## [Coherence: 1] (Incoherent Response)
**Definition:** The response lacks coherence entirely. It consists of disjointed words or phrases that do not form complete or meaningful sentences. There is no logical connection to the question, making the response incomprehensible.

**Examples:**
  **Query:** What are the benefits of renewable energy?
  **Response:** Wind sun green jump apple silence over.

  **Query:** Explain the process of photosynthesis.
  **Response:** Plants light water flying blue music.

## [Coherence: 2] (Poorly Coherent Response)
**Definition:** The response shows minimal coherence with fragmented sentences and limited connection to the question. It contains some relevant keywords but lacks logical structure and clear relationships between ideas, making the overall message difficult to understand.

**Examples:**
  **Query:** How does vaccination work?
  **Response:** Vaccines protect disease. Immune system fight. Health better.

  **Query:** Describe how a bill becomes a law.
  **Response:** Idea proposed. Congress discuss vote. President signs.

## [Coherence: 3] (Partially Coherent Response)
**Definition:** The response partially addresses the question with some relevant information but exhibits issues in the logical flow and organization of ideas. Connections between sentences may be unclear or abrupt, requiring the reader to infer the links. The response may lack smooth transitions and may present ideas out of order.

**Examples:**
  **Query:** What causes earthquakes?
  **Response:** Earthquakes happen when tectonic plates move suddenly. Energy builds up then releases. Ground shakes and can cause damage.

  **Query:** Explain the importance of the water cycle.
  **Response:** The water cycle moves water around Earth. Evaporation, then precipitation occurs. It supports life by distributing water.

## [Coherence: 4] (Coherent Response)
**Definition:** The response is coherent and effectively addresses the question. Ideas are logically organized with clear connections between sentences and paragraphs. Appropriate transitions are used to guide the reader through the response, which flows smoothly and is easy to follow.

**Examples:**
  **Query:** What is the water cycle and how does it work?
  **Response:** The water cycle is the continuous movement of water on Earth through processes like evaporation, condensation, and precipitation. Water evaporates from bodies of water, forms clouds through condensation, and returns to the surface as precipitation. This cycle is essential for distributing water resources globally.

  **Query:** Describe the role of mitochondria in cellular function.
  **Response:** Mitochondria are organelles that produce energy for the cell. They convert nutrients into ATP through cellular respiration. This energy powers various cellular activities, making mitochondria vital for cell survival.

## [Coherence: 5] (Highly Coherent Response)
**Definition:** The response is exceptionally coherent, demonstrating sophisticated organization and flow. Ideas are presented in a logical and seamless manner, with excellent use of transitional phrases and cohesive devices. The connections between concepts are clear and enhance the reader's understanding. The response thoroughly addresses the question with clarity and precision.

**Examples:**
  **Query:** Analyze the economic impacts of climate change on coastal cities.
  **Response:** Climate change significantly affects the economies of coastal cities through rising sea levels, increased flooding, and more intense storms. These environmental changes can damage infrastructure, disrupt businesses, and lead to costly repairs. For instance, frequent flooding can hinder transportation and commerce, while the threat of severe weather may deter investment and tourism. Consequently, cities may face increased expenses for disaster preparedness and mitigation efforts, straining municipal budgets and impacting economic growth.

# Data
QUERY: {{input}}
RESPONSE: {{completion}}

# Tasks
## Please provide your assessment Score for the previous RESPONSE in relation to the QUERY based on the Definitions above. Your output should include the following information:
- **ThoughtChain**: To improve the reasoning process, think step by step and include a step-by-step explanation of your thought process as you analyze the data based on the definitions. Keep it brief and start your ThoughtChain with "Let's think step by step:".
- **Explanation**: a very short explanation of why you think the input Data should get that Score.
- **Score**: based on your previous analysis, provide your Score. The Score you give MUST be a integer score (i.e., "1", "2"...) based on the levels of the definitions.

## Please provide only your Score as the last output on a new line.
# Output""",
        choices=STANDARD_CHOICES,
    ),
    # -------------------------------------------------------------------------
    # FLUENCY (Language Quality)
    # -------------------------------------------------------------------------
    "fluency": LLMEvaluator(
        model_id="openai/gpt-4o",
        system_prompt="""# Instruction
## Goal
### You are an expert in evaluating the quality of a RESPONSE from an intelligent system based on provided definition and data. Your goal will involve answering the questions below using the information provided.
- **Definition**: You are given a definition of the communication trait that is being evaluated to help guide your Score.
- **Data**: Your input data include a RESPONSE.
- **Tasks**: To complete your evaluation you will be asked to evaluate the Data in different ways.""",
        prompt="""# Definition
**Fluency** refers to the effectiveness and clarity of written communication, focusing on grammatical accuracy, vocabulary range, sentence complexity, coherence, and overall readability. It assesses how smoothly ideas are conveyed and how easily the text can be understood by the reader.

# Ratings
## [Fluency: 1] (Emergent Fluency)
**Definition:** The response shows minimal command of the language. It contains pervasive grammatical errors, extremely limited vocabulary, and fragmented or incoherent sentences. The message is largely incomprehensible, making understanding very difficult.

**Examples:**
  **Response:** Free time I. Go park. Not fun. Alone.

  **Response:** Like food pizza. Good cheese eat.

## [Fluency: 2] (Basic Fluency)
**Definition:** The response communicates simple ideas but has frequent grammatical errors and limited vocabulary. Sentences are short and may be improperly constructed, leading to partial understanding. Repetition and awkward phrasing are common.

**Examples:**
  **Response:** I like play soccer. I watch movie. It fun.

  **Response:** My town small. Many people. We have market.

## [Fluency: 3] (Competent Fluency)
**Definition:** The response clearly conveys ideas with occasional grammatical errors. Vocabulary is adequate but not extensive. Sentences are generally correct but may lack complexity and variety. The text is coherent, and the message is easily understood with minimal effort.

**Examples:**
  **Response:** I'm planning to visit friends and maybe see a movie together.

  **Response:** I try to eat healthy food and exercise regularly by jogging.

## [Fluency: 4] (Proficient Fluency)
**Definition:** The response is well-articulated with good control of grammar and a varied vocabulary. Sentences are complex and well-structured, demonstrating coherence and cohesion. Minor errors may occur but do not affect overall understanding. The text flows smoothly, and ideas are connected logically.

**Examples:**
  **Response:** My interest in mathematics and problem-solving inspired me to become an engineer, as I enjoy designing solutions that improve people's lives.

  **Response:** Environmental conservation is crucial because it protects ecosystems, preserves biodiversity, and ensures natural resources are available for future generations.

## [Fluency: 5] (Exceptional Fluency)
**Definition:** The response demonstrates an exceptional command of language with sophisticated vocabulary and complex, varied sentence structures. It is coherent, cohesive, and engaging, with precise and nuanced expression. Grammar is flawless, and the text reflects a high level of eloquence and style.

**Examples:**
  **Response:** Globalization exerts a profound influence on cultural diversity by facilitating unprecedented cultural exchange while simultaneously risking the homogenization of distinct cultural identities, which can diminish the richness of global heritage.

  **Response:** Technology revolutionizes modern education by providing interactive learning platforms, enabling personalized learning experiences, and connecting students worldwide, thereby transforming how knowledge is acquired and shared.

# Data
RESPONSE: {{completion}}

# Tasks
## Please provide your assessment Score for the previous RESPONSE based on the Definitions above. Your output should include the following information:
- **ThoughtChain**: To improve the reasoning process, think step by step and include a step-by-step explanation of your thought process as you analyze the data based on the definitions. Keep it brief and start your ThoughtChain with "Let's think step by step:".
- **Explanation**: a very short explanation of why you think the input Data should get that Score.
- **Score**: based on your previous analysis, provide your Score. The Score you give MUST be a integer score (i.e., "1", "2"...) based on the levels of the definitions.

## Please provide only your Score as the last output on a new line.
# Output""",
        choices=STANDARD_CHOICES,
    ),
    # -------------------------------------------------------------------------
    # RELEVANCE (Query Addressing)
    # -------------------------------------------------------------------------
    "relevance": LLMEvaluator(
        model_id="openai/gpt-4o",
        system_prompt="""# Instruction
## Goal
### You are an expert in evaluating the quality of a RESPONSE from an intelligent system based on provided definition and data. Your goal will involve answering the questions below using the information provided.
- **Definition**: You are given a definition of the communication trait that is being evaluated to help guide your Score.
- **Data**: Your input data include QUERY and RESPONSE.
- **Tasks**: To complete your evaluation you will be asked to evaluate the Data in different ways.""",
        prompt="""# Definition
**Relevance** refers to how effectively a response addresses a question. It assesses the accuracy, completeness, and direct relevance of the response based solely on the given information.

# Ratings
## [Relevance: 1] (Irrelevant Response)
**Definition:** The response is unrelated to the question. It provides information that is off-topic and does not attempt to address the question posed.

**Examples:**
  **Query:** What is the team preparing for?
  **Response:** I went grocery shopping yesterday evening.

  **Query:** When will the company's new product line launch?
  **Response:** International travel can be very rewarding and educational.

## [Relevance: 2] (Incorrect Response)
**Definition:** The response attempts to address the question but includes incorrect information. It provides a response that is factually wrong based on the provided information.

**Examples:**
  **Query:** When was the merger between the two firms finalized?
  **Response:** The merger was finalized on April 10th.

  **Query:** Where and when will the solar eclipse be visible?
  **Response:** The solar eclipse will be visible in Asia on December 14th.

## [Relevance: 3] (Incomplete Response)
**Definition:** The response addresses the question but omits key details necessary for a full understanding. It provides a partial response that lacks essential information.

**Examples:**
  **Query:** What type of food does the new restaurant offer?
  **Response:** The restaurant offers Italian food like pasta.

  **Query:** What topics will the conference cover?
  **Response:** The conference will cover renewable energy and climate change.

## [Relevance: 4] (Complete Response)
**Definition:** The response fully addresses the question with accurate and complete information. It includes all essential details required for a comprehensive understanding, without adding any extraneous information.

**Examples:**
  **Query:** What type of food does the new restaurant offer?
  **Response:** The new restaurant offers Italian cuisine, featuring dishes like pasta, pizza, and risotto.

  **Query:** What topics will the conference cover?
  **Response:** The conference will cover renewable energy, climate change, and sustainability practices.

## [Relevance: 5] (Comprehensive Response with Insights)
**Definition:** The response not only fully and accurately addresses the question but also includes additional relevant insights or elaboration. It may explain the significance, implications, or provide minor inferences that enhance understanding.

**Examples:**
  **Query:** What type of food does the new restaurant offer?
  **Response:** The new restaurant offers Italian cuisine, featuring dishes like pasta, pizza, and risotto, aiming to provide customers with an authentic Italian dining experience.

  **Query:** What topics will the conference cover?
  **Response:** The conference will cover renewable energy, climate change, and sustainability practices, bringing together global experts to discuss these critical issues.

# Data
QUERY: {{input}}
RESPONSE: {{completion}}

# Tasks
## Please provide your assessment Score for the previous RESPONSE in relation to the QUERY based on the Definitions above. Your output should include the following information:
- **ThoughtChain**: To improve the reasoning process, think step by step and include a step-by-step explanation of your thought process as you analyze the data based on the definitions. Keep it brief and start your ThoughtChain with "Let's think step by step:".
- **Explanation**: a very short explanation of why you think the input Data should get that Score.
- **Score**: based on your previous analysis, provide your Score. The Score you give MUST be a integer score (i.e., "1", "2"...) based on the levels of the definitions.

## Please provide only your Score as the last output on a new line.
# Output""",
        choices=STANDARD_CHOICES,
    ),
    # -------------------------------------------------------------------------
    # GROUNDEDNESS (Context Anchoring)
    # -------------------------------------------------------------------------
    "groundedness": LLMEvaluator(
        model_id="openai/gpt-4o",
        system_prompt="""# Instruction
## Goal
### You are an expert in evaluating the quality of a RESPONSE from an intelligent system based on provided definition and data. Your goal will involve answering the questions below using the information provided.
- **Definition**: You are given a definition of the communication trait that is being evaluated to help guide your Score.
- **Data**: Your input data include CONTEXT, QUERY, and RESPONSE.
- **Tasks**: To complete your evaluation you will be asked to evaluate the Data in different ways.""",
        prompt="""# Definition
**Groundedness** refers to how well an answer is anchored in the provided context, evaluating its relevance, accuracy, and completeness based exclusively on that context. It assesses the extent to which the answer directly and fully addresses the question without introducing unrelated or incorrect information. The scale ranges from 1 to 5, with higher numbers indicating greater groundedness.

# Ratings
## [Groundedness: 1] (Completely Unrelated Response)
**Definition:** An answer that does not relate to the question or the context in any way. It fails to address the topic, provides irrelevant information, or introduces completely unrelated subjects.

**Examples:**
  **Context:** The company's annual meeting will be held next Thursday.
  **Query:** When is the company's annual meeting?
  **Response:** I enjoy hiking in the mountains during summer.

  **Context:** The new policy aims to reduce carbon emissions by 20% over the next five years.
  **Query:** What is the goal of the new policy?
  **Response:** My favorite color is blue.

## [Groundedness: 2] (Related Topic but Does Not Respond to the Query)
**Definition:** An answer that relates to the general topic of the context but does not answer the specific question asked. It may mention concepts from the context but fails to provide a direct or relevant response.

**Examples:**
  **Context:** The museum will exhibit modern art pieces from various local artists.
  **Query:** What kind of art will be exhibited at the museum?
  **Response:** Museums are important cultural institutions.

  **Context:** The new software update improves battery life and performance.
  **Query:** What does the new software update improve?
  **Response:** Software updates can sometimes fix bugs.

## [Groundedness: 3] (Attempts to Respond but Contains Incorrect Information)
**Definition:** An answer that attempts to respond to the question but includes incorrect information not supported by the context. It may misstate facts, misinterpret the context, or provide erroneous details.

**Examples:**
  **Context:** The festival starts on June 5th and features international musicians.
  **Query:** When does the festival start?
  **Response:** The festival starts on July 5th and features local artists.

  **Context:** The recipe requires two eggs and one cup of milk.
  **Query:** How many eggs are needed for the recipe?
  **Response:** You need three eggs for the recipe.

## [Groundedness: 4] (Partially Correct Response)
**Definition:** An answer that provides a correct response to the question but is incomplete or lacks specific details mentioned in the context. It captures some of the necessary information but omits key elements needed for a full understanding.

**Examples:**
  **Context:** The bookstore offers a 15% discount to students and a 10% discount to senior citizens.
  **Query:** What discount does the bookstore offer to students?
  **Response:** Students get a discount at the bookstore.

  **Context:** The company's headquarters are located in Berlin, Germany.
  **Query:** Where are the company's headquarters?
  **Response:** The company's headquarters are in Germany.

## [Groundedness: 5] (Fully Correct and Complete Response)
**Definition:** An answer that thoroughly and accurately responds to the question, including all relevant details from the context. It directly addresses the question with precise information, demonstrating complete understanding without adding extraneous information.

**Examples:**
  **Context:** The author released her latest novel, 'The Silent Echo', on September 1st.
  **Query:** When was 'The Silent Echo' released?
  **Response:** 'The Silent Echo' was released on September 1st.

  **Context:** Participants must register by May 31st to be eligible for early bird pricing.
  **Query:** By what date must participants register to receive early bird pricing?
  **Response:** Participants must register by May 31st to receive early bird pricing.

# Data
CONTEXT: {{expected}}
QUERY: {{input}}
RESPONSE: {{completion}}

# Tasks
## Please provide your assessment Score for the previous RESPONSE in relation to the CONTEXT and QUERY based on the Definitions above. Your output should include the following information:
- **ThoughtChain**: To improve the reasoning process, think step by step and include a step-by-step explanation of your thought process as you analyze the data based on the definitions. Keep it brief and start your ThoughtChain with "Let's think step by step:".
- **Explanation**: a very short explanation of why you think the input Data should get that Score.
- **Score**: based on your previous analysis, provide your Score. The Score you give MUST be a integer score (i.e., "1", "2"...) based on the levels of the definitions.

## Please provide only your Score as the last output on a new line.
# Output""",
        choices=STANDARD_CHOICES,
    ),
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def get_evaluator(name: str) -> Optional[LLMEvaluator]:
    """Get a built-in evaluator by name."""
    return BUILTIN_EVALUATORS.get(name.lower())


def list_evaluators() -> List[str]:
    """List all available built-in evaluators."""
    return list(BUILTIN_EVALUATORS.keys())


def template_prompt(prompt: str, variables: Dict[str, Any]) -> str:
    """Template a prompt string with variables using {{variable}} syntax.

    This is compatible with gh-models' simple templating approach.
    """
    result = prompt
    for key, value in variables.items():
        result = result.replace(f"{{{{{key}}}}}", str(value))
    return result


# =============================================================================
# EVALUATOR RUNNER
# =============================================================================


class EvaluatorRunner:
    """Runs built-in evaluators against model outputs.

    Compatible with gh-models' evaluation pattern:
    1. Template the prompt with test data variables
    2. Call the judge model
    3. Extract score using choice matching
    """

    def __init__(self, llm_client=None):
        """Initialize runner with an LLM client.

        Args:
            llm_client: Client with generate_text(model_name, prompt, temperature) method
        """
        self.llm_client = llm_client

    def run_evaluator(
        self,
        evaluator_name: str,
        test_data: Dict[str, Any],
        completion: str,
        model_override: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Run a single evaluator on a completion.

        Args:
            evaluator_name: Name of built-in evaluator (e.g., "similarity", "coherence")
            test_data: Dict with input/expected values
            completion: The model's completion to evaluate
            model_override: Optional model to use instead of evaluator's default

        Returns:
            Dict with evaluator_name, score, passed, details
        """
        evaluator = get_evaluator(evaluator_name)
        if not evaluator:
            return {
                "evaluator_name": evaluator_name,
                "score": 0.0,
                "passed": False,
                "details": f"Evaluator '{evaluator_name}' not found",
            }

        # Prepare variables for templating
        variables = dict(test_data)
        variables["completion"] = completion

        # Template the prompt
        templated_prompt = template_prompt(evaluator.prompt, variables)

        # Build messages
        messages = []
        if evaluator.system_prompt:
            messages.append({"role": "system", "content": evaluator.system_prompt})
        messages.append({"role": "user", "content": templated_prompt})

        # Call LLM
        if self.llm_client is None:
            return {
                "evaluator_name": evaluator_name,
                "score": 0.0,
                "passed": False,
                "details": "No LLM client configured",
            }

        model = model_override or evaluator.model_id

        # Convert model_id format if needed (gh-models uses "openai/gpt-4o")
        if model.startswith("openai/"):
            model = f"gh:{model.split('/')[-1]}"

        try:
            # Build full prompt from messages
            full_prompt = ""
            for msg in messages:
                if msg["role"] == "system":
                    full_prompt += f"System: {msg['content']}\n\n"
                else:
                    full_prompt += f"{msg['content']}"

            response = self.llm_client.generate_text(
                model_name=model,
                prompt=full_prompt,
                temperature=0.0,  # Deterministic for evaluation
            )

            # Extract score using choice matching
            result = evaluator.get_score_from_response(response)

            if result:
                choice_label, score = result
                return {
                    "evaluator_name": evaluator_name,
                    "score": score,
                    "passed": score > 0,
                    "details": f"LLM evaluation matched choice: '{choice_label}'",
                    "raw_response": response,
                }
            else:
                return {
                    "evaluator_name": evaluator_name,
                    "score": 0.0,
                    "passed": False,
                    "details": "LLM response did not match any defined choices",
                    "raw_response": response,
                }

        except Exception as e:
            return {
                "evaluator_name": evaluator_name,
                "score": 0.0,
                "passed": False,
                "details": f"Evaluation failed: {str(e)}",
            }

    def run_string_evaluator(
        self,
        evaluator: StringEvaluator,
        name: str,
        response: str,
        variables: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Run a string-based evaluator.

        Args:
            evaluator: StringEvaluator instance
            name: Name for the evaluator
            response: Response to evaluate
            variables: Template variables

        Returns:
            Dict with evaluator_name, score, passed, details
        """
        passed, score, details = evaluator.evaluate(response, variables)
        return {
            "evaluator_name": name,
            "score": score,
            "passed": passed,
            "details": details,
        }


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    print("Available built-in evaluators:")
    for name in list_evaluators():
        evaluator = get_evaluator(name)
        print(f"  - {name}: {evaluator.model_id}")

    print(
        "\nThese evaluators use example-anchored definitions from Microsoft PromptFlow."
    )
    print(
        "Usage: runner.run_evaluator('similarity', {'input': '...', 'expected': '...'}, completion)"
    )
