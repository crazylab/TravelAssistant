import sys
from wit import Wit

# Quickstart example
# See https://wit.ai/l5t/Quickstart

if len(sys.argv) != 2:
    print("usage: python examples/quickstart.py <wit-token>")
    exit(1)
access_token = sys.argv[1]

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def say(session_id, context, msg):
    print(msg)

def merge(session_id, context, entities, msg):
    # print entities
    print entities
    dest = first_entity_value(entities, 'dest')
    if dest:
        context['dest'] = dest
    return context

def error(session_id, context, e):
    print(str(e))

actions = {
    'say': say,
    'merge': merge,
    'error': error
}

client = Wit(access_token, actions)
response = client.run_actions(session_id="xyz",message="I'm planning to go to usa", max_steps=3, context={})

print response
