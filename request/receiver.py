
def fun(numero2):
    try:
        if numero2 == 0:
            raise Exception('general exceptions not caught by specific handling')

        print("siguio")

    except Exception:
        print('excepcion capturada')





