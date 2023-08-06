# -*- coding: utf-8 -*-

"""Main module."""
import re

def validate(value, indextype=None, customExpression=None):
  """
    Evaluates if a string complies with a predefined data type, according to a regular
    expression customized or predefined

    @param: value: String to evaluate
    @param: indextype (Default: Integer number) Predefine type
    @param: customExpression (Optional) Custom regular expression

    Expressions table
    index   Description
    0       Integer number
    1       Alphanumeric characters (English alphabet)
    2       Only characters (English alphabet)
    3       Decimal number
    4       Password policy (Capital letter, minuscule, number, special character and min length 8)
  """
  expressions = {
    0: "^\-?\d+$",
    1: "^[0-9a-zA-Z]+$",
    2: "^[a-zA-Z]+$",
    3: "^[\-\+]?(([0-9]+)([\.,]([0-9]+))?|([\.,]([0-9]+))?)$",
    4: "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&.+-\/])[A-Za-z\d$@$!%*?&.+-\/]{8,}"
  }

  expressions = expressions[indextype] if customExpression is None else customExpression
  return bool(re.match(expressions, value))

