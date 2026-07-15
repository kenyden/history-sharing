#!/usr/bin/env python3
"""
Parse 馬雅全書.txt and split into individual chapter Markdown files
for the Astro/Starlight website.
"""
import re, os, unicodedata, sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

SRC = '/Users/kennethlin/Desktop/maya/馬雅全書.txt'
OUT_BASE = '/Users/kennethlin/history-sharing/src/content/docs/馬雅文化/馬雅全書'

def sanitize_path(text):
    """Remove special chars, keep Chinese, letters, digits, spaces and hyphens"""
    # Replace Chinese/special punctuation with hyphen
    text = re.sub(r'[、，。·：\u2014\u2013\u3001\u3002\uff0c\uff1a\u00b7]+', '-', text)
    # Remove anything not Chinese, alphanumeric, space, or hyphen
    text = re.sub(r'[^\u4e00-\u9fff\w\s\-]', '', text)
    # Collapse multiple hyphens
    text = re.sub(r'-+', '-', text)
    # Replace spaces with hyphens
    text = re.sub(r'\s+', '-', text)
    return text.strip('-')

SRC = '/Users/kennethlin/Desktop/maya/馬雅全書.txt'
OUT_BASE = '/Users/kennethlin/history-sharing/src/content/docs/馬雅文化/馬雅全書'

# Read entire file
with open(SRC, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Skip table of contents (lines 0-97, we know from reading)
# Find first volume separator
content_start = 0
for i, line in enumerate(lines):
    if line.strip().startswith('=' * 30) and '卷一' in lines[i+1] if i+1 < len(lines) else '':
        content_start = i
        break

# State machine
current_vol = None
current_chap = None
current_lines = []
output_dir = None
chap_counter = 0

def slugify(text):
    """Create a simple slug for filenames"""
    # Remove special chars, keep Chinese and alphanumeric
    result = []
    for ch in text.strip():
        if ch.isalnum() or ch in ' _-':
            result.append(ch)
        elif unicodedata.category(ch).startswith('L'):  # letter categories
            result.append(ch)
        elif ch in '（）、。，·—':
            result.append(ch)
    s = ''.join(result).strip()
    # Remove extra spaces
    s = re.sub(r'\s+', ' ', s)
    return s[:60]

def safe_filename(name):
    """Make a safe filename, removing problematic chars"""
    name = sanitize_path(name)
    return name[:80]

def write_chapter(vol_name, chap_num, chap_title, chap_lines, dynasty_info=None):
    """Write a chapter as a Markdown file"""
    global chap_counter
    
    if not chap_title:
        return
    
    chap_counter += 1
    
    # Create volume subdirectory
    vol_slug = f"{vol_name.split('·')[0].strip()}-{vol_name.split('·')[-1].strip()}" if '·' in vol_name else vol_name
    vol_slug = sanitize_path(vol_slug)[:30]
    
    vol_dir = os.path.join(OUT_BASE, vol_slug)
    os.makedirs(vol_dir, exist_ok=True)
    
    # Build filename
    num_part = f"{chap_num:02d}" if isinstance(chap_num, int) else str(chap_num)
    fname = f"{num_part}-{safe_filename(chap_title)}.md"
    fpath = os.path.join(vol_dir, fname)
    
    # Build description
    desc = chap_title
    if dynasty_info:
        desc = f"{chap_title}（{dynasty_info}）"
    
    # Prepare content - remove chapter title line from content
    content_text = '\n'.join(chap_lines).strip()
    
    # Build full markdown
    md = f"""---
title: {chap_title}
description: {desc}
---

{content_text}
"""
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(md)
    
    print(f"  ✅ {fname}")

# Start parsing
i = content_start
current_vol_name = None
current_chap_title = None
current_chap_num = None
chap_accum = []
dynasty_line = None
in_volume_header = False
volume_header_lines = []

while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    
    # Detect volume separator (===...===)
    if stripped.startswith('=' * 10) and len(stripped) > 30:
        # Check if next line contains volume title
        if i + 1 < len(lines):
            next_line = lines[i+1].strip()
            if '卷' in next_line and '·' in next_line:
                # New volume
                # First, flush any pending chapter
                if current_chap_title and chap_accum:
                    write_chapter(current_vol_name, current_chap_num, current_chap_title, 
                                chap_accum, dynasty_line)
                    chap_accum = []
                    dynasty_line = None
                
                current_vol_name = next_line.strip()
                current_chap_title = None
                current_chap_num = None
                print(f"\n📁 {current_vol_name}")
                # Skip volume header lines (the === and the title and blank lines)
                i += 3
                continue
        i += 1
        continue
    
    # Detect chapter title: 第X章 ... or 附錄
    chap_match = re.match(r'^第([一二三四五六七八九十百零]+)章\s+(.+)$', stripped)
    appendix_match = re.match(r'^附錄\s+(.+)$', stripped)
    
    if chap_match or appendix_match:
        # Flush previous chapter
        if current_chap_title and chap_accum:
            write_chapter(current_vol_name, current_chap_num, current_chap_title, 
                        chap_accum, dynasty_line)
            chap_accum = []
            dynasty_line = None
        
        if chap_match:
            ch_num_text = chap_match.group(1)
            # Convert Chinese number to int (e.g. "十一" → 11, "二十" → 20)
            ch_num = 0
            temp = 0
            for c in ch_num_text:
                if c in '一二三四五六七八九':
                    temp = '一二三四五六七八九'.index(c) + 1
                elif c == '十':
                    if temp == 0:
                        temp = 10
                    else:
                        temp *= 10
                    ch_num += temp
                    temp = 0
                elif c == '百':
                    if temp == 0:
                        temp = 100
                    else:
                        temp *= 100
                    ch_num += temp
                    temp = 0
                elif c == '千':
                    if temp == 0:
                        temp = 1000
                    else:
                        temp *= 1000
                    ch_num += temp
                    temp = 0
            ch_num += temp
            current_chap_num = ch_num
            current_chap_title = chap_match.group(2).strip()
        elif appendix_match:
            current_chap_num = f"appendix"
            current_chap_title = appendix_match.group(1).strip()
        
        i += 1
        continue
    
    # Check for dynasty info line
    if current_chap_title and stripped.startswith('對應中國'):
        dynasty_line = stripped
        i += 1
        continue
    
    # Collect chapter content
    if current_chap_title:
        # Skip the blank line between title and content start
        if not stripped and not chap_accum:
            # Skip leading blank line
            i += 1
            continue
        chap_accum.append(line.rstrip())
    
    i += 1

# Flush final chapter
if current_chap_title and chap_accum:
    write_chapter(current_vol_name, current_chap_num, current_chap_title, 
                chap_accum, dynasty_line)

print(f"\n\n📊 Total: {chap_counter} chapters written to {OUT_BASE}")
