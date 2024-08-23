import json
from typing import Any, Protocol, TypedDict

from .models import Message, PromptFunction, PromptVersion


class Prompt(Protocol):
    v1: PromptVersion
    v2: PromptVersion
    edge_list: PromptVersion


class Versions(TypedDict):
    v1: PromptFunction
    v2: PromptFunction
    edge_list: PromptFunction


def v1(context: dict[str, Any]) -> list[Message]:
    return [
        Message(
            role='system',
            content='You are a helpful assistant that de-duplicates relationship from edge lists.',
        ),
        Message(
            role='user',
            content=f"""
        Given the following context, deduplicate facts from a list of new facts given a list of existing facts:

        Existing Facts:
        {json.dumps(context['existing_edges'], indent=2)}

        New Facts:
        {json.dumps(context['extracted_edges'], indent=2)}

        Task:
        If any facts in New Facts is a duplicate of a fact in Existing Facts, 
        do not return it in the list of unique facts.

        Guidelines:
        1. The facts do not have to be completely identical to be duplicates, 
        they just need to have similar factual content

        Respond with a JSON object in the following format:
        {{
            "unique_facts": [
                {{
                    "uuid": "unique identifier of the fact"
                }}
            ]
        }}
        """,
        ),
    ]


def v2(context: dict[str, Any]) -> list[Message]:
    return [
        Message(
            role='system',
            content='You are a helpful assistant that de-duplicates relationship from edge lists.',
        ),
        Message(
            role='user',
            content=f"""
        Given the following context, deduplicate edges from a list of new edges given a list of existing edges:

        Existing Edges:
        {json.dumps(context['existing_edges'], indent=2)}

        New Edges:
        {json.dumps(context['extracted_edges'], indent=2)}

        Task:
        1. start with the list of edges from New Edges
        2. If any edge in New Edges is a duplicate of an edge in Existing Edges, replace the new edge with the existing
            edge in the list
        3. Respond with the resulting list of edges

        Guidelines:
        1. Use both the triplet name and fact of edges to determine if they are duplicates, 
            duplicate edges may have different names meaning the same thing and slight variations in the facts.
        2. If you encounter facts that are semantically equivalent or very similar, keep the original edge

        Respond with a JSON object in the following format:
        {{
            "new_edges": [
                {{
                    "triplet": "source_node_name-edge_name-target_node_name",
                    "fact": "one sentence description of the fact"
                }}
            ]
        }}
        """,
        ),
    ]


def edge_list(context: dict[str, Any]) -> list[Message]:
    return [
        Message(
            role='system',
            content='You are a helpful assistant that de-duplicates edges from edge lists.',
        ),
        Message(
            role='user',
            content=f"""
        Given the following context, find all of the duplicates in a list of facts:

        Facts:
        {json.dumps(context['edges'], indent=2)}

        Task:
        If any facts in Facts is a duplicate of another fact, return a new fact with one of their uuid's.

        Guidelines:
        1. The facts do not have to be completely identical to be duplicates, they just need to have similar content
        2. The final list should have only unique facts. If 3 facts are all duplicates of each other, only one of their
            facts should be in the response

        Respond with a JSON object in the following format:
        {{
            "unique_facts": [
                {{
                    "uuid": "unique identifier of the fact",
                    "fact": "fact of a unique edge"
                }}
            ]
        }}
        """,
        ),
    ]


versions: Versions = {'v1': v1, 'v2': v2, 'edge_list': edge_list}