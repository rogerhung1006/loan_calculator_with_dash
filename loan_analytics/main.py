from loan_analytics.Helper import *
from loan_analytics.Loan import *
from loan_analytics.LoanPortfolio import *
import pandas as pd

# from Helper import *
# from Loan import *
# from LoanPortfolio import *
# import pandas as pd

loans = LoanPortfolio()

def compute_schedule(principal, rate, payment, extra_payment):

    loan = None
    try:
        loan = Loan(principal=principal, rate=rate, payment=payment, extra_payment=extra_payment)
        loan.check_loan_parameters()
        loan.compute_schedule()
    except ValueError as ex:
        print(ex)
    loans.add_loan(loan)
    # Helper.plot(loan)
    # Helper.print(loan)

    # Return single loan schedule
    cols = ['Payment Number', 'Begin Principal', 'Payment', 'Extra Payment', 'Applied Principal', 'Applied Interest', 'End Principal']
    ind = pd.Index(cols)
    single_loan_schedule = pd.DataFrame(loan.schedule).set_index(ind).T



    print(round(loan.total_principal_paid, 2), round(loan.total_interest_paid, 2),
          round(loan.time_to_loan_termination, 0))

    if loans.get_loan_count() >= 2:
        print(f'num of loans: {loans.get_loan_count()}')
        loans.loans.pop(0)
        print(f'num of loans final: {loans.get_loan_count()}')
        loans.aggregate()
        # Helper.plot(loans)
        Helper.print(loans)

        # Return multiple loans schedule
        cols = ['Payment Number', 'Begin Principal', 'Payment', 'Extra Payment', 'Applied Principal', 'Applied Interest', 'End Principal']
        ind = pd.Index(cols)
        multiple_loan_schedule = pd.DataFrame(loans.schedule).set_index(ind).T
        return multiple_loan_schedule
    
    else:
        return single_loan_schedule


# if __name__ == '__main__':
#     compute_schedule(12000.0, 4.0, 70.0, 12.0)
#     compute_schedule(5000.0, 2.0, 20.0, 6.0)
#     compute_schedule(10000.0, 3.0, 60.0, 7.0)
