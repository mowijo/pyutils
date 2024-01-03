from pybash import x



r = x("echo -e 'hallo, Welt\nhello, World\nbonjour Monde' | grep World | sed -e 's/World/world/g'")
print("\n")
print("\n ")
print("Execution Done ---------------------------")
print(" --- returnCode ---- ")
print(r.returnCode)
print(" ----- stdOut ------ ")
print(r.stdOut)
print(" ----- stdErr ------ ")
print(r.stdErr)

