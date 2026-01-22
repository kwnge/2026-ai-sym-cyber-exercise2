import asyncio
import logfire
from pydantic_ai import AgentRunResult

from dotenv import load_dotenv
# Load environment variables from .env filetract
load_dotenv()

from dependencies import Deps, MissionKnowledge, AttackVector
from agents import recon_endpoint_agent, recon_auth_agent, summary_agent

# Configure Logfire tracing
logfire.configure(
    environment="2026 AI Symposium",
    service_name="Automating Recon - Exercise 2")
logfire.instrument_pydantic_ai()

# Check Deps for latest class model
async def _update_knowledge_from_results(
    results: list[AgentRunResult],
    knowledge: MissionKnowledge
) -> None:
    logfire.info('Mission knowledge (context) was updated!')

    for run_result in results:
        for v in run_result.output:
            knowledge.identified_vulns.append(v)
            knowledge.attack_surface.setdefault(v.explicit_path, [])
            knowledge.credentials_found.setdefault(v.type, [])
            knowledge.credentials_found[v.type].append(v.credentials)
            if v.type not in knowledge.attack_surface[v.explicit_path]:
                knowledge.attack_surface[v.explicit_path].append(v.type)

async def main():
    mission_dependencies = Deps(
        target="10.26.1.11:80",
        goal="Perform recon against the target and report back findings.",
        target_information="Your target is an OWASP Juice shop instance"
    )

    logfire.info(f'Starting automated recon against: {mission_dependencies.target}')

    # Define tasks for async gather
    tasks = [
        recon_endpoint_agent.run(f"Identify 5 highly vulnerable public endpoints on target {mission_dependencies.target}. Only focus on typical endpoints. Don't search for everything as we are under a time constraint. Additional information: \n{mission_dependencies.target_information}", deps=mission_dependencies),
        recon_auth_agent.run(f"Test and identify for authentication and login boundaries on target {mission_dependencies.target}. Additional information: \n{mission_dependencies.target_information}", deps=mission_dependencies),
    ]

    # Run tasks simultaneously (Python GIL limitation...)
    results = await asyncio.gather(*tasks)

    logfire.info(f'{len(tasks)} recon tasks were completed!')

    await _update_knowledge_from_results(results=results, knowledge=mission_dependencies.knowledge)
    logfire.info(f'{len(tasks)} recon tasks were completed!')

    logfire.info('Calling summary agent!')
    summary_results = await summary_agent.run(
        f"Generate summary report on latest MissionKnowledge output: {mission_dependencies.knowledge}"
        "\n Include Detailed findings review, Advisement on exploitation next steps, "
        "and possible operation security steps to remove exploitation events produced. ",
        deps=mission_dependencies
    )
    logfire.info('Summary agent completed!')

    with open('mission_summary.md', 'w') as f:
        f.write(summary_results.output)
    
if __name__ == "__main__":
    asyncio.run(main())