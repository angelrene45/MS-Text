Slide 9: Semantic Model Specification
Title: Semantic Model Specification
Content:

SemanticModel: A semantic model is a collection of logical tables.

tables: List[LogicalTable]
LogicalTable: A logical table is a view over a database table or view.

dimensions: List[Dimension]
time_dimensions: List[TimeDimension]
measures: List[Measure]
filters: List[Filter]
Dimension: A dimension contains categorical values.

TimeDimension: A time dimension contains time values.

Measure: A measure contains numerical values.

Filter: A filter represents a SQL expression used for filtering.

Verified Queries: Example questions and queries that answer them.
