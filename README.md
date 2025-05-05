Problema de los Filósofos Comensales
==================================================
Nombre: Said Omar Hernández Grande  
Nombre: Tania Joseline Reséndiz Díaz  
Sección: D07  
Actividad: 11  
Fecha: 04/05/2025

ÍNDICE
--------------------------------------------------
1. Introducción  
2. Objetivo  
3. Requerimientos del Problema  
4. Solución Propuesta  

1. Introducción
--------------------------------------------------
El interbloqueo (también conocido como deadlock, bloqueo mutuo o abrazo mortal) es un fenómeno en los sistemas concurrentes donde un conjunto de procesos se bloquea permanentemente al esperar recursos que nunca se liberarán. Este problema ocurre cuando se cumplen simultáneamente las condiciones de Coffman: mutua exclusión, retención y espera, no expropiación y espera circular. El problema de los filósofos comensales ejemplifica estas condiciones, lo que permite realizar diversas propuestas de solución al problema del interbloqueo mediante técnicas de sincronización.

2. Objetivo
--------------------------------------------------
Proponer una solución software al problema del interbloqueo a través del problema de los filósofos comensales. Se busca evitar que los filósofos caigan en espera infinita (deadlock) y garantizar que cada uno de ellos coma al menos seis veces.

3. Requerimientos del Problema
--------------------------------------------------
- 5 filósofos que alternan entre pensar y comer.
- Para comer, cada filósofo debe tomar los tenedores a su izquierda y derecha.
- No deben ocurrir interbloqueos.
- Todos los filósofos deben comer al menos 6 veces.
- Mostrar visualmente el progreso de cada filósofo (mediante GUI).
- Permitir iniciar, pausar/reanudar y detener la simulación.

4. Solución Propuesta
--------------------------------------------------
Esta implementación utiliza condiciones con mutex para sincronizar a los filósofos. Se basa en una estrategia tipo Monitores:

- Cada filósofo adquiere un lock global para modificar su estado.
- Verifica si puede comer: solo si sus vecinos no están comiendo.
- Si no puede comer, espera en su Condition.
- Al terminar de comer, notifica a sus vecinos para que puedan comer si es posible.
- Se utiliza una interfaz gráfica para mostrar estados y cantidad de comidas de cada filósofo.

Se evita el interbloqueo controlando cuidadosamente la entrada a la sección crítica y utilizando espera condicional solo cuando es seguro.
