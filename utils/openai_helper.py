import os
from typing import List, Dict, Optional
from openai import OpenAI
from logging import getLogger
import textwrap

logger = getLogger(__name__)


class OpenAIHelper:
    def __init__(self, api_key: Optional[str] = None, api_base_url: Optional[str] = None, model: str = "gpt-5-nano"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter")
        
        if api_base_url:
            self.client = OpenAI(api_key=self.api_key, base_url=api_base_url)
        else:
            self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def analyze_subject_from_abstract(self, abstract: str, target_subject: List[str]) -> bool:
        """Summarize given abstract and determine if it relates to the target subject"""
        prompt = f"Analyze the following abstract and determine if it relates to the subject: {', '.join(target_subject)}.\n\n\
Abstract:\n{abstract}\n\nAnswer with 'yes' or 'no'."
        try:
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=1,
                reasoning={"effort": "low"},
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
        except Exception as e:
            logger.error(f"Error summarizing paper: {e}")
            raise Exception(f"Failed to summarize paper: {e}")

if __name__ == "__main__":
    import os
    api_key = os.getenv("OPENAI_API_KEY")

    # Example usage
    ai = OpenAIHelper(api_key)
    sample_text = """
    Artificial intelligence is transforming industries worldwide. From healthcare
    to finance, AI technologies are being integrated to improve efficiency and
    decision-making processes. However, concerns about job displacement and
    ethical implications remain significant challenges.
    """

    # ai.summarize_paper_markdown("https://arxiv.org/abs/2504.17728")
    ai.summarize_paper_message("https://arxiv.org/abs/2504.17728")