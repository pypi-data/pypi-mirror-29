=====
Usage
=====

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

To use validatorpy in a project::

    import validatorpy

