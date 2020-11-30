from loan_analytics.Loan import Loan
from loan_analytics.LoanPortfolio import LoanPortfolio
import pandas as pd

# from Loan import Loan
# from LoanPortfolio import LoanPortfolio
# import pandas as pd


class LoanImpacts:
    """ Contributor Impacts to Loan class
    """

    def __init__(self, principal, rate, payment, extra_payment, contributions):
        self.principal = principal
        self.rate = rate
        self.payment = payment
        self.extra_payment = extra_payment
        self.contributions = contributions

    def compute_impacts(self):
        # setup a loan portfolio
        # loan_portfolio = LoanPortfolio()

        # loan with all contributions (mi)_all
        #
        loan_all = Loan(principal=self.principal, rate=self.rate,
                        payment=self.payment, extra_payment=self.extra_payment + sum(self.contributions))
        loan_all.check_loan_parameters()
        loan_all.compute_schedule()

        # loan with no contributions (mi)_0
        #
        loan_none = Loan(principal=self.principal, rate=self.rate,
                         payment=self.payment, extra_payment=self.extra_payment)
        loan_none.check_loan_parameters()
        loan_none.compute_schedule()

        micro_impact_interest_paid_all = \
            (loan_none.total_interest_paid - loan_all.total_interest_paid) / loan_all.total_interest_paid
        micro_impact_duration_all = -\
            (loan_none.time_to_loan_termination - loan_all.time_to_loan_termination) / loan_all.time_to_loan_termination

        # micro_impact_interest_paid_all = loan_none.total_interest_paid / loan_all.total_interest_paid
        # micro_impact_duration_all = loan_none.time_to_loan_termination / loan_all.time_to_loan_termination

        # print(f'\nIndex\tInterestPaid\tDuration\tMIInterest\tMIDuration')
        # print(f'ALL \t\t',
        #       round(loan_all.total_interest_paid, 2), f'\t\t', loan_all.time_to_loan_termination)
        # print(f'0\t\t\t',
        #       round(loan_none.total_interest_paid, 2), f'\t\t', loan_none.time_to_loan_termination, f'\t\t',
        #       round(micro_impact_interest_paid_all, 4), f'\t', round(micro_impact_duration_all, 4))
        
        comparison_table = pd.DataFrame(columns=['Index', 'InterstPaid', 'Duration', 'MIInterest', 'MIDuration']).set_index('Index')
        comparison_table.loc['all'] = [round(loan_all.total_interest_paid, 2), loan_all.time_to_loan_termination, '-', '-']
        comparison_table.loc[0] = [round(loan_none.total_interest_paid, 2), loan_none.time_to_loan_termination, round(micro_impact_interest_paid_all, 4), round(micro_impact_duration_all, 4)]
        
        

        # iterate over each contribution (mi)_index
        #
        for index, contribution in enumerate(self.contributions):
            loan_index = Loan(principal=self.principal, rate=self.rate, payment=self.payment,
                              extra_payment=self.extra_payment + sum(self.contributions) - contribution)
            loan_index.check_loan_parameters()
            loan_index.compute_schedule()

            micro_impact_interest_paid = \
                (loan_index.total_interest_paid - loan_all.total_interest_paid) / loan_all.total_interest_paid
            micro_impact_duration = \
                (loan_index.time_to_loan_termination - loan_all.time_to_loan_termination) / loan_all.time_to_loan_termination

            # micro_impact_interest_paid = loan.total_interest_paid / loan_all.total_interest_paid
            # micro_impact_duration = loan.time_to_loan_termination / loan_all.time_to_loan_termination

            # print(index+1, f'\t\t\t',
            #       round(loan_index.total_interest_paid, 2), f'\t\t', loan_index.time_to_loan_termination, f'\t\t',
            #       round(micro_impact_interest_paid, 4), f'\t', round(micro_impact_duration, 4))
            comparison_table.loc[index+1] = [round(loan_index.total_interest_paid, 2), loan_index.time_to_loan_termination, round(micro_impact_interest_paid, 4), round(micro_impact_duration, 4)]
        # print(f'Below is the pd table')
        # print(comparison_table)
        # print(f'End')
        return comparison_table.reset_index()
# if __name__ == '__main__':
#     loan_impacts = LoanImpacts(principal=68000, rate=4, payment=899,
#                                extra_payment=0, contributions=[10, 100, 1000])
#     loan_impacts.compute_impacts()
