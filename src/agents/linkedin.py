from langchain_openai import ChatOpenAI
from tools.tavily import Tavily
from langchain import hub
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate


class LinkedInAgent:
    def get_profile_url(self, name: str, llm: ChatOpenAI) -> str | None:
        """
        Agent to crawl the internet and find the LinkedIn profile url of a person.
        Args:
            name(str): Name of the person
            llm(ChatOpenAO): LLM to use for agent execution
        Returns:
            (str | None): LinkedIn URL
        """
        prompt_template = PromptTemplate(
            template="""Given the name of the person {name}, I want you to get their LinkedIn profile page url. Your answer should only contain a url link.""",
            input_variables=["name"],
        )

        tavily = Tavily()

        tools = [
            Tool(
                name="google_search",
                description="Useful when you want to search for profile url such as LinkedIn, Twitter, etc. of a user on the internet.",
                func=tavily.search,
            )
        ]

        react_template = hub.pull("hwchase17/react")

        agent = create_react_agent(
            llm=llm,
            prompt=react_template,
            tools=tools,
        )
        agent_exec = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
        )

        res = agent_exec.invoke(
            input={
                "input": prompt_template.format_prompt(
                    name=name,
                )
            }
        )
        return None if ("output" not in res or res is None) else res["output"]
