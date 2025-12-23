'''
Stripe Capital
Stripe Capital lends our merchants funds in order to grow their businesses.
In exchange for these funds, instead of a traditional interest over time model, Stripe charges a fixed loan fee on top of the original loan amount.
To get back the investment, some percentage of the merchant's future sales goes towards repayment, until the total owed amount is repaid.
In this problem, you'll be building a bookkeeping system for a modified version of Stripe Capital.
This bookkeeping system will have 4 API methods:
   1. A merchant can create a loan.
   2. A merchant can pay down a loan manually.
   3. A merchant can process transactions, from which some percentage of the processed amount goes towards repayment towards a loan.
   4. A merchant can increase an existing loan's amount.
Your Task
1. Evaluate each line of stdin, performing the actions as described by documentation below.
   - Each line will always begin with an API method, followed by a colon and a space, then followed by comma separated parameters for the API method, in order of the documentation.
2. After evaluating all actions, print out a list of $merchant_id, $outstanding_debt pairs, skipping over merchants who do not have an outstanding balance. This list should be lexicographically sorted by the merchant ID.
Keep in mind:
   - We will not test you against unparsable input formats. Handle them as you see fit.
   - We will evaluate both code correctness and code quality.
   - You are allowed to refer the web to make sure of various resources, tools, and documentation. However, do not copy code verbatim.
API Documentation
CREATE_LOAN: Merchant initiates a loan.
Fields
   - merchant_id: The ID of the merchant. (String; non-empty)
   - loan_id: The ID of the merchant's loan. (String; non-empty)
   - amount: The initial loan amount. (Integer; x >= 0)
Ex: CREATE_LOAN: merchant1, loan1, 1000
PAY_LOAN: Merchants pays off their loans on a one-time basis.
Fields
   - merchant_id: The ID of the merchant. (String; non-empty)
   - loan_id: The ID of loan to pay off. (String; non-empty)
   - amount: The amount given back to Stripe. (Integer; x >= 0)
Ex: PAY_LOAN: merchant1, loan1, 1000
INCREASE_LOAN: Merchant increases an existing loan.
Fields
   - merchant_id: The ID of the merchant. (String; non-empty)
   - loan_id: The ID of loan to increase. (String; non-empty)
   - amount: The amount to increase the loan by. (Integer; x >= 0)
Ex: PAY_LOAN: merchant1, loan1, 1000
TRANSACTION_PROCESSED: A single transaction. A portion of the transaction amount is withheld to pay down the merchant's outstanding loans.
Fields
   - merchant_id: The ID of the merchant. (String; non-empty)
   - loan_id: The ID of loan to pay off for this transaction. (String; non-empty)
   - amount: The amount this transaction processed. (Integer; x >= 0)
   - repayment_percentage: The percentage of the transaction amount that goes towards repayment. (Integer; 1 <= x <= 100)
Ex: TRANSACTION_PROCESSED: merchant1, loan1, 500, 10
System Behavior
   - This version of Capital will represent all monetary amounts as U.S. cents in integers (e.g. amount = 1000 => $10.00 USD)
   - A merchant may have multiple outstanding loans.
   - Loan IDs are unique to a given merchant only.
   - A loan's outstanding balance should never go negative. Ignore the remaining amount in the case of overpayment.
   - Truncate repayments when applicable (e.g. if withholding from a transaction is 433.64 cents, truncate to 433 cents).
   - Your system should handle invalid API actions appropriately. (ex: attempting to pay-off a nonexistent loan)
Examples
Example 0 (manual repayment):
   CREATE_LOAN: acct_foobar,loan1,5000
   PAY_LOAN: acct_foobar,loan,1000
Expected Output:
   acct_foobar,4000
Explanation:
   1. The merchant acct_foobar creates a loan ("loan1") for $50.00.
   2. The merchant pays down $10.00 of the loan.
   Result: The merchant owes Stripe $40.00.
Example 1 (transaction repayment):
   CREATE_LOAN: acct_foobar,loan1,5000
   CREATE_LOAN: acct_foobar,loan2,5000
   TRANSACTION_PROCESSED: acct_foobar,loan1,500,10
   TRANSACTION_PROCESSED: acct_foobar,loan2,500,1
Expected Output:
   acct_foobar,9945
Example 2 (multiple actions):
   CREATE_LOAN: acct_foobar,loan1,1000
   CREATE_LOAN: acct_foobar,loan2,2000
   CREATE_LOAN: acct_barfoo,loan1,3000
   TRANSACTION_PROCESSED: acct_foobar,loan1,100,1
   PAY_LOAN: acct_barfoo,loan1,1000
   INCREASE_LOAN: acct_foobar,loan2,1000
Expected Output:
   acct_barfoo,2000
   acct_foobar,3999
Explanation:
   1. The merchant acct_foobar creates two loans for $30.00 in total.
   2. The merchant acct_barfoo creates a loan for $30.00.
   3. Merchant acct_foobar processes a transaction, paying off $0.01 from loan1.
   4. Merchant acct_barfoo manually pays back a loan for $10.00.
   5. Merchant acct_foobar increases its second loan by $10.00.
   Result: acct_barfoo owes $20.00, acct_foobar owes $39.99.
'''

from collections import defaultdict
import math

class StripeCapital:
    def __init__(self):
        # { merchant_id: {loan_id: amount} }
        self.merchants = defaultdict(dict)
    
    def add_line(self, line):
        params = line.split(': ', 1)
        if len(params) < 2:
            raise ValueError("Invalid input line: " + line)
        args = params[1].split(',')

        action = params[0].strip()
        if action == "CREATE_LOAN":
            self.create_loan(args)
        elif action == "PAY_LOAN":
            self.pay_loan(args)
        elif action == "INCREASE_LOAN":
            self.increase_loan(args)
        elif action == "TRANSACTION_PROCESSED":
            self.transaction_processed(args)
        else:
            raise ValueError("Unknown action: " + action)

    def create_loan(self, args):
        if len(args) != 3:
            raise ValueError("Invalid number of arguments for CREATE_LOAN: " + str(args))
        try:
            merchant_id = args[0].strip()
            loan_id = args[1].strip()
            amount = int(args[2].strip())
            if merchant_id in self.merchants and loan_id in self.merchants[merchant_id]:
                raise ValueError("Loan already exists for merchant: " + merchant_id + ", loan: " + loan_id)
            
            self.merchants[merchant_id][loan_id] = amount
        except Exception as e:
            raise ValueError("Error parsing arguments for CREATE_LOAN: " + str(args)) from e

    def pay_loan(self, args):
        if len(args) != 3:
            raise ValueError("Invalid number of arguments for PAY_LOAN: " + str(args))
        try:
            merchant_id = args[0].strip()
            loan_id = args[1].strip()
            amount = int(args[2].strip())

            if merchant_id not in self.merchants or loan_id not in self.merchants[merchant_id]:
                raise ValueError("Loan does not exist for merchant: " + merchant_id + ", loan: " + loan_id)
            
            current_amount = self.merchants[merchant_id][loan_id]
            new_amount = 0 if current_amount - amount < 0 else current_amount - amount
            self.merchants[merchant_id][loan_id] = new_amount
        except Exception as e:
            raise ValueError("Error parsing arguments for PAY_LOAN: " + str(args)) from e


    def increase_loan(self, args):
        if len(args) != 3:
            raise ValueError("Invalid number of arguments for INCREASE_LOAN: " + str(args))
        try:
            merchant_id = args[0].strip()
            load_id = args[1].strip()
            amount = int(args[2].strip())
            if merchant_id not in self.merchants or load_id not in self.merchants[merchant_id]:
                raise ValueError("Loan does not exist for merchant: " + merchant_id + ", loan: " + load_id)
            
            current_amount = self.merchants[merchant_id][load_id]
            new_amount = current_amount + amount
            self.merchants[merchant_id][load_id] = new_amount
        except Exception as e:
            raise ValueError("Error parsing arguments for INCREASE_LOAN: " + str(args)) from e

    def transaction_processed(self, args):
        if len(args) != 4:
            raise ValueError("Invalid number of arguments for TRANSACTION_PROCESSED: " + str(args))
        try:
            merchant_id = args[0].strip()
            loan_id = args[1].strip()
            amount = int(args[2].strip())
            fee_percentage = float(args[3].strip())

            if merchant_id not in self.merchants or loan_id not in self.merchants[merchant_id]:
                raise ValueError("Loan does not exist for merchant: " + merchant_id + ", loan: " + loan_id)
            
            fee = amount * fee_percentage / 100
            current_amount = self.merchants[merchant_id][loan_id]
            new_amount = current_amount - fee if current_amount - fee > 0 else 0
            self.merchants[merchant_id][loan_id] = math.trunc(new_amount)
        except ValueError as e:
            raise e
    
    def display(self):
        sorted_merchants = sorted(self.merchants.keys())
        for merchant in sorted_merchants:
            debt = sum(self.merchants[merchant].values())
            if debt > 0:
                print(f"{merchant}: {debt}")
        print("-----")

        
strip = StripeCapital()
strip.add_line(" CREATE_LOAN: acct_foobar,loan,5000")
strip.add_line("PAY_LOAN: acct_foobar,loan,1000")
strip.display()

strip = StripeCapital()
strip.add_line("CREATE_LOAN: acct_foobar,loan1,5000")
strip.add_line("CREATE_LOAN: acct_foobar,loan2,5000")
strip.add_line("TRANSACTION_PROCESSED: acct_foobar,loan1,500,10")
strip.add_line("TRANSACTION_PROCESSED: acct_foobar,loan2,500,1")
strip.display()

strip = StripeCapital()
strip.add_line("CREATE_LOAN: acct_foobar,loan1,1000")
strip.add_line("CREATE_LOAN: acct_foobar,loan2,2000")
strip.add_line("CREATE_LOAN: acct_barfoo,loan1,3000")
strip.add_line("TRANSACTION_PROCESSED: acct_foobar,loan1,100,1")
strip.add_line("PAY_LOAN: acct_barfoo,loan1,1000")
strip.add_line("INCREASE_LOAN: acct_foobar,loan2,1000")
strip.display()