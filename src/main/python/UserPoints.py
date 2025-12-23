'''
Background
Our users have points in their accounts.
Users only see a single balance in their accounts.
But for reporting purposes we actually track their points per payer/partner.
In our system, each transaction record contains:
   payer (String), points (String), timestamp (date).
For earning points it is easy to assign a payer, we know which actions earned the points.
And thus which partner should be paying for the points.

When a user spends points, they don't know or care which payer the points come from.
But, our accounting team does car how the points are spent.
There are two rules for determining what points to "spend" first:
   We want the oldest points to be spent first
   We want no payer's points to go negative

You need to do:
   Add transaction for a specific payer and date.
   Spend points using the rules above and return a list of
      {"payer": <string>, "points": <integer>} for each call
   Return all payer point balances.

Example
Suppose you call your add transaction route with the following sequence of calls:
   { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }
   { "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" }
   { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" }
   { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" }
   { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }

Then you call your spend points route with the following request:
   { "points": 5000 }
The expected response from the spend call would be:
   [
      { "payer": "DANNON", "points": -100 },
      { "payer": "UNILEVER", "points": -200 },
      { "payer": "MILLER COORS", "points": -4,700 }
   ]
A subsequent call to the points balance route, after the spend, should returns the following results:
   {
      "DANNON": 1000,
      "UNILEVER": 0,
      "MILLER COORS": 5300
   }

FAQ: For any requirements not specified via an example, use your best judgement to determine the expected result.
'''

from datetime import datetime


class Transaction:
    def __init__(self, timestamp, payer, point):
        self.timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        self.payer = payer
        self.point = point


class UserPoints:
    def __init__(self):
        self.transactions = []
    
    def add(self, payer, point, timestamp):
        self.transactions.append(Transaction(timestamp, payer, point))
        self.transactions.sort(key=lambda t: t.timestamp)
    
    def spend(self, point):
        deductions = {}
        
        for transaction in self.transactions:
            if point == 0:
                break
            
            deduction = min(transaction.point, point)
            transaction.point -= deduction
            point -= deduction
            
            if transaction.payer not in deductions:
                deductions[transaction.payer] = 0
            deductions[transaction.payer] += deduction
        
        result = []
        for payer, amount in deductions.items():
            result.append(f"{payer}: -{amount}")
        
        return result
    
    def get_balance(self):
        balances = {}
        
        for transaction in self.transactions:
            if transaction.payer not in balances:
                balances[transaction.payer] = 0
            balances[transaction.payer] += transaction.point
        
        result = []
        for payer, amount in balances.items():
            result.append(f"{payer}: {amount}")
        
        return result


def run():
    p1 = UserPoints()
    p1.add("DANNON", 1000, "2020-11-02T14:00:00Z")
    p1.add("UNILEVER", 200, "2020-10-31T11:00:00Z")
    p1.add("DANNON", -200, "2020-10-31T15:00:00Z")
    p1.add("MILLER COORS", 10000, "2020-11-01T14:00:00Z")
    p1.add("DANNON", 300, "2020-10-31T10:00:00Z")
    
    print(p1.get_balance())
    print(p1.spend(5000))
    print(p1.get_balance())


if __name__ == "__main__":
    run()
