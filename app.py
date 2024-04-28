from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_arbitrage_wager(initial_wager, initial_odds, second_odds):
    if initial_odds > 0 and second_odds > 0:
        # Both odds are positive, use the provided equation
        wager2 = (initial_wager + initial_wager * (initial_odds / 100)) / (1 + (second_odds / 100))
    elif initial_odds < 0 and second_odds < 0:
        # Both odds are negative, use the provided equation with negative odds
        wager2 = (initial_wager + initial_wager * (100 / abs(initial_odds))) / (1 + (100 / abs(second_odds)))
    elif initial_odds > 0 and second_odds < 0:
        # Initial odds positive, second odds negative
        wager2 = (initial_wager + initial_wager * (initial_odds / 100)) / (1 + (100 / abs(second_odds)))
    elif initial_odds < 0 and second_odds > 0:
        # Initial odds negative, second odds positive
        wager2 = (initial_wager + initial_wager * 100 / abs(initial_odds)) / (1 + (second_odds / 100))
    else:
        return None
    
    return round(wager2, 2)

def calculate_profit(wager_amount, odds):
    if odds > 0:
        return wager_amount * odds / 100
    elif odds < 0:
        return wager_amount * 100 / abs(odds)

@app.route('/')
def home():
    return render_template('arbitrageandwagers.html')

@app.route('/arbitrage', methods=['POST'])
def arbitrage():
    initial_wager = float(request.form['initial_wager'])
    initial_odds = float(request.form['initial_odds'])
    second_odds = float(request.form['second_odds'])
    
    arbitrage_wager = calculate_arbitrage_wager(initial_wager, initial_odds, second_odds)
    total_payout_initial = initial_wager + initial_wager * (initial_odds / 100)
    
    if second_odds > 0:
        total_payout_second = arbitrage_wager + arbitrage_wager * (second_odds / 100)
    else:
        total_payout_second = arbitrage_wager + arbitrage_wager * (100 / abs(second_odds))
    
    total_stake = initial_wager + arbitrage_wager
    profit = total_payout_initial - total_stake
    total_payout_combined = total_payout_initial + total_payout_second
    profit_percentage = (profit / (total_payout_combined/2)) * 100
    
    return render_template('results.html', arbitrage_wager=arbitrage_wager, 
                           total_payout_initial=total_payout_initial, 
                           total_payout_second=total_payout_second, 
                           total_stake=total_stake, profit=profit, 
                           profit_percentage=profit_percentage,
                           total_profit=None, total_payout_combined=None)

@app.route('/wagers', methods=['POST'])
def wagers():
    num_wagers = int(request.form['num_wagers'])
    total_stake = 0
    total_profit = 0
    
    for i in range(num_wagers):
        wager_amount = float(request.form[f'wager_amount_{i}'])
        odds = float(request.form[f'odds_{i}'])
        profit = calculate_profit(wager_amount, odds)
        total_stake += wager_amount
        total_profit += profit
    
    total_payout_combined = total_stake + total_profit
    
    return render_template('results.html', arbitrage_wager=None, 
                           total_payout_initial=None, 
                           total_payout_second=None, 
                           total_stake=total_stake, profit=None, 
                           profit_percentage=None,
                           total_profit=total_profit, 
                           total_payout_combined=total_payout_combined)

if __name__ == "__main__":
    app.run(debug=True)
