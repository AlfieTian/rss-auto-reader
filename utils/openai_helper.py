import os
from typing import List, Dict, Optional
from openai import OpenAI
from .logger import MyLogger
import textwrap

logger = MyLogger("OpenAIHelper")

class OpenAIHelper:
    def __init__(self, api_key: Optional[str] = None, api_base_url: Optional[str] = None, model: str = "gpt-5-nano", reasoning: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter")
        
        if api_base_url:
            self.client = OpenAI(api_key=self.api_key, base_url=api_base_url)
        else:
            self.client = OpenAI(api_key=self.api_key)
        self.reasoning = reasoning
        self.model = model

    def analyze_subject_from_abstract(self, abstract: str, target_subject: List[str], exclude_subject: List[str]) -> bool:
        """Summarize given abstract and determine if it relates to the target subject"""

        # Normalize inputs so None/strings won't crash join()
        def _as_list(value):
            if value is None:
                return []
            if isinstance(value, str):
                return [value]
            try:
                return list(value)
            except TypeError:
                return [str(value)]

        targets = _as_list(target_subject)
        exclusions = _as_list(exclude_subject)

        head = textwrap.dedent("""
            You are a binary classifier. Follow these rules strictly and output only yes or no in lowercase.

            Targets: {targets}
            Exclusions: {exclusions}

            Rules:
            - If the abstract mainly talks about any Exclusions -> no.
            - Else if it relates to any Targets -> yes.
            - If both appear -> no.
            - If unclear/insufficient info/off-topic -> no.
            - No explanation, no quotes, only yes or no.

            Abstract:
        """).format(
            targets=", ".join(targets) if targets else "(none)",
            exclusions=", ".join(exclusions) if exclusions else "(none)",
        ).strip()
        prompt = f"{head}\n{abstract}\n\nAnswer:\n"
        try:
            if self.reasoning:
                response = self.client.responses.create(
                    model=self.model,
                    input=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=1,
                    reasoning={"effort": self.reasoning},
                )
                logger.debug(f"OpenAI response: {response}")
                return response.output_text.lower() == 'yes'
            else:
                response = self.client.responses.create(
                    model=self.model,
                    input=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=1,
                )
                logger.debug(f"OpenAI response: {response}")
                return response.output_text.lower() == 'yes'
        except Exception as e:
            logger.error(f"Error analyzing subject from abstract: {e}")
            raise Exception(f"Failed to analyze subject from abstract: {e}")

    def summarize_paper_message(self, file) -> str:
        """Summarize the paper uploaded"""
        role_prompt = textwrap.dedent("""\
                                      You are an academic assistant. Summarize the user's uploaded paper using the fewest words possible. 
                                      Output only the following template (exclude anything in brackets). Use 2-3 sentences per part, preserve key numbers, 
                                      and avoid speculation, filler, or questions. No extra text before or after the template.
                                      ❓ Problems: 
                                        [1-2 sentences]

                                      🛠️ Core Method: 
                                        [2-3 sentences]

                                      📈 Main Results/Impact: 
                                        [1-2 sentences]

                                      ⚠️ Limitation: 
                                        [1-2 sentences]

                                      DON'T ASK ANYTHING MORE. JUST RESPOND.
                                      """).strip()
        user_prompt = f"Please summarize the following paper:"
        try:
            if self.reasoning:
                response = self.client.responses.create(
                    model=self.model,
                    input=[
                        {
                            "role": "system",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": role_prompt
                                }
                            ]
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": user_prompt
                                },
                                {
                                    "type": "input_file",
                                    "file_url": file
                                }
                            ]
                        }
                    ],
                    temperature=1,
                    reasoning={"effort": self.reasoning},
                )
                logger.debug(f"OpenAI response: {response}")
                
                return response.output_text
            else:
                response = self.client.responses.create(
                    model=self.model,
                    input=[
                        {
                            "role": "system",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": role_prompt
                                }
                            ]
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": user_prompt
                                },
                                {
                                    "type": "input_file",
                                    "file_url": file
                                }
                            ]
                        }
                    ],
                    temperature=1,
                )
                logger.debug(f"OpenAI response: {response}")

                return response.output_text
        except Exception as e:
            logger.error(f"Error summarizing paper: {e}")
            raise Exception(f"Failed to summarize paper: {e}")
        
    def summarize_paper_markdown(self, file) -> str:
        """Summarize the paper uploaded in Markdown format"""
        role_prompt = textwrap.dedent("""\
            You are an academic assistant. Summarize the user's uploaded paper using the fewest words possible.
            Output using the following template (exclude anything in brackets) in Markdown format (4 H2 titles).
            Use 2-3 sentences per part, preserve key numbers, and avoid speculation or questions.
            No extra text before or after the template.

            ## ❓ Problems:
            [1-2 sentences]

            ## 🛠️ Core Method:
            [2-3 sentences]

            ## 📈 Main Results/Impact:
            [1-2 sentences]

            ## ⚠️ Limitations:
            [1-2 sentences]
        """).strip('\n')
        user_prompt = f"Please summarize the following paper:"
        try:
            if self.reasoning:
                response = self.client.responses.create(
                    model=self.model,
                    input=[
                        {
                            "role": "system",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": role_prompt
                                }
                            ]
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": user_prompt
                                },
                                {
                                    "type": "input_file",
                                    "file_url": file
                                }
                            ]
                        }
                    ],
                    temperature=1,
                    reasoning={"effort": "low"},
                )
                logger.debug(f"OpenAI response: {response}")

                return response.output_text
            else:
                response = self.client.responses.create(
                    model=self.model,
                    input=[
                        {
                            "role": "system",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": role_prompt
                                }
                            ]
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": user_prompt
                                },
                                {
                                    "type": "input_file",
                                    "file_url": file
                                }
                            ]
                        }
                    ],
                    temperature=1,
                )
                logger.debug(f"OpenAI response: {response}")

                return response.output_text
        except Exception as e:
            logger.error(f"Error summarizing paper: {e}")
            raise Exception(f"Failed to summarize paper: {e}")

if __name__ == "__main__":
    import os
    api_key = os.getenv("OPENAI_API_KEY")

    # Example usage
    ai = OpenAIHelper(api_key, model="gpt-4.1-mini")
    sample_text = textwrap.dedent("""
    Artificial intelligence is transforming industries worldwide. From healthcare
    to finance, AI technologies are being integrated to improve efficiency and
    decision-making processes. However, concerns about job displacement and
    ethical implications remain significant challenges.
    """)
    print(ai.analyze_subject_from_abstract(sample_text, ["AI", "Machine Learning"], ["Robots"]))
    # ai.summarize_paper_markdown("https://arxiv.org/abs/2504.17728")
    # ai.summarize_paper_message("https://arxiv.org/abs/2504.17728")
