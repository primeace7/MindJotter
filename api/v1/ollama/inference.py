#!/usr/bin/env python3
'''
Generate insights from journal entries by running local inference on llama3 with ollama
'''
import ollama
from .prompts import prompt1, prompt2
from ..auth import Auth
from datetime import datetime, timezone
import re


auth = Auth()

def get_month_entries(session_id: str) -> str:
    '''
    Get all of a user's entries for the current month
    '''
    all_entries = auth.all_user_entries(session_id)

    current_date = datetime.now(tz=timezone.utc)

    current_month_entries = [
        entry for entry in all_entries
        if entry.created_at.month == current_date.month]

    current_month_entries.sort(key=lambda obj: obj.created_at)

    journals_json = {}
    fmt = '%A %B %d'

    for obj in current_month_entries:
        pretty_date = obj.created_at.strftime(fmt)
        if pretty_date not in journals_json:
            journals_json[pretty_date] = [obj.entry]
        else:
            journals_json[pretty_date].append(obj.entry)

    return str(journals_json)

def generate_groups(entries: str) -> str:
    '''
    Generage a group of topics that describe a user's journal entries
    '''
    result = ollama.generate(model='llama3', prompt=prompt1.format(entries=entries))['response']
    # print('results from grouping: ', result)

    # Extract the list content within square brackets
    pattern = r"\[([^\]]*)\]"
    matches = re.findall(pattern, result, re.MULTILINE)
    if len(matches) == 1:
        matches = matches[0].split(',')

    # Convert the extracted strings to a Python list
    groups = [group.strip().strip('"') for group in matches]  # Remove quotes

    return str(groups)

def generate_insights(session_id: str) -> str:
    '''
    Generate insights from a user's journal entries for the current month
    '''
    current_month_entries = get_month_entries(session_id=session_id)

    groupings = generate_groups(entries=current_month_entries)

    result = ollama.generate(
        model='llama3', prompt=prompt2.format(entries=current_month_entries, groupings=groupings))
    
    return result['response']