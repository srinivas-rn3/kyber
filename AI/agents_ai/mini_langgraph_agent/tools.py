import ast
import operator


def get_weather(city: str) -> str:
    """Return mock weather information for a given city."""
    weather_data = {
        "bangalore": "Cloudy, 27°C",
        "mumbai": "Rainy, 40°C",
        "delhi": "Sunny, 45°C",
        "hyderabad": "Hot, 43°C",
    }

    result = weather_data.get(city.lower())
    if result:
        return f"Weather in {city.title()}: {result}"
    return f"No weather data found for {city}."


def set_alarm(time: str) -> str:
    """Return a confirmation message for setting an alarm."""
    return f"Alarm set successfully for {time}."


def tell_joke() -> str:
    """Return a simple programmer joke."""
    return "Why do programmers prefer dark mode? Because light attracts bugs."


class SafeCalculator:
    """Safely evaluate arithmetic expressions using Python AST."""

    ALLOWED_BINARY_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    ALLOWED_UNARY_OPERATORS = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def evaluate(self, expression: str):
        parsed = ast.parse(expression, mode="eval")
        return self._evaluate_node(parsed.body)

    def _evaluate_node(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numeric constants are allowed.")

        if isinstance(node, ast.Num):
            return node.n

        if isinstance(node, ast.BinOp):
            left = self._evaluate_node(node.left)
            right = self._evaluate_node(node.right)
            operator_type = type(node.op)

            if operator_type not in self.ALLOWED_BINARY_OPERATORS:
                raise ValueError(f"Operator {operator_type.__name__} is not allowed.")

            if operator_type is ast.Pow and abs(right) > 10:
                raise ValueError("Exponent is too large.")

            return self.ALLOWED_BINARY_OPERATORS[operator_type](left, right)

        if isinstance(node, ast.UnaryOp):
            operand = self._evaluate_node(node.operand)
            operator_type = type(node.op)

            if operator_type not in self.ALLOWED_UNARY_OPERATORS:
                raise ValueError(f"Unary operator {operator_type.__name__} is not allowed.")

            return self.ALLOWED_UNARY_OPERATORS[operator_type](operand)

        raise ValueError(f"Unsupported expression element: {type(node).__name__}")


def calculate(expression: str) -> str:
    """Safely evaluate a simple arithmetic expression and return the result."""
    if not expression or not expression.strip():
        return "No calculation expression was provided."

    if len(expression) > 100:
        return "Calculation error: expression is too long."

    calculator = SafeCalculator()

    try:
        result = calculator.evaluate(expression.strip())
        return f"Calculation result: {expression} = {result}"
    except ZeroDivisionError:
        return "Calculation error: division by zero."
    except SyntaxError:
        return "Calculation error: invalid expression syntax."
    except ValueError as exc:
        return f"Calculation error: {exc}"
    except Exception:
        return "Calculation error: unsupported expression."