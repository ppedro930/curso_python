import sys

#tupla = (43,12)
#tupla_1 = (43,)
#tupla_falsa = (43) #como no tiene la coma entonces para python no es un tupla

##print(type(tupla_1))
##print(type(tupla_falsa))

##print(tupla_1[0]) # provoca typeError

t_base = (10,20,30)
#t_base[0] = 99 # error , las tuplas no se modifican

#solucion 1 : convertirlo a lista
##print(f"lugar de memoria antes de convers {id(t_base)}")
# t_base= list(t_base)
# t_base[0]=99

t_base =(99,) + t_base[1:] #desaparece la primera pocision para colocar el 99 en esa posicion

##print(f"lugar de memoria despues de de convers{id(t_base)}")
##print(f"solucion 2{t_base}")

###############################3


# #print(f"solucion 2 para modificar tuplas usar slicings: {t_base}")

t_base= t_base + (40,)

##print(f"lugar de memoria antes de convers {id(t_base)}")
# t_base= list(t_base)
# t_base[0]=99
##print(f"lugar de memoria despues de de convers{id(t_base)}")


resultado = t_base + tuple([40,50])

##print(resultado)

lista_orden = sorted(resultado)

tupla_ordenada = tuple(lista_orden)

##print(f"tupla ordenada {lista_orden} lo saca en tipo lista {type(tupla_ordenada)}")

t_extend = (1,2,[3,4])

#print(t_extend)
#print({id(t_extend)})

t_extend[2].extend([9,9])


#print(t_extend)
#print({id(t_extend)})

t_extend[2][:]=[9,9]

#print(t_extend)
#print({id(t_extend)})

tupla_2 = (1,2,[3,4])
a,b,_ = tupla_2
tupla_2 = (a,b,[9,9])

print(f"tupla editada it 2{tupla_2}")
print(f" id tupla {id(tupla_2)}")

print(f"peso de {sys.getsizeof(tupla_2)}")


