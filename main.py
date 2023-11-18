from db import  create_list
from functions import measure_point, downl_data

''' wywolanie funkcji do stworzenia listy id stacji '''

id_list = create_list()


''' petla wykonujaca funkcje przez wszystkie stacje zawarte w liscie '''

for id in id_list:

    var1 = downl_data(id)
    current = measure_point(0, 0, 0, 0, "")
    current.add_atr(var1)
    current.show_atr()
    current.conditions()
