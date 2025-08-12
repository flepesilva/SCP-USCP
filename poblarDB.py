from BD.sqlite import BD
import json

bd = BD()
scp     = False
uscp    = True
mhs = ['DOA']
cantidad = 0

DS_actions = [
    'V1-STD', 'V1-COM', 'V1-PS', 'V1-ELIT',
    'V2-STD', 'V2-COM', 'V2-PS', 'V2-ELIT',
    'V3-STD', 'V3-COM', 'V3-PS', 'V3-ELIT',
    'V4-STD', 'V4-COM', 'V4-PS', 'V4-ELIT',
    'S1-STD', 'S1-COM', 'S1-PS', 'S1-ELIT',
    'S2-STD', 'S2-COM', 'S2-PS', 'S2-ELIT',
    'S3-STD', 'S3-COM', 'S3-PS', 'S3-ELIT',
    'S4-STD', 'S4-COM', 'S4-PS', 'S4-ELIT',
]

paramsML = json.dumps({
    'MinMax'        : 'min',
    'DS_actions'    : DS_actions,
    'gamma'         : 0.4,
    'policy'        : 'e-greedy',
    'qlAlphaType'   : 'static',
    'rewardType'    : 'withPenalty1',
    'stateQ'        : 2
})



if uscp:
    # poblar ejecuciones USCP
    # instancias posibles a utilizar para este problema
    # u41		u51 	u61		ub1		clr10	ud1		unrf1	unrh1
    # u410	    u510	u62		ub2		clr11	ud2		unrf2	unrh2
    # u42		u52		u63		ub3		clr12	ud3		unrf3	unrh3
    # u43		u53		u64		ub4		clr13	ud4		unrf4	unrh4
    # u44		u54		u65		ub5		cyc06	ud5		unrf5	unrh5
    # u45		u55		ua1		uc1		cyc07	unre1	unrg1	
    # u46		u56		ua2		uc2		cyc08	unre2	unrg2	
    # u47		u57		ua3		uc3		cyc09	unre3	unrg3	
    # u48		u58		ua4		uc4		cyc10	unre4	unrg4	
    # u49		u59		ua5		uc5		cyc11	unre5	unrg5	
    instancias = bd.obtenerInstancias(f'''
                                      "clr10", "clr11", "clr12", "clr13",
                                      "cyc06", "cyc07", "cyc08", "cyc09", "cyc10", "cyc11"
                                      ''')
    iteraciones = 20
    experimentos = 1
    poblacion = 5
    for instancia in instancias:

        for mh in mhs:
            binarizaciones = ['V3-STD', 'V3-STD_LOG']
            for binarizacion in binarizaciones:
                
                data = {}
                data['experimento'] = f'{mh} {binarizacion}'
                data['MH']          = mh
                data['paramMH']     = f'iter:{str(iteraciones)},pop:{str(poblacion)},DS:{binarizacion},repair:complex,cros:0.9;mut:0.20'
                data['ML']          = ''
                data['paramML']     = ''
                data['ML_FS']       = ''
                data['paramML_FS']  = ''
                data['estado']      = 'pendiente'

                cantidad +=experimentos
                bd.insertarExperimentos(data, experimentos, instancia[0])

if scp:
    # poblar ejecuciones SCP
    # instancias posibles a utilizar para este problema
    # 41		51 		61		b1		d1		nrf1	nrh1
    # 410	    510		62		b2		d2		nrf2	nrh2
    # 42		52		63		b3		d3		nrf3	nrh3
    # 43		53		64		b4		d4		nrf4	nrh4
    # 44		54		65		b5		d5		nrf5	nrh5
    # 45		55		a1		c1		nre1	nrg1	
    # 46		56		a2		c2		nre2	nrg2	
    # 47		57		a3		c3		nre3	nrg3	
    # 48		58		a4		c4		nre4	nrg4	
    # 49		59		a5		c5		nre5	nrg5	
    instancias = bd.obtenerInstancias(f'''
                                      "41"
                                      ''')
    iteraciones = 100
    experimentos = 1
    poblacion = 10
    for instancia in instancias:

        for mh in mhs:
            binarizaciones = ['V3-STD','V3-STD_LOG']
            # binarizaciones = ['V3-ELIT_LOG']
            for binarizacion in binarizaciones:
                
                data = {}
                data['experimento'] = f'{mh} {binarizacion}'
                data['MH']          = mh
                data['paramMH']     = f'iter:{str(iteraciones)},pop:{str(poblacion)},DS:{binarizacion},repair:complex,cros:0.9;mut:0.20'
                data['ML']          = ''
                data['paramML']     = ''
                data['ML_FS']       = ''
                data['paramML_FS']  = ''
                data['estado']      = 'pendiente'

                cantidad +=experimentos
                bd.insertarExperimentos(data, experimentos, instancia[0])

print("------------------------------------------------------------------")
print(f'Se ingresaron {cantidad} experimentos a la base de datos')
print("------------------------------------------------------------------")

