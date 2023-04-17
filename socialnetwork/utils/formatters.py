import logging


class SQLFormatter(logging.Formatter):
    def format(self, record):
        # Check if Pygments is available for coloring
        try:
            import pygments
            from pygments.formatters import TerminalTrueColorFormatter
            from pygments.lexers import SqlLexer
        except ImportError:
            pygments = None

        # Check if sqlparse is available for indentation
        try:
            import sqlparse
        except ImportError:
            sqlparse = None

        # Remove leading and trailing whitespaces
        sql = record.sql.strip()

        if sqlparse:
            # Indent the SQL query
            sql = sqlparse.format(sql, reindent=True)

        if pygments:
            # Highlight the SQL query
            sql = pygments.highlight(
                sql,
                SqlLexer(),
                TerminalTrueColorFormatter(),
            )

        # Set the records statement to the formatted query
        record.statement = sql
        return super(SQLFormatter, self).format(record)
