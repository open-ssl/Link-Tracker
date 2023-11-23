INSERT_NEW_LINKS_TEMPLATE = """
    INSERT INTO visited_domains
    VALUES ({}, current_timestamp)
"""

SELECT_VISITED_DOMAINS_IN_INTERVAL_TEMPLATE = """
    SELECT json_agg(visited_domains)
    from visited_domains
    where tracked_at 
"""