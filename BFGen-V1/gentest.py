import gene

a = gene.Gene("+++")
b = a.clone()
assert a.code == b.code, "CLONE ERROR"
a.mutate(10)
assert a.code != b.code, "MUTATION ERROR"
assert b.run()[0] == 3, "RUN + ERROR"
assert gene.Gene("+++---").run()[0] == 0, "RUN +- ERROR"

assert gene.Gene(">+++++").run()[1] == 5, "RUN >+ ERROR"
assert gene.Gene("++++[>+++<-]").run()[1] == 12, "RUN [] ERROR"
print("NO ERRORS")