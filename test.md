This table contains employee dimension data, including both static and historically changing attributes.

EMP_MS_CODE is the stable business identifier for an employee, remaining constant across time, even as roles, teams, or units change.

EMPLOYEE_KEY is a surrogate key representing a specific version of the employee's profile at a point in time (e.g., when business unit or role changes).
This allows tracking the history of employee changes over time and ensures accurate point-in-time analysis.
