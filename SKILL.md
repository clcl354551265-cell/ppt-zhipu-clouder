---
name: ppt-clouder
description: Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch. Helps non-designers discover their aesthetic through visual exploration rather than abstract choices. Features include intelligent web search for content research, self-evolving memory system, and slide-by-slide design verification.
---

# PPT-Clouder

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser.

## Key Features

1. **Visual Style Discovery** — Preview-based aesthetic selection, not abstract choices
2. **Web Search Integration** — Automatically research and generate content using 智谱AI search (optional)
3. **Self-Evolving Memory** — Learns user preferences and optimizes recommendations over time
4. **Slide-by-Slide Verification** — Review each slide before final assembly
5. **PPT Conversion** — Convert existing PowerPoint files to HTML

## Core Principles

1. **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Show, Don't Tell** — Generate visual previews, not abstract choices. People discover what they want by seeing it.
3. **Distinctive Design** — No generic "AI slop." Every presentation must feel custom-crafted.
4. **Viewport Fitting (NON-NEGOTIABLE)** — Every slide MUST fit exactly within 100vh. No scrolling within slides, ever. Content overflows? Split into multiple slides.
5. **Slide-by-Slide Verification (NON-NEGOTIABLE)** — You MUST ask user preferences for EACH slide before generating it. NEVER generate multiple slides at once. NEVER skip the verification loop.

## Design Aesthetics

You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight.

Focus on:
- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.
- Motion: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic.
- **Background Images**: Use strategically to add visual impact and context. Always include a semi-transparent overlay to ensure text readability. See "Background Image Pattern" section below.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Cliched color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. You still tend to converge on common choices (Space Grotesk, for example) across generations. Avoid this: it is critical that you think outside the box!

## Viewport Fitting Rules

These invariants apply to EVERY slide in EVERY presentation:

- Every `.slide` must have `height: 100vh; height: 100dvh; overflow: hidden;`
- ALL font sizes and spacing must use `clamp(min, preferred, max)` — never fixed px/rem
- Content containers need `max-height` constraints
- Images: `max-height: min(50vh, 400px)`
- Breakpoints required for heights: 700px, 600px, 500px
- Include `prefers-reduced-motion` support

**When generating, read `viewport-base.css` and include its full contents in every presentation.**

### Content Density Limits Per Slide

| Slide Type | Maximum Content |
|------------|-----------------|
| Title slide | 1 heading + 1 subtitle + optional tagline |
| Content slide | 1 heading + 4-6 bullet points OR 1 heading + 2 paragraphs |
| Feature grid | 1 heading + 6 cards maximum (2x3 or 3x2) |
| Code slide | 1 heading + 8-10 lines of code |
| Quote slide | 1 quote (max 3 lines) + attribution |
| Image slide | 1 heading + 1 image (max 60vh height) |

**Content exceeds limits? Split into multiple slides. Never cram, never scroll.**

---

## Background Image Pattern

When using background images to enhance visual impact:

### When to Use
- Title slides for strong first impressions
- Contextual slides (e.g., Wall Street theme for finance content)
- Transition slides between major sections
- Emotional or story-driven moments

### Implementation Pattern

```css
/* 1. Create a unique class for the slide */
.slide.slide-themed {
    background-color: #0d0d1a; /* Fallback color matching image tone */
    background-image: url('../public/background.jpg'); /* User image from public/ */
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
}

/* 2. REQUIRED: Add overlay for text readability */
.slide-themed::before {
    content: '';
    position: absolute;
    top: 0; right: 0; bottom: 0; left: 0;
    /* Gradient overlay - adjust opacity based on image darkness */
    background: linear-gradient(
        to bottom, 
        rgba(13, 13, 26, 0.3), 
        rgba(13, 13, 26, 0.7)
    );
    z-index: 0;
}

/* 3. Ensure content sits above overlay */
.slide-themed .slide-content {
    position: relative;
    z-index: 1;
}
```

### Best Practices

1. **Always use overlay**: Never place text directly on a photo without a semi-transparent layer
2. **Match fallback color**: Set `background-color` to a color extracted from the image
3. **Optimize images**: Keep background images under 500KB when possible
4. **Path handling**: 
   - User images from `public/`: `url('../public/background.jpg')` or `url('../public/slide-05-bg.jpg')`
   - External URLs: `url('https://example.com/image.jpg')`
5. **Contrast check**: Ensure text has sufficient contrast (WCAG AA minimum)
6. **Animation compatibility**: Background slides work well with `.reveal` animations

### Variations

```css
/* Dark image with subtle overlay */
.overlay-subtle::before {
    background: rgba(0, 0, 0, 0.4);
}

/* Gradient overlay for visual interest */
.overlay-gradient::before {
    background: linear-gradient(
        135deg,
        rgba(255, 107, 53, 0.2),
        rgba(0, 0, 0, 0.6)
    );
}

/* Vignette effect - darkens edges */
.overlay-vignette::before {
    background: radial-gradient(
        ellipse at center,
        transparent 0%,
        rgba(0, 0, 0, 0.6) 100%
    );
}
```

## Project Directory Structure

每个演示文稿项目遵循以下目录结构：

```
project-name/
├── websearch.md          # 网络搜索结果记录（自动更新）
├── public/               # 用户提供的图片资源
│   ├── slide-01-bg.jpg
│   ├── chart-data.png
│   └── ...
├── final/                # 最终生成的演示文稿
│   ├── index.html        # 主演示文件
│   └── assets/           # 演示文稿内嵌资源
└── .claude-design/       # 设计预览文件（临时）
    └── slide-previews/
```

**目录说明：**
- `websearch.md`: 自动记录所有搜索内容、来源和关键信息
- `public/`: 存放用户提供的图片，按用户指定的文件名引用
- `final/`: 最终交付的演示文稿，包含完整的 HTML 文件
- `.claude-design/`: 临时预览文件，生成完成后可清理

Determine what the user wants:

- **Mode A: New Presentation** — Create from scratch. Go to Phase 1.
- **Mode B: PPT Conversion** — Convert a .pptx file. Go to Phase 4.
- **Mode C: Enhancement** — Improve an existing HTML presentation. Read it, understand it, enhance.

---

## Phase 0.5: Load Evolution Memory

**ALWAYS READ FIRST**: Check the self-evolving memory system at:
`/Users/mac/.claude/projects/-Users-mac--claude/memory/frontend-slides-runtime-log.md`

### What to Look For

1. **User Profile** — Has this user generated presentations before? What are their preferences?
2. **Smart Recommendations** — Are there context-based recommendations for this topic?
3. **Layout Weights** — Which layouts have high success rates?
4. **Failure Patterns** — Any known issues to avoid?
5. **Quick Decision Paths** — Can we use a fast-track mode?

### Apply Learned Insights

If user has history:
- Pre-populate style preferences
- Prioritize previously successful layouts
- Skip verification for trusted patterns
- Warn about historically problematic choices

If new user:
- Use default weights
- Start building their profile
- Follow full questionnaire flow

---

## Phase 1: Content Discovery (New Presentations)

Ask via AskUserQuestion (can combine up to 4 questions per call):

**Question 1 — Purpose** (header: "Purpose"):
What is this presentation for? Options: Pitch deck / Teaching-Tutorial / Conference talk / Internal presentation

**Question 2 — Length** (header: "Length"):
Approximately how many slides? Options: Short 5-10 / Medium 10-20 / Long 20+

**Question 3 — Content** (header: "Content"):
Do you have content ready? Options: All content ready / Rough notes / Topic only / Need help researching

**Question 4 — Content Research** (header: "Research", only if "Need help researching" selected):
Enable web search to find content? Options:
- **Yes, search for every slide** — Auto-search content for each slide
- **Yes, but ask per slide** — Decide slide-by-slide
- **No, I'll provide all content** — Skip web search

If user has content, ask them to share it.

---

## Phase 1.5: Web Search Configuration (Optional)

If web search is enabled:

**Configure default search parameters:**

| Parameter | Description | Default |
|-----------|-------------|---------|
| **Search Engine** | `search_pro` (recommended), `search_pro_sogou`, `search_std` | `search_pro` |
| **Content Size** | `high` (detailed), `medium` (brief) | `high` |
| **Recency Filter** | `oneDay`, `oneWeek`, `oneMonth`, `oneYear`, `noLimit` | `noLimit` |

**Environment Setup Check:**
```bash
# Verify ZHIPU_API_KEY is set
export ZHIPU_API_KEY='your-api-key'
```
Get API key: https://open.bigmodel.cn/usercenter/apikeys

---

## Phase 2: Style Discovery

**This is the "show, don't tell" phase.** Most people can't articulate design preferences in words.

### Step 2.0: Style Path

Ask how they want to choose (header: "Style"):
- "Show me options" (recommended) — Generate 3 previews based on mood
- "I know what I want" — Pick from preset list directly

**If direct selection:** Show preset picker and skip to Phase 3. Available presets are defined in [STYLE_PRESETS.md](STYLE_PRESETS.md).

### Step 2.1: Mood Selection (Guided Discovery)

Ask (header: "Vibe", multiSelect: true, max 2):
What feeling should the audience have? Options:
- Impressed/Confident — Professional, trustworthy
- Excited/Energized — Innovative, bold
- Calm/Focused — Clear, thoughtful
- Inspired/Moved — Emotional, memorable

### Step 2.2: Generate 3 Style Previews

Based on mood, generate 3 distinct single-slide HTML previews showing typography, colors, animation, and overall aesthetic. Read [STYLE_PRESETS.md](STYLE_PRESETS.md) for available presets and their specifications.

| Mood | Suggested Presets |
|------|-------------------|
| Impressed/Confident | Bold Signal, Electric Studio, Dark Botanical |
| Excited/Energized | Creative Voltage, Neon Cyber, Split Pastel |
| Calm/Focused | Notebook Tabs, Paper & Ink, Swiss Modern |
| Inspired/Moved | Dark Botanical, Vintage Editorial, Pastel Geometry |

Save previews to `.claude-design/slide-previews/` (style-a.html, style-b.html, style-c.html). Each should be self-contained, ~50-100 lines, showing one animated title slide.

Open each preview automatically for the user.

### Step 2.3: User Picks

Ask (header: "Style"):
Which style preview do you prefer? Options: Style A: [Name] / Style B: [Name] / Style C: [Name] / Mix elements

If "Mix elements", ask for specifics.

---

## Phase 3: Generate Presentation

Generate the full presentation using content from Phase 1 and style from Phase 2.

**Before generating, read these supporting files:**
- [html-template.md](html-template.md) — HTML architecture and JS features
- [viewport-base.css](viewport-base.css) — Mandatory CSS (include in full)
- [animation-patterns.md](animation-patterns.md) — Animation reference for the chosen feeling

### Step 3.0: Slide-by-Slide Design Questionnaire

For **each slide**, you MUST ask the user about their preferences before generating. Use AskUserQuestion to collect:

**Question 1 — Charts** (header: "Charts"):
Does this slide need charts? Options: Yes / No

**Question 2 — Images** (header: "Images"):
Does this slide need images? Options: Yes / No

**Question 2a — Image Filename** (header: "ImageFile", only if "Yes" selected):
What is the image filename? (Place your image in the `public/` folder and provide the filename, e.g., "slide-02-bg.jpg")

**Question 3 — Layout** (header: "Layout"):
Which layout style? Options:
- **Centered** — Content centered vertically and horizontally, ideal for title/quote slides
- **Split** — Two-column layout (text + visual), ideal for feature comparisons
- **Grid** — Card-based grid layout, ideal for showcasing multiple items
- **Asymmetric** — Offset/dynamic composition, ideal for visual interest and storytelling

**Question 4 — Special Elements** (header: "Extras", multiSelect: true):
Any special elements? Options:
- Code block
- Data visualization
- Quote/callout
- Timeline/progress
- Icons
- None

**Question 5 — Content Source** (header: "Content"):
How to get slide content? Options:
- **I'll provide the content** — User writes or pastes content
- **Search online for relevant information** — Use web search to find and summarize content

---

### Step 3.0a: Web Search Configuration (If Selected)

If user chooses "Search online for relevant information":

**First, confirm search parameters via AskUserQuestion:**

**Question 1 — Search Scope** (header: "Search"):
What to search for this slide? (Provide keywords or topic)

**Question 2 — Time Range** (header: "Time"):
How recent should the information be? Options: Latest news (oneDay) / Recent (oneWeek) / Past month / Past year / No limit

**Question 3 — Search Depth** (header: "Depth"):
How detailed? Options: Brief summary / Detailed analysis with data

**Execute Search:**

```bash
/Users/mac/.claude/skills/ppt-clouder/scripts/web_search.py "[slide_topic]" --engine search_pro --recency [time_range] --content-size [high/medium]
```

Or using the venv Python directly:

```bash
/Users/mac/.claude/skills/ppt-clouder/.venv/bin/python scripts/web_search.py "[slide_topic]" --engine search_pro --recency [time_range]
```

**Process Results:**
1. Extract key points from search results
2. Organize into bullet points or paragraphs suitable for slides
3. Include source citations if using quotes or data
4. **Append to `websearch.md`**: Record search query, results summary, and sources
5. Present summarized content to user for approval

**Update `websearch.md` format:**
```markdown
### 搜索 #[N] - [Slide Type]
**时间**: [timestamp]
**关键词**: [query]
**结果摘要**: [key points]
**来源**: [source list]
```

**User Review:**
Ask (header: "Content"):
Is this searched content suitable? Options: Yes, use it / No, search again with different keywords / No, I'll write my own

If user approves, use the searched content. If not, repeat search with adjusted parameters or let user provide content.

---

### ⚠️ CRITICAL: Strict Execution Rule

**YOU MUST NOT skip the slide-by-slide questionnaire.** 

**Violations of this rule include:**
- Generating multiple slides at once without per-slide user approval
- Assuming user preferences based on previous slides
- Auto-generating content without asking content source for each slide
- Skipping the verification loop and proceeding to next slide without explicit user confirmation

**Consequences of violations:**
- User dissatisfaction with final presentation
- Wasted time regenerating entire presentation
- Loss of trust in the process

**If you catch yourself about to generate multiple slides:**
1. STOP immediately
2. Return to Step 3.0 for the current slide
3. Ask the user for their preferences
4. Generate ONLY that slide
5. Wait for explicit approval before proceeding

---

### Step 3.1: Generate Single Slide Preview

Based on the user's answers:
1. Generate **ONLY the current slide** as a standalone preview
2. **DO NOT** generate any other slides
2. Save to `.claude-design/slide-previews/slide-{N}-preview.html`
3. If using user images, reference them from `public/` folder: `url('../public/[filename]')`
4. Open the preview for user review

### Step 3.2: User Verification Loop

Ask (header: "Verification"):
Is this slide satisfactory? Options: Yes, proceed to next / No, modify layout / No, modify content / No, modify style

**If user selects any "No" option:**
- Ask follow-up questions about what needs to change
- Return to Step 3.0 with adjusted preferences
- Regenerate the slide preview

**Repeat until user approves**, then proceed to the next slide.

### Step 3.3: Assemble Final Presentation

Once all slides are approved:
1. **Create directories**: `mkdir -p public final`
2. **Copy websearch.md template**: `cp /Users/mac/.claude/skills/ppt-clouder/templates/websearch.md.template ./websearch.md`
3. Combine all approved slide HTML into a single file
4. Save to `final/index.html`
5. Include the FULL contents of viewport-base.css in the `<style>` block
6. Use fonts from Fontshare or Google Fonts — never system fonts
7. Add detailed comments explaining each section
8. Every section needs a clear `/* === SECTION NAME === */` comment block

**Image paths in final HTML:**
```css
/* Reference user images from public/ folder */
background-image: url('../public/slide-01-bg.jpg');
```

**Key requirements:**
- Single self-contained HTML file in `final/`, all CSS/JS inline
- All animations from approved previews preserved
- Navigation and keyboard controls working

---

## Phase 4: PPT Conversion

When converting PowerPoint files:

1. **Create directories**: `mkdir -p public final`
2. **Extract content** — Run `python scripts/extract-pptx.py <input.pptx> <output_dir>` (install python-pptx if needed: `pip install python-pptx`)
3. **Extract images**: Save PPT images to `public/` folder with original filenames
4. **Confirm with user** — Present extracted slide titles, content summaries, and image counts
5. **Style selection** — Proceed to Phase 2 for style discovery
6. **Generate HTML** — Convert to chosen style, preserving all text, images (reference from `public/`), slide order, and speaker notes (as HTML comments)

---

## Phase 5: Delivery

1. **Create directory structure**: Ensure `public/` and `final/` folders exist
2. **Assemble final presentation**: Save to `final/index.html`
3. **Update websearch.md**: Finalize with timestamp and summary
4. **Clean up**: Delete `.claude-design/slide-previews/` if it exists
5. **Open**: Use `open final/index.html` to launch in browser
6. **Summarize**: Tell the user:
   - File location: `final/index.html`
   - Images location: `public/` folder
   - Search records: `websearch.md`
   - Navigation: Arrow keys, Space, scroll/swipe, click nav dots
   - How to customize: `:root` CSS variables for colors, font link for typography, `.reveal` class for animations

---

## Phase 6: Update Files

### 6.1 Update Evolution Memory

**CRITICAL**: After every presentation, update the self-evolving memory system.

### 6.2 Update websearch.md

**Append final summary to `websearch.md`:**

```markdown
---

## 演示文稿完成摘要

- **主题**: [主题名称]
- **完成时间**: [timestamp]
- **总页数**: N
- **使用风格**: [风格名]
- **搜索次数**: N
- **最终文件**: `final/index.html`
```

### Update Checklist

```markdown
1. **User Profile Update**
   - [ ] 如果是新用户，创建画像
   - [ ] 更新最后活跃时间
   - [ ] 累计生成次数 +1

2. **Preference Learning**
   - [ ] 记录最终选择的风格
   - [ ] 记录每页的布局选择
   - [ ] 记录图表/图片使用频率
   - [ ] 计算平均验证轮数

3. **Success Tracking**
   - [ ] 标记哪些推荐被接受
   - [ ] 标记哪些需要修改
   - [ ] 更新布局成功率统计
   - [ ] 更新风格满意度

4. **Pattern Detection**
   - [ ] 检查是否触发新模式
   - [ ] 检查偏好冲突
   - [ ] 识别失败模式

6. **Web Search Tracking** (if used)
   - [ ] 记录搜索次数
   - [ ] 记录搜索成功率
   - [ ] 记录用户对搜索内容的满意度
   - [ ] 更新内容研究偏好权重
```

### Quick Update Template

将以下信息追加到记忆文件：

```yaml
interaction_log:
  - timestamp: "2026-04-10Txx:xx:xx"
    user: "[user_hash]"
    topic: "[主题]"
    slides_count: N
    final_style: "[风格名]"
    layouts_used: ["layout1", "layout2", ...]
    charts_used: N
    images_used: N
    web_search_used: true/false
    web_search_count: N
    web_search_satisfaction: "high/medium/low"
    verification_rounds_avg: N
    satisfaction: "high/medium/low"
    modifications: ["布局修改", "内容调整", ...]
    learnings: "[关键学习点]"
```

---

## Supporting Files

| File | Purpose | When to Read |
|------|---------|-------------|
| [STYLE_PRESETS.md](STYLE_PRESETS.md) | 12 curated visual presets with colors, fonts, and signature elements | Phase 2 (style selection) |
| [viewport-base.css](viewport-base.css) | Mandatory responsive CSS — copy into every presentation | Phase 3 (generation) |
| [html-template.md](html-template.md) | HTML structure, JS features, code quality standards | Phase 3 (generation) |
| [animation-patterns.md](animation-patterns.md) | CSS/JS animation snippets and effect-to-feeling guide | Phase 3 (generation) |
| [scripts/extract-pptx.py](scripts/extract-pptx.py) | Python script for PPT content extraction | Phase 4 (conversion) |
| [scripts/web_search.py](scripts/web_search.py) | 智谱AI网络搜索脚本 — 用于为幻灯片搜索文案素材 | Phase 1.5 & Phase 3.0a (when research enabled) |
| [templates/websearch.md.template](templates/websearch.md.template) | 搜索记录模板 | 项目初始化时复制 |
| [Memory: frontend-slides-runtime-log](../../../projects/-Users-mac--claude/memory/frontend-slides-runtime-log.md) | Self-evolving memory system — user profiles, learned weights, failure patterns | Phase 0.5 (always read first) & Phase 6 (always update after) |

---

## Environment Requirements

### Core Requirements
- Python 3.10+ (managed by uv)
- `uv` tool installed

### Setup (One-time)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to skill directory
cd /Users/mac/.claude/skills/ppt-clouder

# Install Python 3.10
uv python install 3.10

# Create virtual environment
uv venv --python 3.10 .venv

# Install dependencies
uv pip install -p .venv python-pptx zhipuai python-dotenv
```

### Optional: Web Search Feature

**Required for content research functionality:**

1. **API Key Setup**:
   ```bash
   export ZHIPU_API_KEY='your-api-key-here'
   ```
   Get key: https://open.bigmodel.cn/usercenter/apikeys

2. **Or create .env file**:
   ```bash
   echo 'ZHIPU_API_KEY=your-api-key-here' > /Users/mac/.claude/skills/ppt-clouder/.env
   ```

### Running Scripts

Scripts use the virtual environment automatically via shebang:

```bash
# Extract PPT
/Users/mac/.claude/skills/ppt-clouder/scripts/extract-pptx.py input.pptx

# Web search
/Users/mac/.claude/skills/ppt-clouder/scripts/web_search.py "搜索内容"
```

Or explicitly use the venv Python:

```bash
/Users/mac/.claude/skills/ppt-clouder/.venv/bin/python scripts/web_search.py "搜索内容"
```
