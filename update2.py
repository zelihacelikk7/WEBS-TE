# -*- coding: utf-8 -*-
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Clean up old CSS media queries
css_start = content.find('/* DESKTOP STYLES */')
if css_start == -1:
    css_start = content.find('/* DESKTOP STYLES (NOW DEFAULT) */')

css_end = content.find('</style>')
if css_start != -1 and css_end != -1:
    old_css = content[css_start:css_end]
    
    # We want a static, desktop-only layout. No media queries.
    new_css = """/* STRICT DESKTOP LAYOUT */
        .hero-title { font-size: 4rem; }
        .hero-subtitle { font-size: 1.5rem; }
        .team-container {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 30px;
            overflow-x: visible;
            padding: 0;
            width: 100%;
        }
        .team-member { width: auto; }
        .fluid-section {
            flex-direction: row;
            gap: 80px;
            padding: 0 40px;
        }
        .fluid-section:nth-child(even) { flex-direction: row-reverse; }
        .fluid-section:nth-child(even) .huge-number { left: auto; right: 20px; }
        .fluid-content { padding: 40px 0; }
        .fluid-media { margin-top: 0; }
        
        /* STICKY LOGO */
        .sticky-logo {
            position: fixed;
            top: 20px;
            left: 40px;
            width: 280px !important;
            height: auto;
            z-index: 1000;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
        }

        .sticky-logo.show {
            opacity: 1;
            pointer-events: auto;
        }

        /* WRAPPER CSS */
        body {
            overflow-x: hidden;
            background-color: var(--bg-color);
            margin: 0;
            padding: 0;
        }
        #desktop-wrapper {
            width: 1200px;
            margin: 0 auto;
            background-image: radial-gradient(circle at 50% 50%, rgba(253, 216, 53, 0.05) 0%, var(--bg-color) 60%);
        }
    """
    content = content[:css_start] + new_css + content[css_end:]

# Remove old body css block
body_css_regex = r'\s*body\s*\{[^}]*\}'
content = re.sub(body_css_regex, '', content, count=1)

# 2. Add wrapper to body
body_start = content.find('<body>') + len('<body>')
content = content[:body_start] + '\n    <div id="desktop-wrapper">' + content[body_start:]

# 3. Close wrapper and add JS
body_end = content.find('</body>')
js_code = """
    </div>
    <!-- SCALE SCRIPT -->
    <script>
        function scaleWrapper() {
            const wrapper = document.getElementById('desktop-wrapper');
            if (window.innerWidth < 1200) {
                const scale = window.innerWidth / 1200;
                wrapper.style.transform = scale();
                wrapper.style.transformOrigin = 'top left';
            } else {
                wrapper.style.transform = 'scale(1)';
                wrapper.style.transformOrigin = 'top center';
            }
            document.body.style.height = ${wrapper.getBoundingClientRect().height}px;
        }
        window.addEventListener('resize', scaleWrapper);
        scaleWrapper();
    </script>
"""
content = content[:body_end] + js_code + content[body_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated perfectly")
