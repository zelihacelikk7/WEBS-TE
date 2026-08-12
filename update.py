# -*- coding: utf-8 -*-
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update background color
content = content.replace('--bg-color: #f4f6f8;', '--bg-color: #FAF9F6;')

# 2. Add radial gradient to body
body_css_old = """        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.6;
            overflow-x: hidden;
        }"""
body_css_new = """        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            background-image: radial-gradient(circle at 50% 50%, rgba(253, 216, 53, 0.05) 0%, var(--bg-color) 60%);
            color: var(--text-main);
            line-height: 1.6;
            overflow-x: hidden;
        }"""
content = content.replace(body_css_old, body_css_new)

# 3. Replace CSS block for content cards
css_old_regex = r'/\* CONTENT CARDS \*/.*?/\* DESKTOP STYLES \*/'
css_new = """/* FLUID SECTIONS (APPLE STYLE) */
        .fluid-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 120px;
            position: relative;
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
            padding: 0 20px;
        }

        .huge-number {
            position: absolute;
            font-size: 8rem;
            font-weight: 800;
            color: var(--enerjisa-yellow);
            opacity: 0.15;
            top: -50px;
            left: 10px;
            z-index: -1;
            pointer-events: none;
            line-height: 1;
        }

        .fluid-content {
            flex: 1;
            padding: 20px 0;
            z-index: 2;
            width: 100%;
        }

        .fluid-title {
            color: #1E293B;
            font-size: 2.2rem;
            margin-bottom: 25px;
            font-weight: 700;
            position: relative;
        }

        .fluid-list {
            list-style: none;
            color: #1E293B;
        }

        .fluid-list li {
            position: relative;
            padding-left: 30px;
            margin-bottom: 15px;
            font-size: 1.15rem;
            line-height: 1.8;
        }

        .fluid-list li::before {
            content: '';
            position: absolute;
            left: 0;
            top: 12px;
            width: 10px;
            height: 10px;
            background-color: var(--enerjisa-yellow);
            border-radius: 50%;
        }

        .fluid-media {
            flex: 1;
            width: 100%;
            min-height: 350px;
            background-color: rgba(255, 255, 255, 0.6);
            border: 1px solid rgba(0, 0, 0, 0.05);
            border-radius: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-muted);
            font-weight: 600;
            padding: 20px;
            z-index: 2;
            margin-top: 30px;
        }

        /* DESKTOP STYLES */"""
content = re.sub(css_old_regex, css_new, content, flags=re.DOTALL)

# Update media queries for fluid section
desktop_css_old_regex = r'\.content-card \{.*?\.content-card:nth-child\(even\) \.card-media \{.*?\}'
desktop_css_new = """.fluid-section {
                flex-direction: row;
                gap: 80px;
                padding: 0 40px;
            }
            .fluid-section:nth-child(even) {
                flex-direction: row-reverse;
            }
            .fluid-section:nth-child(even) .huge-number {
                left: auto;
                right: 20px;
            }
            .fluid-content {
                padding: 40px 0;
            }
            .fluid-media {
                margin-top: 0;
            }"""
content = re.sub(desktop_css_old_regex, desktop_css_new, content, flags=re.DOTALL)

# 4. Replace HTML Sections
def replace_section(match):
    num = match.group(1)
    title = match.group(2)
    bullets = match.group(3)
    media = match.group(4)
    
    # replace .card-list with .fluid-list
    bullets = bullets.replace('card-list', 'fluid-list')
    
    return f'''    <section class="fluid-section" data-aos="fade-up" data-aos-offset="200">
        <div class="huge-number">{{num}}</div>
        <div class="fluid-content">
            <h2 class="fluid-title">{{title}}</h2>
            {{bullets}}
        </div>
        <div class="fluid-media">
            {{media}}
        </div>
    </section>'''

section_regex = r'<section>\s*<div class="content-card".*?>\s*<div class="card-body">\s*<h2 class="card-title"><span>Bölüm (\d+)</span> (.*?)</h2>\s*(<ul class="card-list">.*?</ul>)\s*</div>\s*<div class="card-media">\s*(.*?)\s*</div>\s*</div>\s*</section>'
content = re.sub(section_regex, replace_section, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated successfully")
