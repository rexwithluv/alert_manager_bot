# AlertManager - Telegram Bot

En la casa donde vivo es algo habitual que una vez por semana o cada dos semanas, haya un corte de luz. A veces estoy en casa y no hay problema porque puedo apagar todos mis equipos o avisar a alguien que lo haga por mí, pero, ¿qué hago si no estoy? ¿Cómo me entero de que el SAI a entrado en funcionamiento y que es cuestión de tiempo que se acabe si la luz no vuelve? En caso de que la luz se vaya, el router pierde la conexión y por lo tanto, este sistema te avisará de que no tiene conexión con tu red doméstica, pues necesitas tener algún aparato con permanente corriente eléctrica y conexión a tu red doméstica mediante por ejemplo VPN.

El código consiste en un servidor websocket que corre sobre el equipo que tiene constante conexión a la red y eléctrica, y un cliente que corre sobre el equipo que puede verse afectado por la caída de red eléctrica o de conexión.

## Uso

Por el momento sin implementar, se prevee intentar que ambos corran sobre contenedores docker.
