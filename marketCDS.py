import QuantLib as ql

# Set up the evaluation date and calendar
calendar = ql.TARGET()
todaysDate = ql.Date(1, ql.January, 2025)  # Use current date or a specific date
ql.Settings.instance().evaluationDate = todaysDate

# Flat interest rate of 0.25% for JPY
risk_free_rate = ql.YieldTermStructureHandle(ql.FlatForward(todaysDate, 0.0025, ql.Actual365Fixed()))

# CDS parameters
recovery_rate = 0.35  # Example recovery rate, adjust as needed
quoted_spreads = [0.0057572,
                  0.0084083,
                  0.0152213,
                  0.0231506,
                  0.0272022,
                  0.0305,
                  0.0333345,
                  0.0344355]  # Dummy spreads in decimal form

# Define maturities for 6M, 1Y, 2Y, 3Y, 4Y, 5Y, 7Y, 10Y
tenors = [
    ql.Period(6, ql.Months),
    ql.Period(1, ql.Years),
    ql.Period(2, ql.Years),
    ql.Period(3, ql.Years),
    ql.Period(4, ql.Years),
    ql.Period(5, ql.Years),
    ql.Period(7, ql.Years),
    ql.Period(10, ql.Years),
]

# Generate adjusted maturities
maturities = [calendar.adjust(todaysDate + x, ql.Following) for x in tenors]

# Create SpreadCdsHelper for each maturity and spread
instruments = [
    ql.SpreadCdsHelper(
        ql.QuoteHandle(ql.SimpleQuote(spread)),
        tenor,
        0,
        calendar,
        ql.Quarterly,
        ql.Following,
        ql.DateGeneration.TwentiethIMM,
        ql.Actual365Fixed(),
        recovery_rate,
        risk_free_rate,
    )
    for spread, tenor in zip(quoted_spreads, tenors)
]

# Build the hazard rate curve
hazard_curve = ql.PiecewiseFlatHazardRate(todaysDate, instruments, ql.Actual365Fixed())

# Print calibrated hazard rate values
print("Calibrated hazard rate values: ")
for x in hazard_curve.nodes():
    print("hazard rate on %s is %.7f" % x)

# Calculate and print survival probabilities for each year up to 10Y
print("\nSurvival probabilities:")
for i in range(1, 11):  # Years 1 to 10
    survival_prob = hazard_curve.survivalProbability(todaysDate + ql.Period(i, ql.Years))
    print(f"{i}Y survival probability: {survival_prob:.7f}")
