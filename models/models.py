from sqlalchemy import (
    MetaData,
    Column,
    Table,
    Integer,
    String,
    TIMESTAMP,
    ARRAY,
)

metadata = MetaData()

visited_domains = Table(
    "visited_domains",
    metadata,
    Column("visited_domains", ARRAY(String), default=[]),
    Column("tracked_at", TIMESTAMP, index=True),
)
