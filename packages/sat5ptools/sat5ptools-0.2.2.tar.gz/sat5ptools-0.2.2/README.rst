
SAT5P tools
===========

Background
----------

These tools manage "conversations" for use with a chat-style
web interface created as part of the *"Improving the transition
and retention of regional students from low−socioeconomic 
backgrounds: A '5Ps' approach"* project.

The chat interface receives the conversation script in a JSON
data file. Each question follows one of the two following 
patterns:

+-----------------------------+-------------------------------+
| Multi answer question       | Text answer question          |
+=============================+===============================+
|                                                             |
| A question id                                               |
|                                                             |
+-----------------------------+-------------------------------+
|                                                             |
| Text, images, and links, in one or more paragraphs.         |
|                                                             |
+-----------------------------+-------------------------------+
|                             |                               |
| One or more responses, each | A space for the user to type  |
| containing:                 | text (usually in response to  |
|                             | prompts in the text section). |
| - a short response label    |                               |
| - an optional information   +-------------------------------+
|   block, displayed only     |                               |
|   when this response is     | The id of a destination       |
|   selected by the user      | question.                     |
| - the id of a destination   |                               |
|   question                  |                               |
|                             |                               |
+-----------------------------+-------------------------------+
|                                                             |
| A question id                                               |
|                                                             |
+-----------------------------+-------------------------------+

Authoring the conversation script is usually done in an Excel
spreadsheet with the following columns:

- Question ID
- Question Text
- Responses (either a list of responses, or "{text}" indicating that this is a text answer question).
- Response 1 Result detailing the info and destination question of the first response
- Response 2 Result detailing the info and destination question of the second response
- similar responses for 3, 4, 5, 6, 7, 8, and 9

Tools available
---------------

**``excel2qns``** is a command line tool for producing a conversation JSON file from an Excel document.

more..

**``excel2graph``** is a command line tool for producing a GraphViz graph in ``dot`` format from an Excel document.

more..

**``excel2all``** is a command line tool for producing both a conversation JSON file and a GraphViz graph from an Excel document.

Formatting available in Excel
-----------------------------












