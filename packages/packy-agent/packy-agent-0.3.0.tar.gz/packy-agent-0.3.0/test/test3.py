from sh import sleep

p = sleep(3, _bg=True)
print("prints immediately!")
# p.wait()
print("...and 3 seconds later")