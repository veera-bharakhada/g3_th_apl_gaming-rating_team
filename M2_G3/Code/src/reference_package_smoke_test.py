"""Optional smoke test for the reference package example in TTT paper Code 7-9.

This does not produce the project's reported KPIs. It checks that the package's
three-event History/convergence/learning_curves example runs in an environment
where `trueskillthroughtime` is installed.
"""
def main():
    try:
        from trueskillthroughtime import History
    except Exception as exc:
        print('REFERENCE PACKAGE NOT AVAILABLE:', repr(exc))
        print('In Colab, try: %pip install trueskillthroughtime')
        return 2
    c1 = [['a'], ['b']]
    c2 = [['b'], ['c']]
    c3 = [['c'], ['a']]
    composition = [c1, c2, c3]
    h = History(composition, gamma=0.0)
    h.convergence()
    curves = h.learning_curves()
    for player in ('a','b','c'):
        print(player, curves[player])
    print('Reference package three-event example completed. This is a smoke test, not a full equivalence benchmark.')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
