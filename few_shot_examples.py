FEW_SHOT_EXAMPLES = [
    (
        "How many employees work for multiple companies?",
        "SELECT COUNT(*) FROM (SELECT employee_id FROM employee_company GROUP BY employee_id HAVING COUNT(*) > 1);"
    ),
    (
        "What jobs are related to Recon Pest Control?",
        "SELECT j.* FROM job j JOIN company c ON j.company_id = c.company_id WHERE c.name = 'Recon Pest Control';"
    ),
    (
        "What is the total amount of all invoices?",
        "SELECT SUM(total_amount) FROM invoice;"
    ),
    (
        "List all active employees with their base rates.",
        "SELECT first_name, last_name, base_rate FROM employee WHERE active = 1;"
    ),
    (
        "How many jobs are currently in progress?",
        "SELECT COUNT(*) FROM job WHERE status = 'in_progress';"
    ),
    (
        "What is the average gross pay for employees in the most recent pay period?",
        "SELECT AVG(gross_pay) FROM payroll WHERE pay_period_id = (SELECT MAX(pay_period_id) FROM pay_period);"
    ),
    (
        "Show me all customers who have jobs with Central Glass.",
        "SELECT DISTINCT c.* FROM customer c JOIN job j ON c.customer_id = j.customer_id JOIN company co ON j.company_id = co.company_id WHERE co.name = 'Central Glass';"
    ),
    (
        "What are the total expenses for each company?",
        "SELECT c.name, SUM(e.amount) as total_expenses FROM expense e JOIN company c ON e.company_id = c.company_id GROUP BY c.company_id, c.name;"
    ),
    (
        "What is the profit for Recon Pest Control?",
        "SELECT (SELECT COALESCE(SUM(p.amount), 0) FROM payment p JOIN invoice i ON p.invoice_id = i.invoice_id JOIN company c ON i.company_id = c.company_id WHERE c.name = 'Recon Pest Control') - (SELECT COALESCE(SUM(e.amount), 0) FROM expense e JOIN company c ON e.company_id = c.company_id WHERE c.name = 'Recon Pest Control') AS profit;"
    )
]
