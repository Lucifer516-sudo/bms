class Compute:
    def __init__(self) -> None:
        pass

    def simple_interest(self, P: float, n: int, r: float):
        """
        WKT,
            S.I = (P * n * r) / 100

            where,
                (float) | P -> Principal Amount - The Amount that we payed to the Deposit or that is in the bank No. of days
                (float) | n -> No. of days / Months
                (float) | r -> Rate of Interest
                (float) | S.I -> Result Amount
        """
        s_i = (P * n * r) / 100
        interest_amount = s_i - P
        return (s_i, interest_amount)

    def compound_interest(self, P: float, n: int, r: float, t: int):
        """
        A = P * ( 1 + ((r/100)/ n))** (n*t)
        n -> Compouding Periods
        t -> Time Period
        """
        A = P * ((1 + ((r / 100) / n))) ** (n * (t / 12))

        interest_amount: float = float(A - P)
        return (A, interest_amount)
