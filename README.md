# Linjeföljare

En linjeföljande robot byggd med Raspberry Pi 5, LEGO SPIKE-motorer och en reflexsensor-array. En kamera ska hjälpa roboten att se hur linjen fortsätter framåt, så att den kan köra mjukare och effektivare.

> Projektet är under utveckling. Mycket är ännu inte bestämt, och det här dokumentet beskriver bara det som redan är klart.

## Mål

- Följa en linje stabilt och mjukt.
- Använda kameran för att förutse linjens form framåt.
- Låta sensorarrayen hålla roboten exakt på linjen.

## Hårdvara

- Raspberry Pi 5
- Kameramodul till Raspberry Pi
- Pololu QTR-8A Reflectance Sensor Array (8 sensorer)
- Raspberry Pi Build HAT
- LEGO SPIKE-motorer

## Grundidé

Styrningen delas i två steg. Sensorarrayen styr roboten längs linjen med en PID-regulator. Kameran tittar längre fram och ger information som påverkar hur roboten kör. Hur de två stegen exakt samverkar är ännu inte bestämt.

## Status

Under utveckling. Det finns inga installations- eller användningsinstruktioner än.

## Licens

Inte bestämd ännu.