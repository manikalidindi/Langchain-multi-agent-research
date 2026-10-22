
from src.agents.agents import (
    build_search_agent,
    build_scrape_agent,
    writer_chain,
    critic_chain,
)


def research_pipeline(topic: str) -> dict:
    state = {}

    # Step 1: Search
    print("\n" + "=" * 50)
    print("Step 1 - Search agent is working...")
    print("=" * 50)

    search_agent = build_search_agent()

    search_results = search_agent.invoke({
        "messages": [
            (
                "user",
                f"Find recent, reliable, and detailed information about: {topic}",
            )
        ]
    })

    state["search_results"] = search_results["messages"][-1].content

    print("\nSearch results:\n", state["search_results"])

    # Step 2: Scrape
    print("\n" + "=" * 50)
    print("Step 2 - Scrape agent is working...")
    print("=" * 50)

    reader_agent = build_scrape_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"Based on the search results about '{topic}', "
                "identify the most relevant URLs and scrape them for "
                "additional detail. Prefer reliable primary sources.\n\n"
                f"Search results:\n{state['search_results'][:4000]}"
            )
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    print("\nScraped content:\n", state["scraped_content"])

    # Step 3: Write report
    print("\n" + "=" * 50)
    print("Step 3 - Writer is generating the research report...")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })

    print("\nFinal research report:\n", state["report"])

    # Step 4: Critique report
    print("\n" + "=" * 50)
    print("Step 4 - Critic is evaluating the report...")
    print("=" * 50)

    state["critique"] = critic_chain.invoke({
        "report": state["report"],
    })

    print("\nReport critique:\n", state["critique"])

    return state
