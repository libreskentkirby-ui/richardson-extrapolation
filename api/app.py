from flask import Flask, render_template, request
import math

# Corrected: Pointed the template_folder to the templates directory in the root
app = Flask(__name__, template_folder='../templates')

def evaluate_fx(expression, x_val):
    """Manually evaluates a mathematical string expression for a given x value."""
    # 1. Gi-convert ang common math shortcuts ngadto sa pormat nga masabtan sa Python
    safe_expr = expression.replace('^', '**')
    safe_expr = safe_expr.replace('ln(', 'log(')  # I-convert ang ln(x) ngadto sa log(x) automatic

    # 2. LISTAHAN SA MGA MATH UG TRIGONOMETRY FUNCTIONS
    allowed_words = {
        'x': x_val,
        'abs': abs,
        'exp': math.exp,
        'log': math.log,  # Natural Logarithm ln(x)
        'log10': math.log10,  # Log base 10

        # --- BASIC TRIGONOMETRY ---
        'sin': math.sin,  # Sine
        'cos': math.cos,  # Cosine
        'tan': math.tan,  # Tangent

        # --- RECIPROCAL TRIGONOMETRY ---
        'csc': lambda v: 1.0 / math.sin(v) if math.sin(v) != 0 else float('inf'),
        'sec': lambda v: 1.0 / math.cos(v) if math.cos(v) != 0 else float('inf'),
        'cot': lambda v: 1.0 / math.tan(v) if math.tan(v) != 0 else float('inf'),

        # --- INVERSE TRIGONOMETRY ---
        'asin': math.asin,  # Arcsine
        'acos': math.acos,  # Arccosine
        'atan': math.atan,  # Arctangent

        # --- MGA DUGANG NGA MAPUSLAN ---
        'sqrt': math.sqrt,  # Square root
        'pi': math.pi,  # Ang bili sa Pi (3.14159...)
        'e': math.e  # Euler's number (2.71828...)
    }

    return eval(safe_expr, {"__builtins__": None}, allowed_words)


@app.route('/', methods=['GET', 'POST'])
def home():
    results = []
    error = None

    # Default values nga makita sa input boxes sa sugod
    fx_str = '5 * x * exp(-2 * x)'
    x_target_str = '0.5'
    h_str = '0.2'

    if request.method == 'POST':
        try:
            # Pagkuha sa mga gi-input sa user gikan sa HTML form
            fx_str = request.form['fx']
            x_target = float(request.form['x_target'])
            h = float(request.form['h'])

            x_target_str, h_str = str(x_target), str(h)

            # --- CORE ALGORITHM: RICHARDSON'S EXTRAPOLATION ---

            # 1. Central Difference gamit ang tibuok nga step size (h)
            f_x_plus_h = evaluate_fx(fx_str, x_target + h)
            f_x_minus_h = evaluate_fx(fx_str, x_target - h)
            D_h = (f_x_plus_h - f_x_minus_h) / (2 * h)

            # 2. Central Difference gamit ang tunga sa step size (h/2)
            half_h = h / 2
            f_x_plus_half_h = evaluate_fx(fx_str, x_target + half_h)
            f_x_minus_half_h = evaluate_fx(fx_str, x_target - half_h)
            D_half_h = (f_x_plus_half_h - f_x_minus_half_h) / (2 * half_h)

            # 3. Richardson's Extrapolation Formula
            extrapolated_val = (4 * D_half_h - D_h) / 3

            # Pag-save sa mga kalkulasyon aron i-display sa HTML table
            results.append({
                'h': h,
                'D_h': D_h,
                'half_h': half_h,
                'D_half_h': D_half_h,
                'final_D': extrapolated_val
            })

        except Exception as e:
            error = f"Invalid Input or Syntax Error: {str(e)}"

    return render_template('index.html', results=results, error=error, fx=fx_str, x_target=x_target_str, h=h_str)