import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.globals import set_debug
from langchain.prompts import PromptTemplate
from agents.linkedin import LinkedInAgent
from services.linkedin import LinkedInService


if __name__ == "__main__":
    load_dotenv(override=True)
    set_debug(True)

    OPEN_AI_BASE_URL = os.getenv("OPEN_AI_BASE_URL")
    OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")

    llm = ChatOpenAI(
        base_url=OPEN_AI_BASE_URL,
        api_key=OPEN_AI_API_KEY,
        temperature=0,
    )

    linkedin_agent = LinkedInAgent()
    linkedin_url = linkedin_agent.get_profile_url(
        name="Bill Gates",
        llm=llm,
    )
    print(linkedin_url)

    if linkedin_url is None:
        print("Linked profile not found for given name")
    else:
        linkedin_id = LinkedInService.extract_id_from_url(linkedin_url)
        print(">>>>", linkedin_id)
        linkedin_service = LinkedInService()
        user_detail = linkedin_service.get_user_detail(username=linkedin_id, mock=False)
        prompt_template = PromptTemplate(
            template="""From the following LinkedIn profile json information, provide these details of the user:
            - name
            - description
            - company
            - position
            - location
            - experiences

            Here's the LinkedIn profile information of the user: {profile_data}
            """,
            input_variables=["profile_data"],
        )
        chain = prompt_template | llm
        print(">>>", user_detail)
        res = chain.invoke(input={"profile_data": str(user_detail)})
        print(res)
