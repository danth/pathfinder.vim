def escape(search_query):
    for char in r"\^$.*[~/":
        search_query = search_query.replace(char, "\\" + char)

    return search_query


def search(text, start, target):
    search_text = text[target:]

    text = text[start + 1 :] + text[:start]
    target -= start + 1
    if target < 0:
        target = len(text) + target + 1

    for query_length in range(1, len(search_text) + 1):
        query = search_text[:query_length]
        if text.index(query) == target:
            return query


def search_lines(lines, start_line, start_col, target_line, target_col):
    text = "\n".join(lines)
    start = sum(len(line) + 1 for line in lines[:start_line]) + start_col
    target = sum(len(line) + 1 for line in lines[:target_line]) + target_col
    return search(text, start, target)
