"""
Package Creator
Creates setup instructions and file structure templates
"""

from pathlib import Path
from typing import Dict, Any

class PackageCreator:
    """Creates setup package components"""

    def create_setup_instructions(self, meta_answers: Dict[str, Any]) -> str:
        """Generate setup-instructions.md content"""

        use_case = meta_answers.get('use_case', 'general')
        maintenance = meta_answers.get('maintenance', 'weekly')

        instructions = f"""# Setup Instructions: Implementing Your AI-Brain Integration

## Overview

You've downloaded a customized setup package for creating a persistent AI memory system tailored for **{use_case}** use case.

This guide will walk you through implementation.

---

## What You'll Create

```
.memory/
├── 1-core/
│   └── core-identity.md          (Your questionnaire answers)
├── 2-active/
│   └── active-projects.md        (Your current projects)
├── knowledge-base/
│   ├── [domain-specific files]
└── session-logs/
    └── [timestamped session records]
```

---

## Step 1: Answer the Questionnaire

1. Open `questionnaire.md` from this package
2. Answer all questions thoughtfully
3. Keep your answers - you'll use them in Step 3

---

## Step 2: Create File Structure

Choose a location for your `.memory/` folder:
- Recommended: `~/projects/.memory/` or `~/.memory/`

Create the folder structure:

```bash
mkdir -p ~/.memory/{{1-core,2-active,knowledge-base,session-logs}}
```

---

## Step 3: Create core-identity.md

1. Create file: `~/.memory/1-core/core-identity.md`
2. Add YAML frontmatter:

```yaml
---
tier: 1
category: core
tags:
  - tier1
  - identity
  - profile
created: {self._get_date()}
updated: {self._get_date()}
---
```

3. Add sections based on your questionnaire answers:

```markdown
# Core Identity Profile

**Last updated:** {self._get_date()}

---

## Cognitive Profile

[Your answers to cognitive profile questions]

## Career Context

[Your answers to career questions]

## Communication Preferences

[Your answers to communication questions]

[Continue for all sections...]
```

---

## Step 4: Set Up Claude Code Startup Hook

1. Open Claude Code settings
2. Navigate to: Settings > Hooks > Startup
3. Add this command:

```bash
cat ~/.memory/1-core/core-identity.md
```

Or use the provided `startup-hook-example.sh` file.

---

## Step 5: Create Slash Commands (Optional)

See the `examples/slash-commands/` folder for:
- `/log` - Create session logs
- `/extract` - Extract knowledge from sessions
- `/context` - Load additional context on demand

---

## Step 6: Test Your Setup

1. Start a new Claude Code session
2. Verify your core identity loads automatically
3. Test slash commands (if configured)
4. Create your first session log

---

## Maintenance Schedule

Based on your preference: **{maintenance} updates**

Recommended workflow:
1. Work on projects
2. At interval, use `/log` to capture session learnings
3. Use `/extract` to update knowledge base
4. Review and refine core identity {maintenance}

---

## Troubleshooting

**Issue:** Core identity doesn't load
- Check file path in startup hook
- Verify .memory folder location
- Ensure core-identity.md exists

**Issue:** Slash commands don't work
- Verify commands are in `.claude/commands/` folder
- Check file permissions
- Restart Claude Code

---

## Next Steps

1. Answer the questionnaire
2. Create your core-identity.md file
3. Set up startup hook
4. Start using your AI-brain integration!

**Questions?** See README.md or refer to documentation.
"""
        return instructions

    def create_file_structure(self) -> Dict[str, str]:
        """Create empty file structure templates"""
        structure = {
            '1-core/core-identity.md': self._core_identity_template(),
            '2-active/active-projects.md': self._active_projects_template(),
            'knowledge-base/README.md': self._knowledge_base_readme(),
            'session-logs/README.md': self._session_logs_readme(),
        }
        return structure

    def create_startup_hook(self) -> str:
        """Generate startup-hook-example.sh"""
        return """#!/bin/bash
# Startup hook for AI-brain integration
# Add to Claude Code settings: Settings > Hooks > Startup

cat ~/.memory/1-core/core-identity.md
cat ~/.memory/2-active/active-projects.md

# Optional: Load specific knowledge base files
# cat ~/.memory/knowledge-base/devops-learnings.md
"""

    def _get_date(self) -> str:
        """Get current date in YYYY-MM-DD format"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")

    def _core_identity_template(self) -> str:
        return """---
tier: 1
category: core
tags:
  - tier1
  - identity
  - profile
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Core Identity Profile

**Last updated:** YYYY-MM-DD

---

[Fill in with your questionnaire answers]
"""

    def _active_projects_template(self) -> str:
        return """---
tier: 2
category: active
tags:
  - tier2
  - projects
  - current-focus
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Active Projects & Current Focus

**Last updated:** YYYY-MM-DD

---

## Current Active Projects

[Add your projects here]
"""

    def _knowledge_base_readme(self) -> str:
        return """# Knowledge Base

This folder contains domain-specific knowledge extracted from sessions.

## Suggested Files

- `technical-skills.md` - Technologies, tools, languages
- `career-insights.md` - Career development learnings
- `decisions-log.md` - Important decisions and their rationale
- `resources.md` - Useful resources, links, references
"""

    def _session_logs_readme(self) -> str:
        return """# Session Logs

This folder contains timestamped records of work sessions.

## Naming Convention

`YYYY-MM-DD_session-N.md` - e.g., `2025-11-18_session-1.md`

## Template

```markdown
# Session Log: [Date]

## What I Worked On
- [Task 1]
- [Task 2]

## Key Learnings
- [Learning 1]

## Decisions Made
- [Decision 1]

## Next Steps
- [Next action]
```
"""
