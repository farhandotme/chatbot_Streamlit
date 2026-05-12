from agents import critic_chain, writer_chain, build_search_agent, build_reader_agent
from rich import print


def run_research_pipeline(topic: str) -> dict:
    state = {}

    print("\n" + "= " * 50)
    print("Step 1 - Search Agent is working....")
    print("\n" + "= " * 50)
    search_agent = build_search_agent()
    search_result = search_agent.invoke(
        {
            "messages": [
                f"Find recent, reliable and detailed information about : {topic}"
            ]
        }
    )
    state["Search_result"] = search_result["messages"][-1].content
    print("Search Results : ", state["Search_result"])

    print("\n" + "= " * 50)
    print("Reader agent is scraping top resources")
    print("\n" + "= " * 50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"""
                            Based on the following search results about {topic}, 
                            Pick the most relevent url and scrape it for deeper content
                            Search results : {state["Search_result"][:800]}
                       """,
                )
            ]
        }
    )
    state["Scraped_content"] = reader_result["messages"][-1].content

    print(f"The Scraped Content is in the below :\n", state["Scraped_content"])

    # writer chain

    print("\n" + "= " * 50)
    print("Writer is Drafting the report")
    print("\n" + "= " * 50)

    combained_report = f"Search Results : {state['Search_result']} \n Detailed Scraped Content: {state["Scraped_content"]}"

    state["report"] = writer_chain.invoke(
        {"topic": topic, "research": combained_report}
    )

    print(f"Final Report : {state['report']}")

    print("\n" + "= " * 50)
    print("Critic is Reviewing the Report")
    print("\n" + "= " * 50)

    state["feedback"] = critic_chain.invoke({"report": state["report"]})
    print(f"\n critic Report : {state['feedback']}")

    return state


if __name__ == "__main__":
    topic = input("You : ")
    run_research_pipeline(topic)
