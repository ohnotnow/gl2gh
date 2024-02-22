import argparse
import asyncio
from gepetto import gpt
from yaspin import yaspin

async def main():
    # set up argparse to accept a --file argument
    parser = argparse.ArgumentParser(description="GitLab CI to GitHub Actions converter")

    parser.add_argument("--file", default=".gitlab-ci.yml", help="The gitlab CI file to convert to a GitHub Actions file")
    parser.add_argument("--show-useage", action="store_true", help="Show the cost/token usage of the API calls")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--thorough", action="store_true", help="Take extra time to make sure the conversion is thorough")
    group.add_argument("--quick", action="store_true", help="Use a quicker model to convert the file and fewer steps")
    args = parser.parse_args()

    total_cost = 0
    total_tokens = 0

    if args.quick:
        openai_model = "gpt-3.5-turbo-0125"
    else:
        openai_model = "gpt-4-turbo-preview"

    # read the gitlab CI file
    with open(args.file, "r") as file:
        gitlab_ci = file.read()

    model = gpt.GPTModel()

    with yaspin(text="Getting a plan of action to convert GitLab CI file to GitHub Actions", color="yellow") as spinner:
        messages = [
            {
                "role": "system",
                "content": "Your MISSION is to help users who want to migrate from using GitLab CI/CD to using GitHub Actions. You should read the users GitLab CI file and think step-by-step how it would be successfully converted.  Note stages, environment variables, artifacts etc.  Do NOT write the new file - just give the user your detailed plan on how to do it for this specific file."
            },
            {
                "role": "user",
                "content": gitlab_ci
            }
        ]
        response = await model.chat(messages, model=openai_model, temperature=0.7, top_p=1.0)
    print(response.message)
    if args.show_useage:
        print(response.usage)
        total_cost += response.cost
        total_tokens += response.tokens
    print("\n\n")
    with yaspin(text="Taking plan of action and applying it", color="yellow") as spinner:
        messages = [
            {
                "role": "system",
                "content": "Your MISSION is to help users convert their GitLab CI yaml files to a well documented GitHub Actions file. You will be provided with the original GitLab CI file and a plan of action.  You MUST convert ALL of the steps - do NOT BE LAZY. You should ONLY reply with the new file - no chat or extra text."
            },
            {
                "role": "user",
                "content": f"<gitlab-ci-file>{gitlab_ci}</gitlab-ci-file>\n\n<plan-of-action>{response.message}</plan-of-action>"
            }
        ]
        response = await model.chat(messages, model=openai_model, temperature=0.7, top_p=1.0)
    print(response.message)
    if args.show_useage:
        print(response.usage)
        total_cost += response.cost
        total_tokens += response.tokens

    if args.thorough:
        with yaspin(text="Getting a critique of the GitHub Actions file", color="yellow") as spinner:
            messages = [
                {
                    "role": "system",
                    "content": "Your MISSION is to help users who are converting their GitLab CI yaml files to a well documented GitHub Actions file. You will be presented with the original GitLab CI file and a converted GitHub Actions file.  You task is to critique the converted GitHub file, spot any errors and any areas for improvement and provide a critique for the user."
                },
                {
                    "role": "user",
                    "content": f"<gitlab-ci-file>{gitlab_ci}</gitlab-ci-file>\n\n<converted-github-action>{response.message}</converted-girhub-action>"
                }
            ]
            response = await model.chat(messages, model=openai_model, temperature=0.7, top_p=1.0)
        print(response.message)
        if args.show_useage:
            print(response.usage)
            total_cost += response.cost
            total_tokens += response.tokens

        with yaspin(text="Applying critique of GitHub Actions file", color="yellow") as spinner:
            messages = [
                {
                    "role": "system",
                    "content": "Your MISSION is to help users who are converting their GitLab CI yaml files to a well documented GitHub Actions file. You will be presented with the original GitLab CI file, a converted GitHub Actions file and a critique of the converstion.  You task is to take the critique of the converted file and apply any suggestions in it. You will be provided the original GitLab CI file, the converted GitHub Actions file and a critique of the converted file.  You MUST cover ALL of the things in the critique - do NOT BE LAZY. You should ONLY reply with the new file - no chat or extra text."
                },
                {
                    "role": "user",
                    "content": f"<gitlab-ci-file>{gitlab_ci}</gitlab-ci-file>\n\n<converted-github-action>{response.message}</converted-girhub-action>\n\n<critique>{response.message}</critique>"
                }
            ]
            response = await model.chat(messages, model=openai_model, temperature=0.7, top_p=1.0)
        print(response.message)
        if args.show_useage:
            print(response.usage)
            total_cost += response.cost
            total_tokens += response.tokens
            print(f"Total tokens: {total_tokens}")
            print(f"Total cost: ${total_cost}")

if __name__ == "__main__":
    # run the main function asynchronously
    asyncio.run(main())
