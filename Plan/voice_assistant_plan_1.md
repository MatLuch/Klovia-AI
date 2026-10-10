# Windows Voice Assistant: Two-Part Build Plan

## Goal

Build a brand-new Windows-only assistant that can hear a request, understand what the user means, perform actions on the computer, check the result, and speak back.

This is an independent software project. It has no ESP32, serial, TFT display, robotics hardware, or dependency on the previous hardware voice-assistant project.

The project has two deliberate stages:

1. **Pre-LLM:** build a reliable assistant with speech, a deterministic command router, and safe Windows tools.
2. **Post-LLM:** keep those same tools, but let a language model choose tools, handle natural language, remember context, and complete multi-step tasks.

The LLM should be the decision layer. Python remains the layer that actually controls Windows.

## Target stack

| Area | Technology | Purpose |
|---|---|---|
| Main language | Python 3.11 | Application logic and integrations |
| Microphone | `sounddevice` | Record microphone audio |
| Wake word | `openWakeWord` | Detect a phrase such as “Hey Jarvis” |
| Speech to text | `faster-whisper` | Convert speech into a transcript |
| Text to speech | `edge-tts` with `soundfile`/`sounddevice` | Natural spoken replies; keep `pyttsx3` as an offline fallback |
| Windows UI control | `pywinauto` with the UIA backend | Inspect and interact with supported Windows controls |
| Audio control | `pycaw` | Control master and application volume |
| Files | `pathlib`, `shutil`, `os` | Search and organize files |
| Processes | `subprocess`, `psutil` | Launch apps and inspect running processes |
| Browser | Playwright | Automate browser pages through a controlled browser |
| Interface | PySide6 | Tray icon, floating assistant panel, settings |
| Storage | SQLite through `sqlite3` | Preferences, routines, history, undo records |
| Validation | `pydantic` or dataclasses | Validate command arguments and tool results |
| Packaging | PyInstaller | Build a Windows executable |
| LLM layer, post-LLM | Gemini API with function calling | Choose tools and handle natural language |
| Optional local training | Transformers, PEFT/LoRA, TRL, Unsloth | Fine-tune a small model later |

## Recommended project layout

```text
voice_assistant/
├── app.py                    # starts the application
├── config.py                 # settings and environment variables
├── requirements.txt
├── .env.example
├── audio/
│   ├── microphone.py         # recording and silence detection
│   ├── wakeword.py           # wake-word detector
│   ├── stt.py                # faster-whisper wrapper
│   └── tts.py                # speech output and interruption
├── commands/
│   ├── models.py             # Command, Result, ConfirmationPolicy
│   ├── registry.py           # registered commands and aliases
│   ├── parser.py             # deterministic parser in Part 1
│   └── router.py             # deterministic router, then LLM router
├── tools/
│   ├── apps.py               # open, close, focus, list apps
│   ├── windows.py            # move, resize, minimize, maximize windows
│   ├── audio.py              # volume, mute, media controls
│   ├── files.py              # search, open, copy, move, rename
│   ├── browser.py            # browser actions through Playwright
│   ├── system.py             # battery, network, time, screenshots
│   └── clipboard.py          # read/write clipboard with permission rules
├── context/
│   ├── active_state.py       # active app, selection, recent actions
│   └── memory.py             # explicit saved preferences and routines
├── storage/
│   ├── database.py           # SQLite connection and migrations
│   └── audit.py              # action history and undo information
├── ui/
│   ├── tray.py               # system tray icon and menu
│   ├── panel.py              # transcript and status panel
│   └── settings.py           # microphone, voice, privacy, and API settings
├── llm/                      # empty until Part 2
│   ├── client.py
│   ├── schemas.py
│   ├── planner.py
│   └── prompts.py
└── tests/
    ├── test_parser.py
    ├── test_tools.py
    ├── test_safety.py
    └── test_end_to_end.py
```

# Part 1: Pre-LLM

The finish line for Part 1 is a useful assistant that responds to a fixed set of commands. It does not need an LLM. It uses command aliases, regular expressions, and validated arguments.

## Phase 1 — Define the first command set

Start with ten commands that are easy to test and useful every day:

1. “Open Chrome.”
2. “Open VS Code.”
3. “Close Chrome.”
4. “Turn the volume to 30 percent.”
5. “Mute the computer.”
6. “Play” or “pause.”
7. “Show my Downloads folder.”
8. “Find the PDF about robotics.”
9. “What is my battery level?”
10. “What is the weather in Richmond Hill?”

Write the expected result for each command before coding. For example, “turn the volume to 30 percent” must produce an integer between 0 and 100 and then verify the new volume.

Do not begin with every possible Windows feature. A small command set that works every time gives you a foundation for the harder agent later.

## Phase 2 — Build a typed command core

Before microphone input, make the assistant work from typed text. This removes audio problems while you build the actual computer-control system.

Create a common command model:

```python
CommandRequest(
    name="set_volume",
    arguments={"percent": 30},
    source="typed",
)
```

Every command should have:

- a canonical name;
- aliases such as `volume`, `sound`, and `louder`;
- a strict argument schema;
- a handler function;
- a human-readable success response;
- an error response;
- a confirmation policy;
- an undo method when possible.

Use a registry instead of a giant `if` statement. The registry makes the same tools reusable by the LLM later.

Example deterministic parsing rules:

```text
“open chrome”                       -> open_app(name="Chrome")
“set volume to 30 percent”         -> set_volume(percent=30)
“find pdf robotics in downloads”   -> find_files(folder="Downloads", extension=".pdf", query="robotics")
```

Normalize lowercase text, remove filler words, parse numbers carefully, and return an “I did not understand” result when the request is outside the supported set. Never use `eval()` to parse a spoken command.

## Phase 3 — Implement safe Windows tools

Build and test tools one at a time.

### App and process tools

- Maintain an allowlist mapping friendly names to executable paths.
- Launch programs with `subprocess.Popen` using an argument list.
- Check whether the process started.
- Close only the selected application process.
- Never let a spoken string become an unrestricted shell command.

### Audio tools

- Use `pycaw` for master and application volume.
- Support volume percentages from 0 to 100.
- Support mute and unmute.
- Add play/pause and next/previous media shortcuts.
- Read the resulting volume back after changing it.

### File tools

- Start with `Downloads`, `Documents`, and one user-selected project folder.
- Search by filename and extension.
- Open a file with the associated Windows application.
- Copy, move, rename, and delete only after a confirmation policy is in place.
- Store the original path for undo.
- Do not recursively scan the entire drive on every request.

### Window tools

- List visible windows.
- Focus, minimize, maximize, and close a window.
- Use `pywinauto` UI Automation when a control exposes a useful name or pattern.
- Add mouse/keyboard simulation only as a controlled fallback for apps that expose no usable UI controls.

### Browser tools

- Open a URL.
- Search through a controlled browser context.
- Read the page title and visible text.
- Keep logins and purchases outside the first version.

### Information tools

- Battery level through `psutil`.
- Current time through Python.
- Weather through the Open-Meteo integration you already use.
- Clipboard read/write only with a clear status indicator because clipboard contents may be private.

Each tool returns a structured result:

```python
ToolResult(
    ok=True,
    message="Volume set to 30 percent.",
    data={"percent": 30},
    undo_token=None,
)
```

## Phase 4 — Add the audio pipeline

Use this order so audio does not hide bugs in the command system:

1. Press a keyboard shortcut.
2. Record from the microphone at 16 kHz.
3. Stop when silence is detected or a maximum duration is reached.
4. Send the audio to `faster-whisper`.
5. Normalize the transcript.
6. Pass the transcript to the deterministic parser.
7. Execute the command.
8. Speak the response.

After that works, add `openWakeWord` to replace the keyboard shortcut. Keep the shortcut as a fallback for noisy rooms and debugging. Use a cooldown so one phrase cannot trigger multiple commands.

Implement the wake-word and speech modules specifically for this Windows project. Do not add serial, ESP32, TFT, or other hardware code to this repository.

## Phase 5 — Add state, interruption, and errors

Use a small state machine:

```text
IDLE -> LISTENING -> TRANSCRIBING -> EXECUTING -> SPEAKING -> IDLE
```

Add these behaviors:

- a visible stop button;
- speaking interruption when the user says “stop” or presses Escape;
- timeouts for microphone, STT, and tools;
- one retry for temporary failures;
- clear error speech;
- logs with timestamps, command name, duration, and success status;
- no logging of raw microphone audio by default.

Run microphone capture and speech output in worker threads or asynchronous tasks so the UI never freezes.

## Phase 6 — Build the interface

Use PySide6 for a small tray application.

The panel should show:

- microphone status;
- wake-word status;
- the latest transcript;
- the command being executed;
- the result;
- a stop button;
- a settings button;
- a way to disable wake-word listening.

Do not make the interface a chat app yet. Its job is to show what the assistant heard and what it did.

## Phase 7 — Add storage and safety rules

Use SQLite for:

- settings;
- favorite apps;
- saved routines;
- recent action summaries;
- undo records;
- user-approved permissions.

Use three action levels:

| Level | Examples | Behavior |
|---|---|---|
| Safe | Open an app, read battery, change volume | Execute immediately |
| Reversible | Move or rename a file, close an app | Show the action and keep an undo record |
| Sensitive | Delete files, send messages, buy something, shut down | Ask for confirmation every time |

The confirmation system must live in Python and remain active after the LLM is added.

## Phase 8 — Test Part 1

Create a fixed test list with at least:

- exact supported commands;
- different word orders;
- numbers such as 0, 1, 50, and 100;
- unknown app names;
- missing files;
- no microphone;
- noisy or empty transcripts;
- duplicate wake-word detections;
- interrupted speech;
- failed Windows actions;
- dangerous commands that must be blocked or confirmed.

Track three measurements:

1. **Parse accuracy:** did the transcript become the correct command and arguments?
2. **Execution success:** did Windows actually complete the action?
3. **Response latency:** how long from the end of speech to the result?

Part 1 is complete when the ten commands work from typed input and speech, every tool has error handling, dangerous actions have confirmation, and the tray app can run for a long session without freezing.

## Phase 9 — Package Part 1

- Put secrets and machine-specific paths in `.env` or Windows Credential Manager.
- Add a `requirements.txt` with pinned versions after the prototype is stable.
- Build with PyInstaller on Windows.
- Test on a clean Windows account or a second Windows machine.
- Add a startup shortcut only after shutdown and microphone permissions work.
- Keep a developer mode that shows logs and a normal mode that starts in the tray.

At this point you have a real deterministic voice assistant even if you never add an LLM.

# Part 2: Post-LLM

The finish line for Part 2 is an assistant that accepts natural language, chooses your existing tools, asks useful follow-up questions, completes several steps, and verifies its work.

## Phase 10 — Add an LLM behind an interface

Create a `Brain` interface so the rest of the app does not depend directly on Gemini:

```python
class Brain(Protocol):
    def respond(self, messages, tools) -> "BrainResponse": ...
```

Implement:

- `RuleBrain` for the deterministic parser;
- `GeminiBrain` for the API model;
- optionally `LocalBrain` for a local model later.

This lets you switch models without rewriting your Windows tools or UI.

## Phase 11 — Expose tools through function calling

Give the model only the tools it needs, with strict JSON schemas:

```json
{
  "name": "set_volume",
  "description": "Set Windows master volume.",
  "parameters": {
    "type": "object",
    "properties": {
      "percent": {"type": "integer", "minimum": 0, "maximum": 100}
    },
    "required": ["percent"]
  }
}
```

The loop is:

1. Send the transcript, short context, and available tool schemas to the model.
2. Receive either a normal answer or a tool call.
3. Validate the tool name and arguments locally.
4. Apply the confirmation policy locally.
5. Execute the existing Python tool.
6. Send the structured result back to the model.
7. Allow another tool call if the task needs one.
8. Stop after a small maximum number of steps.
9. Speak the final answer.

Function calling is the key connection between an LLM and real computer actions: the model proposes a function call, while your application validates and executes it. citeturn10search3

Never allow the model to output arbitrary PowerShell or Python and run it automatically. If you later add a terminal tool, run it in a restricted, visible, confirmation-controlled environment.

## Phase 12 — Add natural language and follow-up questions

Teach the model rules such as:

- ask one short question when a required argument is missing;
- use the current app and recent action as context;
- never guess a file when multiple matches exist;
- explain what it plans to do before a sensitive action;
- keep replies short for voice;
- say when a tool failed instead of claiming success.

Examples that should work after this phase:

- “Open the project I was working on yesterday.”
- “Make the volume a little quieter.”
- “Find the robotics PDF and put a copy on my desktop.”
- “Open VS Code, Chrome, and my project folder.”

## Phase 13 — Add context and memory

Separate three types of information:

1. **Turn context:** the current request and the last few tool results.
2. **Session context:** active window, selected text, current folder, and recent actions.
3. **Saved memory:** preferences or routines that the user explicitly asks the assistant to remember.

Do not send the entire computer history to the model. Build a small context object and redact secrets, passwords, private clipboard text, and unrelated file contents.

Add explicit commands such as:

- “Remember that my coding projects are in D:\\Projects.”
- “Forget that preference.”
- “What do you remember about my workspace?”

## Phase 14 — Add multi-step planning and verification

Represent a plan as a list of tool calls with checkpoints:

```text
1. Find the latest robotics PDF.
2. Confirm that exactly one matching file exists.
3. Copy it to the study folder.
4. Verify the destination exists.
5. Tell the user the final path.
```

Each step must return evidence. If a step fails, the assistant should stop, explain the failure, and offer a retry or undo. Add a maximum step count and a timeout so a bad plan cannot loop forever.

## Phase 15 — Add screen and browser understanding

Only use visual context when normal APIs are not enough.

- Prefer UI Automation for buttons, menus, and text controls.
- Prefer Playwright DOM information for websites.
- Capture a screenshot only when an app is visually structured but does not expose useful controls.
- Send only the necessary screenshot or selected region to a multimodal model.

Gemini supports image inputs as well as function calling, which makes a screenshot plus an action tool possible when you need it. citeturn10search0turn10search1

Keep a visible indicator whenever the assistant is reading the screen.

## Phase 16 — Add real-time information and integrations

Connect tools for:

- weather;
- web search;
- calendar;
- email drafts;
- music;
- school and project files stored on Windows;
- Windows music, calendar, web, and document integrations.

Use separate tool modules and permissions for each integration. A calendar read can be safe; creating an event or sending a message should be confirmed.

## Phase 17 — Evaluate the agent

Create an evaluation file with at least 100 utterances. Each case should include:

```json
{
  "utterance": "Find my latest robotics notes and open them",
  "expected_tools": ["find_files", "open_file"],
  "requires_confirmation": false,
  "success_condition": "The selected file is opened"
}
```

Measure:

- correct tool selection;
- correct arguments;
- successful execution;
- unnecessary confirmations;
- unsafe calls blocked;
- average response time;
- number of steps before completion;
- whether the final answer matches the actual tool result.

Test prompt injection too. A web page or document may contain instructions aimed at the assistant; treat page text as data, not as permission to run actions.

## Phase 18 — Optional local model and fine-tuning

Do this only after the API-based agent already works.

1. Log approved examples of transcript → tool calls → tool results.
2. Remove private data and incorrect traces.
3. Create a JSONL training set with tool schemas and correct calls.
4. Hold out a test set that the model never sees during training.
5. Fine-tune a small pretrained model with QLoRA.
6. Compare it against the API model using the same evaluation set.
7. Keep the safety and confirmation layer outside the model.

Your RTX A2000 with 8 GB VRAM is suitable for experimenting with a small 1–3B model using QLoRA. A 3B model is listed at about 3.5 GB as an absolute minimum in Unsloth’s table, but sequence length, batch size, and other overhead can increase actual usage. citeturn7view0

Use:

- `transformers` to load the model;
- `bitsandbytes` for 4-bit loading where supported;
- `peft` for LoRA adapters;
- `trl` for supervised fine-tuning;
- Unsloth if its Windows and GPU setup works cleanly for your chosen model.

Fine-tuning changes how the model chooses tools. It does not give the model Windows access by itself; Python still has to execute the tools.

## Suggested order of work

1. Typed deterministic commands.
2. Safe Windows tools.
3. Unit tests for parser and tools.
4. Microphone and speech recognition.
5. Text-to-speech and interruption.
6. Tray interface.
7. SQLite settings and undo records.
8. PyInstaller build.
9. LLM interface and function calling.
10. Follow-up questions and context.
11. Multi-step plans and verification.
12. Browser and screen understanding.
13. Evaluation set and safety tests.
14. Optional local model and fine-tuning.

## Definition of done

### Part 1

- Ten commands work from typed text and speech.
- Wake word and keyboard shortcut both work.
- The UI stays responsive during recording, transcription, and speech.
- Every tool returns structured success or failure data.
- Destructive actions require confirmation.
- File changes can be undone where practical.
- Logs and settings are stored safely.
- A Windows executable can be built and started from the tray.

### Part 2

- The LLM selects only registered tools.
- Tool arguments are validated before execution.
- The confirmation policy cannot be bypassed by the model.
- The assistant can ask follow-up questions.
- Multi-step tasks verify each result.
- Context is small, relevant, and privacy-aware.
- Screen access is visible.
- Evaluation tests measure real success instead of only fluent replies.
- A local fine-tuned model is optional and must beat a simple baseline before replacing it.

The main rule is: **build the tools first, then give the LLM permission to choose among those tools.** That makes the project testable, safer, and much easier to debug.

