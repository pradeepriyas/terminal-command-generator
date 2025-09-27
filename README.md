
# CommandGenerator

**Natural Language → Terminal Command Translator and Simulator**

Convert plain English instructions into Linux/macOS terminal commands and optionally execute them safely. Supports OpenAI API integration with secure key storage.

---

## Features

- Translate natural language into safe, idiomatic shell commands
- Outputs a 3-line simulation:
  - Command suggestion with simulated confirmation
  - Command as it would appear in the terminal
  - Example realistic output
- Optional real execution of commands with user confirmation
- Securely uses OpenAI API keys via keyring or environment variable
- Works in Python venv or via pipx for easy setup

---

## Installation

1. **Clone the repository**
	```bash
	git clone https://github.com/yourusername/commandgenerator.git
	cd commandgenerator
	```

2. **Create a Python virtual environment**
	```bash
	python3 -m venv ~/askenv
	source ~/askenv/bin/activate
	pip install openai keyring
	```

3. **Store OpenAI API key securely**
	```bash
	python -m keyring set openai api_key
	# Paste your API key when prompted
	```

---

## Usage

### 1. Directly with Python
```bash
python commandgenerator.py "how do I check diskspace"
```

### 2. Optional: Create a CLI shortcut
```bash
mkdir -p ~/bin
nano ~/bin/ask
```
Paste the following into `~/bin/ask`:
```bash
#!/usr/bin/env bash
~/askenv/bin/python ~/commandgenerator.py "$@"
```
Make it executable:
```bash
chmod +x ~/bin/ask
```
Add to PATH if necessary:
```bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```
Then run:
```bash
ask "list all files in this folder"
```

---

## Output Example

```
--- Command Suggestion ---
Execute "ls -l"? [y/N] y
$ ls -l

--- Real Output ---
total 16
-rw-r--r-- 1 user group 887 README.md
drwxr-xr-x 3 user group  96 Documents
```

*First part shows simulation. Second part runs the command for real if confirmed.*

---

## Security

- OpenAI API key is stored securely via keyring
- Optionally falls back to environment variable:
  ```bash
  export OPENAI_API_KEY="your_api_key_here"
  ```
- Commands are safe by default; real execution is opt-in

---

## Contributing

1. Fork the repository
2. Create a new branch:
	```bash
	git checkout -b feature-name
	```
3. Commit your changes:
	```bash
	git commit -m "Add new feature"
	```
4. Push:
	```bash
	git push origin feature-name
	```
5. Open a Pull Request