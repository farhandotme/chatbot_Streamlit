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

    combained_report = f"Search Results : {state['Search_result']} \n Detailed Scraped Content: {state['Scraped_content']}"

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


def run_pipeline_streamlit(topic: str, st_session) -> None:
    """
    Streamlit-aware version of the pipeline.
    Updates st.session_state at each step so the UI can reflect progress.

    Call this from app.py instead of run_research_pipeline().
    """
    try:
        state = {}

        # ── Step 1 : Search Agent ──────────────────────────────────────────
        st_session.active_step = "search"
        st_session.logs.append(("info", "Search Agent initialised — querying the web…"))

        search_agent = build_search_agent()
        search_result = search_agent.invoke(
            {
                "messages": [
                    f"Find recent, reliable and detailed information about : {topic}"
                ]
            }
        )
        state["Search_result"] = search_result["messages"][-1].content
        st_session.results["search"] = state["Search_result"]
        st_session.done_steps.append("search")
        st_session.logs.append(("ok", "Search complete — results captured."))

        # ── Step 2 : Reader Agent ──────────────────────────────────────────
        st_session.active_step = "reader"
        st_session.logs.append(("warn", "Reader Agent scraping top URL…"))

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
        st_session.results["scrape"] = state["Scraped_content"]
        st_session.done_steps.append("reader")
        st_session.logs.append(("ok", "Scraping complete — content extracted."))

        # ── Step 3 : Writer Chain ──────────────────────────────────────────
        st_session.active_step = "writer"
        st_session.logs.append(("info", "Writer Chain drafting report…"))

        combined_report = (
            f"Search Results : {state['Search_result']} \n"
            f"Detailed Scraped Content: {state['Scraped_content']}"
        )
        state["report"] = writer_chain.invoke(
            {"topic": topic, "research": combined_report}
        )
        st_session.results["report"] = state["report"]
        st_session.done_steps.append("writer")
        st_session.logs.append(("ok", "Draft report ready."))

        # ── Step 4 : Critic Chain ──────────────────────────────────────────
        st_session.active_step = "critic"
        st_session.logs.append(("warn", "Critic Chain reviewing report…"))

        state["feedback"] = critic_chain.invoke({"report": state["report"]})
        st_session.results["critic"] = state["feedback"]
        st_session.done_steps.append("critic")
        st_session.logs.append(("ok", "Review complete — Pipeline finished ✓"))

        st_session.active_step = None

    except Exception as exc:
        st_session.error = str(exc)
        st_session.logs.append(("warn", f"Error: {exc}"))

    finally:
        st_session.running = False


if __name__ == "__main__":
    topic = input("You : ")
    run_research_pipeline(topic)
