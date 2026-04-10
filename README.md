# Frontend Slides (ppt-clouder)

A Claude Code skill for creating stunning, animation-rich HTML presentations — from scratch or by converting PowerPoint files.

## What This Does

**Frontend Slides** helps non-designers create beautiful web presentations without knowing CSS or JavaScript. It uses a "show, don't tell" approach: instead of asking you to describe your aesthetic preferences in words, it generates visual previews and lets you pick what you like.

### Key Features

- **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools, no frameworks.
- **Visual Style Discovery** — Can't articulate design preferences? No problem. Pick from generated visual previews.
- **Web Search Integration** — Automatic content research using 智谱AI search for rich, sourced material.
- **Project Organization** — Automatic directory structure with `public/` for images, `final/` for output, and `websearch.md` for research tracking.
- **PPT Conversion** — Convert existing PowerPoint files to web, preserving all images and content.
- **Anti-AI-Slop** — Curated distinctive styles that avoid generic AI aesthetics (bye-bye, purple gradients on white).
- **Production Quality** — Accessible, responsive, well-commented code you can customize.

## Project Structure

Each presentation is organized as:

```
my-presentation/
├── websearch.md          # Auto-generated search results and sources
├── public/               # Your images go here
│   ├── slide-01-bg.jpg
│   └── chart-data.png
├── final/                # Final output
│   └── index.html        # Complete presentation
└── .claude-design/       # Temporary preview files
    └── slide-previews/
```

## Installation

### For Claude Code Users

Copy the skill files to your Claude Code skills directory:

```bash
# Create the skill directory
mkdir -p ~/.claude/skills/ppt-clouder/scripts

# Copy all files (or clone this repo directly)
cp SKILL.md STYLE_PRESETS.md viewport-base.css html-template.md animation-patterns.md ~/.claude/skills/ppt-clouder/
cp scripts/extract-pptx.py scripts/web_search.py ~/.claude/skills/ppt-clouder/scripts/
```

Or clone directly:

```bash
git clone https://github.com/zarazhangrui/frontend-slides.git ~/.claude/skills/ppt-clouder
```

Then use it by typing `/ppt-clouder` in Claude Code.

## Usage

### Create a New Presentation

```
/ppt-clouder

> "I want to create a pitch deck for my AI startup"
```

The skill will:
1. Ask about your content (slides, messages, images)
2. Ask about the feeling you want (impressed? excited? calm?)
3. Generate 3 visual style previews for you to compare
4. Create the full presentation in your chosen style
5. Organize files in `public/`, `final/`, and `websearch.md`
6. Open it in your browser

### Using Your Own Images

When a slide needs images:
1. Place your image in the `public/` folder
2. Tell the skill the filename (e.g., "slide-02-bg.jpg")
3. The skill will reference it in the presentation

### Convert a PowerPoint

```
/ppt-clouder

> "Convert my presentation.pptx to a web slideshow"
```

The skill will:
1. Extract all text, images, and notes from your PPT
2. Save images to `public/` folder
3. Show you the extracted content for confirmation
4. Let you pick a visual style
5. Generate an HTML presentation with all your original assets in `final/`

## Included Styles

### Dark Themes
- **Bold Signal** — Confident, high-impact, vibrant card on dark
- **Electric Studio** — Clean, professional, split-panel
- **Creative Voltage** — Energetic, retro-modern, electric blue + neon
- **Dark Botanical** — Elegant, sophisticated, warm accents

### Light Themes
- **Notebook Tabs** — Editorial, organized, paper with colorful tabs
- **Pastel Geometry** — Friendly, approachable, vertical pills
- **Split Pastel** — Playful, modern, two-color vertical split
- **Vintage Editorial** — Witty, personality-driven, geometric shapes

### Specialty
- **Neon Cyber** — Futuristic, particle backgrounds, neon glow
- **Terminal Green** — Developer-focused, hacker aesthetic
- **Swiss Modern** — Minimal, Bauhaus-inspired, geometric
- **Paper & Ink** — Literary, drop caps, pull quotes

## Architecture

This skill uses **progressive disclosure** — the main `SKILL.md` is a concise map (~180 lines), with supporting files loaded on-demand only when needed:

| File | Purpose | Loaded When |
|------|---------|-------------|
| `SKILL.md` | Core workflow and rules | Always (skill invocation) |
| `STYLE_PRESETS.md` | 12 curated visual presets | Phase 2 (style selection) |
| `viewport-base.css` | Mandatory responsive CSS | Phase 3 (generation) |
| `html-template.md` | HTML structure and JS features | Phase 3 (generation) |
| `animation-patterns.md` | CSS/JS animation reference | Phase 3 (generation) |
| `scripts/extract-pptx.py` | PPT content extraction | Phase 4 (conversion) |
| `scripts/web_search.py` | 智谱AI web search | Phase 1.5 & Phase 3.0a |
| `templates/websearch.md.template` | Search record template | Project initialization |

This design follows [OpenAI's harness engineering](https://openai.com/index/harness-engineering/) principle: "give the agent a map, not a 1,000-page instruction manual."

## Environment Setup

### Web Search Feature (Optional)

For automatic content research:

1. **Get API Key**: https://open.bigmodel.cn/usercenter/apikeys
2. **Set environment variable**:
   ```bash
   export ZHIPU_API_KEY='your-api-key-here'
   ```
3. **Or create .env file**:
   ```bash
   echo 'ZHIPU_API_KEY=your-api-key-here' > ~/.claude/skills/ppt-clouder/.env
   ```

## Philosophy

This skill was born from the belief that:

1. **You don't need to be a designer to make beautiful things.** You just need to react to what you see.

2. **Dependencies are debt.** A single HTML file will work in 10 years. A React project from 2019? Good luck.

3. **Generic is forgettable.** Every presentation should feel custom-crafted, not template-generated.

4. **Comments are kindness.** Code should explain itself to future-you (or anyone else who opens it).

5. **Organization matters.** Clear directory structures (`public/`, `final/`, `websearch.md`) make projects maintainable.

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI
- For PPT conversion: Python with `python-pptx` library
- For web search: 智谱AI API key (optional)

## Credits

Created by [@zarazhangrui](https://github.com/zarazhangrui) with Claude Code.

Inspired by the "Vibe Coding" philosophy — building beautiful things without being a traditional software engineer.

## License

MIT — Use it, modify it, share it.
