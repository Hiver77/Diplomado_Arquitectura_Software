
# Actividad 1

# Integrantes 

* Leidy Marcela Ducuara Lenis
* Iver Johan Hincapie Betancur 
* Juan Diego Rojas Peña 
* Eliana Carolina Herrán Logreira. 



# Escenario 1

Para este escenario se elige el patrón Builder que pertenece a la familia de patrones Creacionales, este tipo de patrón se enfoca en la forma en que los objetos son creados. En este caso, el Builder permite construir un objeto Automóvil con múltiples configuraciones opcionales paso a paso, resuelve la situación del constructor telescópico, es decir se usa un solo constructor para todas las configuraciones, y por último separa el proceso de construcción de la representación del objeto final. Para el ejercicio si bien se supone que el cliente puede personalizar elegimos tener adicional la clase Director por si el cliente prefiere escoger automóviles con configuración predefinida.

---

## Resumen
- **Tipo de patrón:** Creacional
- **Patrón elegido:** **Builder**  

**Beneficios logrados:**
1. **Legibilidad y claridad:** construcción paso a paso.
2. **Inmutabilidad:** una vez creado, el "Automovil" no se puede modificar.
3. **Flexibilidad:** omitir atributos opcionales con *defaults* en el builder.
4. **Separación construcción/representación:** reglas y validaciones en el builder; el producto es simple.

## Diagrama de clase
![Diagrama car](01_Actividad/00_Diagramas_De_Clase/diagrama_builder_car.jpg)


## Lenguaje
- Lenguaje: Python 3.10+ (biblioteca estándar).  





# Escenario 2

Para este escenario se elige el patrón Bridge que pertenece a la familia de patrones Estructúrales, este tipo de patrón se enfoca en separar la plataforma (Abstracción) del tipo de mensaje que se quiere enviar, este patrón nos permite incluir otro tipo de notificaciones y plataforma sin modificar las clases existentes. 

## Resumen
- **Tipo de patrón:** Estructural   
- **Patrón elegido:** **Bridge**  

**Beneficios logrados:**

1. **Separación de responsabilidades:** La abstracción gestiona la lógica de negocio (qué y cuándo mostrar) y la implementación se encarga del cómo mostrar el mensaje según el tipo. 
2. **Escalabilidad:** Puedes añadir nuevas plataformas o nuevos tipos de notificación sin tocar el otro eje.
3. **Reducción de clases:** Evita la explosión de crear un tipo de mensaje por cada plataforma pasando a crear clases de manera jerárquica. 
4: **Flexibilidad en tiempo de ejecución:** La plataforma es intercambiable; puedes cambiar el canal en tiempo de ejecución (Web → Móvil → Desktop) sin reinstanciar ni duplicar lógica.


## Lenguaje
- Lenguaje: Python 3.10+ (biblioteca estándar).  

# Escenario 3

Para este escenario se elige el patrón Mediador que pertenece a la familia de patrones de Comportamiento, este tipo de patrón restringe las comunicaciones directas entre los objetos, forzándolos a colaborar únicamente a través de un objeto mediador. En nuestro caso al crear un objeto central como ChatRoom simplificamos las comunicaciones y evitamos las dependencias enlazadas entre los usuarios. 

## Resumen
- **Tipo de patrón:** De Comportamiento   
- **Patrón elegido:** **Mediador**  

**Beneficios logrados:**

1. **Facilita el mantenimiento:** Cada participante solo conoce al mediador (ChatRoom) no al resto. Un usuario puede entrar o salir sin modificar a los demás. 
2. **Mejor organización:** La lógica de coordinación, validaciones y políticas se centralizan en el mediador.  
3. **Reduce la complejidad:** El mediador evita la red de referencias punto a punto entre todos los componentes, ayudando a la mantenibildad y escalabilidad. 


## Lenguaje
- Lenguaje: Python 3.10+ (biblioteca estándar).