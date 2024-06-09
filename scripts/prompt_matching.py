import os
import numpy as np
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
from langchain_openai import ChatOpenAI
from langchain.schema import Document as LangchainDocument, HumanMessage

# Initialize OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')


def generate_single_prompt(llm, human_message):
  """
  Generates a single prompt using the provided LLM and HumanMessage object.

  Args:
      llm: A ChatOpenAI instance for interacting with the language model.
      human_message: A HumanMessage object containing the user prompt and context.

  Returns:
      str: The generated prompt.
  """

  # Option 1: Wrap human_message in a list (if compatible)
  # Try wrapping the human_message in a list to see if llm.generate can handle it.
  message_list = [human_message]
  response = llm.generate(message_list)

  # Option 2: Manual Loop (if wrapping is not compatible)
  # If wrapping doesn't work, use a loop to generate a single response.
  response = llm.generate(human_message)  # Try generating directly

  # Return the first generated content
  return response.generations[0].message.content



def match_prompt_with_gpt(user_prompt, relevant_contexts, openai_api_key):
  """
  Matches the user prompt with relevant contexts and generates multiple prompts using GPT-3.5-turbo.

  Args:
      user_prompt: The user's original prompt.
      relevant_contexts: A list of LangchainDocument objects containing relevant background information.
      openai_api_key: Your OpenAI API key.

  Returns:
      str: The most similar prompt.
      list: A list of all generated prompts ranked by similarity.
  """

  llm = ChatOpenAI(
      openai_api_key=openai_api_key,
      model_name="gpt-3.5-turbo",
      temperature=0.7
  )

  # Combine user prompt with relevant contexts
  combined_context = "\n".join([doc.page_content for doc in relevant_contexts])
  complete_input_with_instruction = (
      f"Context:\n{combined_context}\n\nUser Prompt: {user_prompt}\n\n"
      "Generate five high-quality prompts based on the user's input."
  )

  # Create HumanMessage object
  human_message = HumanMessage(content=complete_input_with_instruction)

  # Generate five prompts using the defined function
  responses = [generate_single_prompt(llm, human_message) for _ in range(5)]

  # Encode prompts using BERT
  prompt_encodings = []
  for prompt in responses:
      inputs = tokenizer(prompt, return_tensors='pt')
      outputs = model(**inputs)
      prompt_encodings.append(outputs.last_hidden_state.mean(dim=1).detach().numpy())

  # Encode the user input
  user_input_encoding = tokenizer(user_prompt, return_tensors='pt')
  user_input_output = model(**user_input_encoding)
  user_input_vector = user_input_output.last_hidden_state.mean(dim=1).detach().numpy()

  # Calculate cosine similarity between user input and generated prompts
  similarities = [cosine_similarity(user_input_vector, prompt_vec)[0][0] for prompt_vec in prompt_encodings]

  # Rank the prompts based on similarity scores
  ranked_prompts = sorted(zip(responses, similarities), key=lambda x: x[1], reverse=True)
  best_prompt = ranked_prompts[0][0]

  return best_prompt, [prompt for prompt, score in ranked_prompts]

# Example usage
if __name__ == "__main__":
  user_prompt = "What are week 3 challenge deliverables?"
  relevant_contexts = [LangchainDocument(page_content="Example context")]

  if not openai_api_key:
      raise ValueError("OpenAI API key not found. Please set it in your environment variables.")

  best_prompt, ranked_prompts = match_prompt_with_gpt(user_prompt, relevant_contexts, openai_api_key)
  print("Best Prompt:", best_prompt)
  print("Ranked Prompts:", ranked_prompts)
