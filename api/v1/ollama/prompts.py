#!/usr/bin/env python3
'''
Prompts for ollama
'''

prompt1 = '''
Consider the benefits of positive affect journaling. I want you to be a detailed, insightful and empathetic but factual
personal journal analyst. Your job is to review my personal journals and help me unlock the benefits of positive 
affect journaling. Below, I provide some of my journal entries over a period of time in JSON  format. The keys 
are dates when I made the journal entries. For each key, the value is a list of journal entries I made on the day
represented by the key. I want you to analyse the journal entries and extract all the topical groupings I have written
about in the entries. For example, if, in my entries, I wrote about my office and also expressed concern about my
master's degree, then the topical groupings could be career and education. The topical groupings in your response
shouldn't be limited to those two. I only provided them as examples to show what I mean. Below are my journal entries:

{entries}

Your response must strictly be a python list of topical groupings called groups, nothing more.
e.g. groups = ['fitness', 'career']
'''

prompt2 = '''
Consider the benefits of positive affect journaling. I want you to be a detailed, insightful and empathetic but factual
personal journal analyst. Your job is to review my personal journals and help me unlock the benefits of positive 
affect journaling. Below, I provide a series of my journal entries over a period of time in JSON format and a list of 
topical groupings. The keys in the JSON-formatted journal entries are dates when i made the entries. For each key,
the value is a list of journal entries I made on the day represented by the key. I want you to analyse the journal
entries (the values in the JSON) and extract insights on all the topical groupings provided. Your analysis should
include the following subsections for each topical grouping: 'What You could do better', 'What You did well', and 
'Observations'. You can optionally add a 'Suggestions' section at the end of everything if there's anything more
you'd like to say, or any more insights you'd like to give based on my journal entries. Below are my journal
entries and the topical groupings:

Journal entries: 
{entries}

Topical groupings:
{groupings}
'''
