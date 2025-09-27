#!/usr/bin/env python3
import os
import sys
import textwrap
import subprocess  # import at top

# Optional keyring for secure API key storage
try:
    import keyring
except ImportError:
    keyring = None

# OpenAI SDK
try:
    from openai import OpenAI
except ImportError:
    print("ERROR: openai package not installed. Install with pip or pipx.")
    sys.exit(1)


def get_api_key() -> str | None:
    """Retrieve OpenAI API key securely from keyring or environment variable."""
    if keyring is not None:
        try:
            secret = keyring.get_password("openai", "api_key")
            if secret:
                return secret.strip()
        except Exception:
            pass
    # Fallback to environment variable
    secret = os.environ.get("OPENAI_API_KEY")
    if secret:
        return secret.strip()
    return None


def nl_to_command(user_query: str, api_key: str) -> str:
    """Call OpenAI to generate a terminal command with 3-line simulation."""
    client = OpenAI(api_key=api_key)
    prompt = textwrap.dedent("""\
        You are a Natural Language to Terminal Command Translator and Simulator.
        Rules:
        1. Respond in EXACTLY 3 lines.
        2. Line 1: Execute "COMMAND"? [y/N] y
        3. Line 2: $COMMAND
        4. Line 3: A short, realistic, typical output of that command on Linux/macOS.
        5. Only generate ONE safe, idiomatic command.
    """)
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # cheapest OpenAI model
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_query}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()


def main():
    if len(sys.argv) < 2:
        print('Usage: ask "your natural language question"')
        sys.exit(1)

    api_key = get_api_key()
    if not api_key:
        print(
            "ERROR: No API key found. Store one with:\n"
            "  python -m keyring set openai api_key\n"
            "or set OPENAI_API_KEY environment variable."
        )
        sys.exit(1)

    # Combine all CLI arguments as the query
    query = " ".join(sys.argv[1:])

    try:
        result = nl_to_command(query, api_key)
    except Exception as e:
        print("ERROR: failed to call OpenAI API:", str(e))
        sys.exit(1)

    # Print simulated 3-line output
    print(result)

    # Optional real execution
    lines = result.splitlines()
    if len(lines) >= 2 and lines[1].startswith("$ "):
        command_to_run = lines[1][2:]
        answer = input(f'Execute "{command_to_run}" for real? [y/N] ')
        if answer.lower() == 'y':
            subprocess.run(command_to_run, shell=True)


if __name__ == "__main__":
    main()
