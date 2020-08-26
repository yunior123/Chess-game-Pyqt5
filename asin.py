import threading


def foo():
    for _ in range(500):
        print("Hello threading!")


my_thread = threading.Thread(target=foo)

my_thread.daemon = True
my_thread.start()


for _ in range(500):
    print("Continue!")